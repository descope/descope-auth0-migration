from migration_utils import fetch_auth0_users, process_users, fetch_auth0_roles, process_roles, fetch_auth0_organizations, process_auth0_organizations, process_users_with_passwords, fetch_auth0_users_from_file
import sys
import argparse
import json


def main():
    """
    Main function to process Auth0 users, roles, permissions, and organizations, creating and mapping them together within your Descope project.
    """
    dry_run = False
    verbose = False
    with_passwords = False
    passwords_file_path = ""
    from_json = False
    json_file_path = ""
    
    
    parser = argparse.ArgumentParser(description='This is a program to assist you in the migration of your users, roles, permissions, and organizations to Descope.')
    parser.add_argument('--dry-run', action='store_true', help='Enable dry run mode')
    parser.add_argument('--verbose','-v', action='store_true',help='Enable verbose printing for real migration and dry runs')
    parser.add_argument('--with-passwords', nargs=1, metavar='file-path', help='Run the script with passwords from the specified file')
    parser.add_argument('--from-json', nargs=1, metavar='file-path', help='Run the script with users from the specified file rather than API')
    
    args = parser.parse_args()

    if args.dry_run:
        dry_run=True
    
    if args.verbose:
        verbose = True

    if args.with_passwords:
        passwords_file_path = args.with_passwords[0]
        with_passwords = True
        print(f"Running with passwords from file: {passwords_file_path}")

    if with_passwords:
        found_password_users, successful_password_users, failed_password_users = process_users_with_passwords(passwords_file_path, dry_run, verbose)
    
    if args.from_json:
        json_file_path = args.from_json[0]
        from_json=True

    # Fetch and Create Users
    if from_json == False:
        auth0_users = fetch_auth0_users()
        # print(auth0_users)
    else:
        auth0_users = fetch_auth0_users_from_file(json_file_path)
        
    
    failed_users, successful_migrated_users, merged_users, disabled_users_mismatch = process_users(auth0_users, dry_run, from_json, verbose)

    # Fetch, create, and associate users with roles and permissions
    auth0_roles = fetch_auth0_roles()
    failed_roles, successful_migrated_roles, roles_exist_descope, failed_permissions, successful_migrated_permissions, total_existing_permissions_descope, roles_and_users, failed_roles_and_users = process_roles(auth0_roles, dry_run, verbose)

    # Fetch, create, and associate users with Organizations
    auth0_organizations = fetch_auth0_organizations()
    successful_tenant_creation, tenant_exists_descope, failed_tenant_creation, failed_users_added_tenants, tenant_users = process_auth0_organizations(auth0_organizations, dry_run, verbose)
    if dry_run == False:
        if with_passwords:
            print("=================== Password User Migration ====================")
            print(f"Auth0 Users password users in file {found_password_users}")
            print(f"Successfully migrated {successful_password_users} users")
            if len(failed_password_users) !=0:
                print(f"Failed to migrate {len(failed_password_users)}")
                print(f"Users which failed to migrate:")
                for failed_user in failed_password_users:
                    print(failed_password_users)
            print(f"Created users within Descope {successful_password_users}")

        print("=================== User Migration =============================")
        print(f"Auth0 Users found via API {len(auth0_users)}")
        print(f"Successfully migrated {successful_migrated_users} users")
        print(f"Successfully merged {len(merged_users)} users")
        if verbose:
            for merged_user in merged_users:
                print(f"Merged user: {merged_user}")
        if len(disabled_users_mismatch) !=0:
            print(f"Users migrated, but disabled due to one of the merged accounts being disabled {len(disabled_users_mismatch)}")
            print(f"Users disabled due to one of the merged accounts being disabled {disabled_users_mismatch}")
        if len(failed_users) !=0:
            print(f"Failed to migrate {len(failed_users)}")
            print(f"Users which failed to migrate:")
            for failed_user in failed_users:
                print(failed_user)
        print(f"Created users within Descope {successful_migrated_users - len(merged_users)}")

        print("=================== Role Migration =============================")
        print(f"Auth0 Roles found via API {len(auth0_roles)}")
        print(f"Existing roles found in Descope {roles_exist_descope}")
        print(f"Created roles within Descope {successful_migrated_roles}")
        if len(failed_roles) !=0:
            print(f"Failed to migrate {len(failed_roles)}")
            print(f"Roles which failed to migrate:")
            for failed_role in failed_roles:
                print(failed_role)

        print("=================== Permission Migration =======================")
        print(f"Auth0 Permissions found via API {len(failed_permissions) + successful_migrated_permissions + len(total_existing_permissions_descope)}")
        print(f"Existing permissions found in Descope {len(total_existing_permissions_descope)}")
        print(f"Created permissions within Descope {successful_migrated_permissions}")
        if len(failed_permissions) !=0:
            print(f"Failed to migrate {len(failed_permissions)}")
            print(f"Permissions which failed to migrate:")
            for failed_permission in failed_permissions:
                print(failed_permission)

        print("=================== User/Role Mapping ==========================")
        print(f"Successfully role and user mapping")
        for success_role_user in roles_and_users:
            print(success_role_user)
        if len(failed_roles_and_users) !=0:
            print(f"Failed role and user mapping")
            for failed_role_user in failed_roles_and_users:
                print(failed_role_user)

        print("=================== Tenant Migration ===========================")
        print(f"Auth0 Tenants found via API {len(auth0_organizations)}")
        print(f"Existing tenants found in Descope {tenant_exists_descope}")
        print(f"Created tenants within Descope {successful_tenant_creation}")
        if len(failed_tenant_creation) !=0:
            print(f"Failed to migrate {len(failed_tenant_creation)}")
            print(f"Tenants which failed to migrate:")
            for failed_tenant in failed_tenant_creation:
                print(failed_tenant)

        print("=================== User/Tenant Mapping ========================")
        print(f"Successfully tenant and user mapping")
        for tenant_user in tenant_users:
            print(tenant_user)
        if len(failed_users_added_tenants) !=0:
            print(f"Failed tenant and user mapping")
            for failed_users_added_tenant in failed_users_added_tenants:
                print(failed_users_added_tenant)

if __name__ == "__main__":
    main()
