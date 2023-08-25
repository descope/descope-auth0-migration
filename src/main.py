from migration_utils import read_auth0_export, fetch_auth0_users, process_users
import sys


def main(file_path):
    """
    Main function to process Auth0 users and create them in Descope.

    Args:
    - file_path (str): The path to the Auth0 export file.
    """
    auth0_export_data = read_auth0_export(file_path)
    auth0_users = fetch_auth0_users()
    process_users(auth0_export_data, auth0_users)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python migrateAuth0ToDescope.py <path_to_auth0_export_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
