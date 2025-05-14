import os
import sys

from msal import PublicClientApplication

# Ensure the environment are set, use constant values as default if not
from pm_studio_mcp.constant import (
    GRAPH_CLIENT_ID as client_id,
    GRAPH_TENANT_ID as tenant_id,
    GRAPH_SCOPE as scope,
)

class AuthUtils:
    client_id = os.environ['GRAPH_CLIENT_ID'] if 'GRAPH_CLIENT_ID' in os.environ else client_id
    tenant_id = os.environ['GRAPH_TENANT_ID'] if 'GRAPH_TENANT_ID' in os.environ else tenant_id
    scopes = scope  # Adjust scopes as needed
    authority = "https://login.microsoftonline.com/" + tenant_id
    
    app = PublicClientApplication(
        client_id=client_id,
        authority=authority,
        # enable_broker_on_mac=True if sys.platform == "darwin" else False, #needed for broker-based flow
        # enable_broker_on_windows=True if sys.platform == "win32" else False, #needed for broker-based flow
    )
    
    def login():
        """
        Authenticate with MSAL and return the access token.

        Returns:
            str: The access token
        """
        try:
            print("Authenticating...")

            # Try to get token silently from cache first
            accounts = AuthUtils.app.get_accounts()
            if accounts:
                print ("Found cached account: ")
                for account in accounts:
                    print(f"  {account['username']}")
                result = AuthUtils.app.acquire_token_silent(AuthUtils.scopes, account=accounts[0])
                if result:
                    print("Retrieved token from cache")
                    return result['access_token']

            # If no cached token, do interactive authentication
            result = AuthUtils.app.acquire_token_interactive(
                AuthUtils.scopes
                # port=0,  # Specify the port if needed
                # parent_window_handle=msal.PublicClientApplication.CONSOLE_WINDOW_HANDLE #needed for broker-based flow
            )

            if "access_token" not in result:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                sys.exit(1)

            print("Authentication successful!")

            return result["access_token"]

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            sys.exit(1)