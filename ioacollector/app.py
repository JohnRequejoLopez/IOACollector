from argparse import Namespace

class EnvironmentManager:
    """
    Manages application secrets stored in a `.env` file for local virtual environments.
    """

    def __init__(self, prefix: str = "IOACollector"):
        """
        Initializes the manager and loads existing environment variables from `.env`.

        Args:
            prefix (str): Prefix used to identify the environment variable keys.
        """
        from dotenv import (
            load_dotenv, 
            find_dotenv
        )
        
        self.prefix = prefix
        self.env_file = find_dotenv()
        if not self.env_file:
            self.env_file = ".env"

        load_dotenv(self.env_file)
        
        self.client_id_key = f"{self.prefix}_CLIENT_ID"
        self.client_secret_key = f"{self.prefix}_CLIENT_SECRET"

    def check_and_configure(self) -> None:
        """
        Checks if the required environment variables exist. If not, prompts the user
        to input them and stores them securely in the `.env` file.
        """
        from os import getenv

        client_id = getenv(self.client_id_key)
        client_secret = getenv(self.client_secret_key)

        if not client_id or not client_secret:
            print("Environment variables not set. Starting configuration...")
            self.setup_environment()
        else:
            print("Environment variables already configured.")

    def setup_environment(self) -> None:
        """
        Prompts the user for credentials and writes them to the `.env` file.
        """
        from dotenv import set_key
        from getpass import getpass

        client_id = input("Enter your CLIENT_ID: ")
        client_secret = getpass("Enter your CLIENT_SECRET (input hidden): ")

        set_key(self.env_file, self.client_id_key, client_id)
        set_key(self.env_file, self.client_secret_key, client_secret)

        print("\nCredentials successfully configured.")
        exit()

    def get_credentials(self) -> str:
        """
        Retrieves the configured credentials from environment variables.

        Returns:
            tuple: A tuple containing (client_id, client_secret).
        """
        from os import getenv

        id_key = f"{self.prefix}_CLIENT_ID"
        secret_key = f"{self.prefix}_CLIENT_SECRET"

        return getenv(id_key), getenv(secret_key)

def Argument(mode: str = None) -> Namespace:
    """
    Parse command line arguments based on the mode of operation (create or delete).
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='IOACollector',
        description='Generates and submits IOA (Indicators of Attack) rules to a rule group via API using a defined template and threat data.',
        epilog='Example: python ioa_collector.py --rulegroup-id <RULEGROUP_ID> --data <IP or indicator> --template <TEMPLATE_PATH>'
    )

    parser.add_argument(
        '--rulegroup-id',
        type=str,
        required=True,
        help='ID of the rule group where the new IOA rule will be added.'
    )

    if mode == 'create':
        parser.add_argument(
            '--data',
            type=str,
            required=True,
            help='Indicator data used to generate the rule (e.g., IP address or domain).'
        )

    elif mode == 'delete':
        parser.add_argument(
            '--rule-id',
            type=str,
            required=True,
            help='ID of the IOA rule to be deleted.'
        )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Only print the payload that would be submitted, without actually sending it.'
    )

    return parser.parse_args()