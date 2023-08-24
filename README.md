# Welcome to the Descope Auth0 Migration Tool

This repository includes a python utility for migrating your Auth0 users to Descope.

## Setup

1. To export hashed password from Auth0, open a [ticket](https://support.auth0.com/tickets) with Auth0 support to
request an export of your user's password hashes.

2. Clone the repo:

```
git clone git@github.com:descope/descope-auth0-migration.git
```

3. Ensure you have the necessary Python libraries

pip
```
pip install json os requests python-dotenv
```

pip3
```
pip install json os requests python-dotenv
```

4. Setup your environment variables within the `.env` file

```
AUTH0_TOKEN=Your_Auth0_Token // Required, this is generated within Auth0
AUTH0_TENANT_ID=Your_Auth0_Tenant_ID // Required, this is the tenant ID of your tenant within Auth0
DESCOPE_PROJECT_ID=Your_Descope_Project_ID // Required, this is your Descope ProjectId
DESCOPE_MANAGEMENT_KEY=Your_Descope_Project_ID // Required, this is your Descope Management Key
```

To get an Auth0 token, go [here](https://manage.auth0.com/#/apis/management/explorer), then copy the token to your
`.env` file. These tokens are only valid for 24 hours by default.

To get your Descope Project ID, go [here](https://app.descope.com/settings/project), then copy the token to your
`.env` file.

To create a Descope Management Key, go [here](https://app.descope.com/settings/company/managementkeys), then copy
the token to your `.env` file.

5. Run the script

python
```
python descope_auth0_migration.py path_to_password_hash_export/file.json
```


python3
```
python3 descope_auth0_migration.py path_to_password_hash_export/file.json
```

The output will include the responses of the created users within Descope.