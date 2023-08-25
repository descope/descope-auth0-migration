# Descope Auth0 Migration Tool

This repository includes a python utility for migrating your Auth0 users to Descope.

## Setup 💿

1. To export hashed password from Auth0, open a [ticket](https://support.auth0.com/tickets) with Auth0 support to
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

4. Setup Your Environment Variables

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
https://manage.auth0.com/dashboard/us/dev-zx7jen5gbxsfdsr/
```

Your tenant ID is: `dev-zx7jen5gbxsfdsr`. You can also read more about it [here](https://auth0.com/docs/get-started/tenant-settings/find-your-tenant-name-or-tenant-id).

c. To get your Descope Project ID, go [here](https://app.descope.com/settings/project), then copy the token to your
`.env` file.

d. To create a Descope Management Key, go [here](https://app.descope.com/settings/company/managementkeys), then copy
the token to your `.env` file.

Once you've set all of that up, you're ready to run the script.

## Running the Migration Script 🚀

To migrate your Auth0 users, simply run the following command:

```
python3 src/main.py path_to_password_hash_export/file.json
```

The output will include the responses of the created users within Descope:

```
User successfully created
{"user":{"loginIds":["app@example.com"], "userId":"U2UTvKxVuf4xYe68xYBK2FtFEuTK", "name":"app@example.com", "email":"app@example.com", "phone":"", "verifiedEmail":false, "verifiedPhone":false, "roleNames":[], "userTenants":[], "status":"invited", "externalIds":["app@example.com"], "picture":"", "test":false, "customAttributes":{"auth0UserId":"64de73a2b160e31c8c3579b7"}, "createdTime":1692976324, "TOTP":false, "SAML":false, "OAuth":{}}}
...
```

## Testing 🧪

Unit testing can be performed by running the following command:

```
python3 -m unittest tests.test_migration
```

## Issue Reporting ⚠️

For any issues or suggestions, feel free to open an issue in the GitHub repository.

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.
