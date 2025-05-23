import json
from .api_client import APIClient

class IOA:
    """
    A wrapper for interacting with the CrowdStrike IOA API using an authenticated API client.
    Provides methods to create, enable, and delete IOA rules, as well as retrieve rule group information.
    """

    def __init__(self, client: APIClient):
        """
        Initializes the IOA object with a given API client.

        Args:
            client (APIClient): An authenticated API client instance.
        """
        self.client = client

    def __DataType__(self, data: str):
        """
        Determines the type of indicator (IP or domain) based on the input data
        and returns metadata used in rule creation.

        Args:
            data (str): The indicator data (IP address or domain).

        Returns:
            tuple: A tuple containing the type ('ip' or 'domain'), rule type ID, and a descriptive name.

        Raises:
            ValueError: If the data is not a valid IP address or domain.
        """
        import validators
        
        if validators.ip_address.ipv4(data):
            return 'ip', 9, f"Block IP {data}"
        elif validators.domain(data):
            return 'domain', 11, f"Block Domain {data}"
        else:
            raise ValueError("Invalid data format: must be an IP or domain.")

    def GetIOAGroupByID(self, id: str):
        """
        Retrieves information for a specific IOA rule group by ID.

        Args:
            id (str): The ID of the rule group.

        Returns:
            list: A list of rule group resources (usually a single item).
        """
        response = self.client.Request(
            method="GET",
            endpoint="/ioarules/entities/rule-groups/v1",
            params={"ids": id}
        )
        return response.json().get("resources", [])

    def NewIOARule(self, data: str, rulegroup_id: str, ruletype: str, dryRun: bool):
        """
        Creates a new IOA rule based on the input data and rule group.

        Args:
            data (str): The indicator (IP or domain) to block.
            rulegroup_id (str): The ID of the rule group to which the rule will be added.
            ruletype (str): The rule type identifier (e.g., "9").
            dryRun (bool): If True, prints the payload instead of submitting it.

        Returns:
            dict: The API response containing the created rule's details.

        Exits:
            Prints and exits if dryRun is True.
        """
        from .jinja import LoadTemplate
        from json import dumps
        
        ptype, ruletype_id, name = self.__DataType__(data)
        
        payload = {
            "name": name,
            "description": "Generated by IOACollector designed by John Requejo.",
            "comment": "",
            "rulegroup_id": rulegroup_id,
            "ruletype_id": str(ruletype_id),
            "pattern_severity": "medium",
            "action_label": "kill_process",
            "disposition_id": 30,
            "field_values": LoadTemplate(templateName=f"{ptype}.yml.j2").render({'data': data}).json()
        }

        if dryRun:
            print("[Dry Run] This is the payload that would be sent:")
            print(dumps(payload, indent=2))
            exit()
        
        return self.client.Request(
            method="POST",
            endpoint="/ioarules/entities/rules/v1",
            json=payload
        ).json()

    def EnableRule(self, rule_id: str, rulegroup_id: str):
        """
        Enables a specific rule within a rule group.

        Args:
            rule_id (str): The instance ID of the rule to enable.
            rulegroup_id (str): The ID of the rule group containing the rule.

        Returns:
            dict: The API response confirming the update.

        Raises:
            ValueError: If the rule group cannot be found.
        """
        group = self.GetIOAGroupByID(rulegroup_id)
        
        if not group:
            raise ValueError("IOA rule group not found.")

        payload = {
            "rulegroup_id": rulegroup_id,
            "comment": "Enabling rule using IOACollector a tool designed by John Requejo.",
            "rulegroup_version": int(group[0]["version"]),
            "rule_updates": [
                {"enabled": True, "instance_id": rule_id}
            ]
        }
        return self.client.Request(
            method="PATCH",
            endpoint="/ioarules/entities/rules/v2",
            json=payload
        ).json()
    
    def DeleteRule(self, rule_id: str, rulegroup_id: str, dryRun: bool) -> json:
        """
        Deletes a rule from a rule group.

        Args:
            rule_id (str): The ID of the rule to delete.
            rulegroup_id (str): The ID of the rule group containing the rule.
            dryRun (bool): If True, prints the request parameters without deleting.

        Returns:
            dict: The API response confirming deletion.

        Exits:
            Prints and exits if dryRun is True.
        """
        from json import dumps

        params = {
            "rule_group_id": rulegroup_id,
            "comment": "Deleted by IOACollector designed by John Requejo.",
            "ids": str(rule_id)
        }

        if dryRun:
            print("[Dry Run] This is the payload that would be sent:")
            print(dumps(params, indent=2))
            exit()

        return self.client.Request(
            method="DELETE",
            endpoint="/ioarules/entities/rules/v1",
            params=params
        ).json()