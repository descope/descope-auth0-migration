<img width="1400" alt="Descope Auth0 Migration Tool" src="https://github.com/descope/descope-auth0-migration/assets/32936811/992ee6e4-682c-4659-b333-f1d32c16258f">

# Descope Auth0 User Migration Tool

This repository includes a Python utility for migrating your Auth0 users, organizations, permissions, and roles to Descope.

This utility allows you to migrate users by loading them from the Auth0 API, and optionally, you can load users' passwords from the exported password file received from Auth0.

## Setup 💿

1. (Optional) To export hashed password from Auth0, open a [ticket](https://support.auth0.com/tickets) with Auth0 support to
   request an export of your user's password hashes.

2. Clone the Repo:

```
git clone git@github.com:descope/descope-auth0-migration.git
```

3. Create a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

4. Install the Necessary Python libraries

```
pip3 install -r requirements.txt
```

5. Setup Your Environment Variables

You can change the name of the `.env.example` file to `.env` to use as a template.

```
AUTH0_TOKEN=Your_Auth0_Token // Required, this is generated within Auth0
AUTH0_TENANT_ID=Your_Auth0_Tenant_ID // Required, this is the tenant ID of your tenant within Auth0
DESCOPE_PROJECT_ID=Your_Descope_Project_ID // Required, this is your Descope ProjectId
DESCOPE_MANAGEMENT_KEY=Your_Descope_Project_ID // Required, this is your Descope Management Key
```

a. To get an Auth0 token, go [here](https://manage.auth0.com/#/apis/management/explorer), then copy the token to your
`.env` file. These tokens are only valid for 24 hours by default.

b. To get your Auth0 Tenant ID, it can be found in the URL of your Auth0 dashboard. For example, when you login to Auth0, your URL might look something like this:

```
https://manage.auth0.com/dashboard/us/dev-xyz/
```

Your tenant ID is: `dev-xyz`. You can also read more about it [here](https://auth0.com/docs/get-started/tenant-settings/find-your-tenant-name-or-tenant-id).

c. To get your Descope Project ID, go [here](https://app.descope.com/settings/project), then copy the project ID to your
`.env` file.

d. To create a Descope Management Key, go [here](https://app.descope.com/settings/company/managementkeys), then copy
the token to your `.env` file.

6. The tool depends on a few custom user attributes that will automatically be created for you. The below outlines the machine names of the attributes created within the [user's custom attributes](https://app.descope.com/users/attributes) section of the Descope console.

- `connection` (type: text): This custom attribute will contain the different connection types associated to the user which was
  migrated from Auth0.
- `freshlyMigrated` (type: Boolean): This custom attribute will be set to true during the migration. This allows for you
  to later check this via a conditional during Descope flow execution.

Once you've set all of that up, you're ready to run the script.

## Running the Migration Script 🚀

### Options

You can run the script to capture the users from the Auth0 database via API, or you can utilize it to fetch users from an exported file.

The below options show the example commands for fetching users from the Auth0 database via API; however, there is a 1000 user limitation from the Auth0 user API. So it is recommended to export a JSON of users if you have more than 1000 users. In order to export the JSON, follow [these steps](https://auth0.com/docs/customize/extensions/user-import-export-extension#export-users).

Then when running the migration script, use the additional flag of `-from-json ./path_to_user_export.json`

Examples:
```
Dry run with passwords: python3 src/main.py --from-json ./path_to_user_export.jso --with-passwords ./path_to_exported_password_users_file.json

Dry run without passwords: python3 src/main.py --from-json ./path_to_user_export.jso

Live run with passwords: python3 src/main.py --from-json ./path_to_user_export.jso --with-passwords ./path_to_exported_password_users_file.json

Live run without passwords: python3 src/main.py --from-json ./path_to_user_export.jso
```

You can use the `-v` or `--verbose` flags to enable more detailed output. This works for both live and dry runs, providing you with additional information.

### Dry run

You can dry run the migration script which will allow you to see the number of users, tenants, roles, etc which will be migrated
from Auth0 to Descope.

#### With Passwords

```
python3 src/main.py --dry-run --with-passwords ./path_to_exported_password_users_file.json
```

The output would appear similar to the following:

```
Running with passwords from file: ./path_to_exported_users_file.json
Would migrate 2 users from Auth0 with Passwords to Descope
Would migrate 112 users from Auth0 to Descope
Would migrate 2 roles from Auth0 to Descope
Would migrate MyNewRole with 2 associated permissions.
Would migrate Role with 0 associated permissions.
Would migrate 2 organizations from Auth0 to Descope
Would migrate Tenant 1 with 5 associated users.
Would migrate Tenant 2 with 4 associated users.
```

#### Without Passwords

```
python3 src/main.py --dry-run
```

The output would appear similar to the following:

```
Would migrate 112 users from Auth0 to Descope
Would migrate 2 roles from Auth0 to Descope
Would migrate MyNewRole with 2 associated permissions.
Would migrate Role with 0 associated permissions.
Would migrate 2 organizations from Auth0 to Descope
Would migrate Tenant 1 with 5 associated users.
Would migrate Tenant 2 with 4 associated users.
```

### Live run

#### With Passwords

To migrate your Auth0 users, simply run the following command:

```
python3 src/main.py --with-passwords ./path_to_exported_password_users_file.json
```

The output will include the responses of the created users, organizations, roles, and permissions as well as the mapping between the various objects within Descope:

The output will include the responses of the created users, organizations, roles, and permissions as well as the mapping between the various objects within Descope. A log file will also be generated in the format of `migration_log_%d_%m_%Y_%H:%M:%S.log`. Any items which failed to be migrated will also be listed with the error that occurred during the migration.

```
Running with passwords from file: ./path_to_exported_users_file.json
Starting migration of 2 users from Auth0 password file
Starting migration of 112 users found via Auth0 API
Still working, migrated 10 users.
...
Still working, migrated 110 users.
Starting migration of 2 roles found via Auth0 API
Starting migration of MyNewRole with 2 associated permissions.
Starting migration of Role with 0 associated permissions.
=================== Password User Migration ====================
Auth0 Users password users in file 2
Successfully migrated 2 users
Created users within Descope 2
=================== User Migration =============================
Auth0 Users found via API 112
Successfully migrated 110 users
Successfully merged 2 users
Users migrated, but disabled due to one of the merged accounts being disabled 1
Users disabled due to one of the merged accounts being disabled ['auth0|653c1bf0398960f19a6d8171']
Failed to migrate 2
Users which failed to migrate:
facebook|122094272078100956 Reason: {"errorCode":"E011002","errorDescription":"Request is missing required arguments","errorMessage":"Missing email or phone","message":"Missing email or phone"}
facebook|10226222057950897 Reason: {"errorCode":"E011002","errorDescription":"Request is missing required arguments","errorMessage":"Missing email or phone","message":"Missing email or phone"}
Created users within Descope 108
=================== Role Migration =============================
Auth0 Roles found via API 2
Successfully migrated 2 roles
Created roles within Descope 2
=================== Permission Migration =======================
Auth0 Permissions found via API 2
Successfully migrated 2 permissions
Created permissions within Descope 2
=================== User/Role Mapping ==========================
Successfully role and user mapping
Mapped 1 user to MyNewRole
Mapped 2 user to Role
=================== Tenant Migration ===========================
Auth0 Tenants found via API 2
Successfully migrated 2 tenants
=================== User/Tenant Mapping ========================
Successfully tenant and user mapping
Associated 5 users with tenant: Tenant 1
Associated 4 users with tenant: Tenant 2
```


#### Without Passwords

To migrate your Auth0 users, simply run the following command:

```
python3 src/main.py
```

The output will include the responses of the created users, organizations, roles, and permissions as well as the mapping between the various objects within Descope:

The output will include the responses of the created users, organizations, roles, and permissions as well as the mapping between the various objects within Descope. A log file will also be generated in the format of `migration_log_%d_%m_%Y_%H:%M:%S.log`. Any items which failed to be migrated will also be listed with the error that occurred during the migration.

```
Starting migration of 112 users found via Auth0 API
Still working, migrated 10 users.
...
Still working, migrated 110 users.
Starting migration of 2 roles found via Auth0 API
Starting migration of MyNewRole with 2 associated permissions.
Starting migration of Role with 0 associated permissions.
=================== User Migration =============================
Auth0 Users found via API 112
Successfully migrated 110 users
Successfully merged 2 users
Users migrated, but disabled due to one of the merged accounts being disabled 1
Users disabled due to one of the merged accounts being disabled ['auth0|653c1bf0398960f19a6d8171']
Failed to migrate 2
Users which failed to migrate:
facebook|122094272078100956 Reason: {"errorCode":"E011002","errorDescription":"Request is missing required arguments","errorMessage":"Missing email or phone","message":"Missing email or phone"}
facebook|10226222057950897 Reason: {"errorCode":"E011002","errorDescription":"Request is missing required arguments","errorMessage":"Missing email or phone","message":"Missing email or phone"}
Created users within Descope 108
=================== Role Migration =============================
Auth0 Roles found via API 2
Successfully migrated 2 roles
Created roles within Descope 2
=================== Permission Migration =======================
Auth0 Permissions found via API 2
Successfully migrated 2 permissions
Created permissions within Descope 2
=================== User/Role Mapping ==========================
Successfully role and user mapping
Mapped 1 user to MyNewRole
Mapped 2 user to Role
=================== Tenant Migration ===========================
Auth0 Tenants found via API 2
Successfully migrated 2 tenants
=================== User/Tenant Mapping ========================
Successfully tenant and user mapping
Associated 5 users with tenant: Tenant 1
Associated 4 users with tenant: Tenant 2
```

### Post Migration Verification

Once the migration tool has ran successfully, you can check the [users](https://app.descope.com/users),
[roles](https://app.descope.com/authorization), [permissions](https://app.descope.com/authorization/permissions),
and [tenants](https://app.descope.com/tenants) for the migrated items from Auth0. You can verify the created items
based on the output of the migration tool.

## Testing 🧪

Unit testing can be performed by running the following command:

```
python3 -m unittest tests.test_migration
```

## Issue Reporting ⚠️

For any issues or suggestions, feel free to open an issue in the GitHub repository.

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.
