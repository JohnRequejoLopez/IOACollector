

def initialize(mode: str = None):
    """
    Initializes the environment, credentials, and API client.
    Returns:
        args: Parsed arguments.
        ioa: Initialized IOA object with authenticated API client.
    """
    from .crwd import IOA
    from .api_client import APIClient
    from .app import (
        EnvironmentManager, 
        Argument
    )

    args = Argument(mode=mode)
    env_manager = EnvironmentManager()
    env_manager.check_and_configure()
    
    args.client_id, args.client_secret = env_manager.get_credentials()
    print(f"Using CLIENT_ID: {args.client_id}")

    client = APIClient(
        base_url="https://api.crowdstrike.com",
        client_id=args.client_id,
        client_secret=args.client_secret 
    )

    ioa = IOA(client)

    return args, ioa

def create():
    """
    Creates and enables an IOA rule.
    """
    args, ioa = initialize(mode='create')

    ruleInstanceID = ioa.NewIOARule(
        data=args.data,
        rulegroup_id=args.rulegroup_id,
        ruletype="9",
        dryRun=args.dry_run
    )['resources'][0]['instance_id']

    ioa.EnableRule(rulegroup_id=args.rulegroup_id, rule_id=ruleInstanceID)
    IOARuleName = ioa.GetIOAGroupByID(id=args.rulegroup_id)[0]['name']

    print(f"Rule with id {ruleInstanceID} has been successfully created and enabled under the IOA rule with name: `{IOARuleName}`.")

def delete():
    """
    Deletes and disables an IOA rule.
    """
    args, ioa = initialize(mode='delete')

    ioa.DeleteRule(rule_id=args.rule_id, rulegroup_id=args.rulegroup_id, dryRun=args.dry_run)
    IOARuleName = ioa.GetIOAGroupByID(id=args.rulegroup_id)[0]['name']
    
    print(f"Rule with id {args.rule_id} has been successfully disabled and deleted from the IOA rule: `{IOARuleName}`.")

def configure():
    """
    Set new API keys.
    """
    from .app import EnvironmentManager

    EnvironmentManager().setup_environment()

if __name__ == '__main__':
    message = 'Generates and submits IOA (Indicators of Attack) rules to a rule group via API using a defined template and threat data.'
    print(message)