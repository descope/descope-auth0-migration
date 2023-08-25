import json
import os
import requests
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

"""Load and read environment variables from .env file"""
load_dotenv()
AUTH0_TOKEN = os.getenv("AUTH0_TOKEN")
AUTH0_TENANT_ID = os.getenv("AUTH0_TENANT_ID")
DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
DESCOPE_MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")


def read_auth0_export(file_path):
    """
    Read and parse the Auth0 export file formatted as NDJSON.

    Args:
    - file_path (str): The path to the Auth0 export file.

    Returns:
    - list: A list of parsed Auth0 user data.
    """
    with open(file_path, "r") as file:
        data = [json.loads(line) for line in file]
    return data


def fetch_auth0_users():
    """
    Fetch and parse Auth0 users from the provided endpoint.

    Returns:
    - list: A list of parsed Auth0 users if successful, empty list otherwise.
    """
    headers = {"Authorization": f"Bearer {AUTH0_TOKEN}"}
    response = requests.get(
        f"https://{AUTH0_TENANT_ID}.us.auth0.com/api/v2/users", headers=headers
    )

    if response.status_code != 200:
        logging.error(
            f"Error fetching Auth0 users. Status code: {response.status_code}"
        )
        return []

    return response.json()


def handle_password(user):
    """
    Extract password details from the user's password hash.

    Args:
    - user (dict): A dictionary containing user details.

    Returns:
    - dict: A dictionary containing password details.
    """
    pw_hash = user["passwordHash"].split("$")
    pw_details = {
        "encryptionScheme": "bcrypt",
        "factor": int(pw_hash[2]),
        "salt": pw_hash[3][:22],
        "password": pw_hash[3][22:],
    }


def create_descope_user(user, matched_user):
    """
    Create a Descope user based on matched Auth0 user data.

    Args:
    - user (dict): A dictionary containing user details from the Auth0 export file.
    - matched_user (dict): A dictionary containing user details fetched from Auth0 API.
    """
    # password_stuff = handle_password(user)
    # this doesn't include phone as it's not within the output from Auth0, but may be later
    payload_data = {
        "loginId": matched_user["email"],
        "email": matched_user["email"],
        "verifiedEmail": matched_user["email_verified"],
        "displayName": matched_user["name"],
        "invite": False,
        "test": False,
        "customAttributes": {
            "nickname": matched_user["nickname"],
            "auth0UserId": matched_user["user_id"].split("|")[-1],
        },
        "picture": matched_user["picture"],
    }
    payload = json.dumps(payload_data)

    # Endpoint
    url = "https://api.descope.com/v1/mgmt/user/create"

    # Headers
    headers = {
        "Authorization": f"Bearer {DESCOPE_PROJECT_ID}:{DESCOPE_MANAGEMENT_KEY}",
        "Content-Type": "application/json",
    }
    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        logging.error(f"Unable to create user.  Status code: {response.status_code}")
    else:
        logging.info("User successfully created")
        logging.info(response.text)


def process_users(exported_users, api_response_users):
    """
    Process the list of users from Auth0 by mapping and creating them in Descope.

    Args:
    - exported_users (list): A list of users from the Auth0 export file.
    - api_response_users (list): A list of users fetched from Auth0 API.
    """
    api_user_map = {
        api_user["user_id"].split("|")[-1]: api_user for api_user in api_response_users
    }
    for user in exported_users:
        user_id = user["_id"]["$oid"]

        matched_user = api_user_map.get(user_id)
        if matched_user:
            create_descope_user(user, matched_user)
        else:
            logging.error(f"No match found for user_id: {user_id}")
