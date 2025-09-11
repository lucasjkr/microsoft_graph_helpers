import json, logging, requests
from .core import get_headers, make_graph_api_request

def verify_user_exists(bearer_token, user_principal_name):
    logging.debug(f"Querying Microsoft Graph for user {user_principal_name}")
    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}"
    headers = get_headers(bearer_token)

    response = make_graph_api_request(
        method="GET",
        url=url,
        headers=headers,
        context="verify_user_exists"
    )

    if response is False:
        logging.debug("User not found.")
        return False
    else:
        return True


def revoke_ms_sessions(bearer_token, user_principal_name):
    logging.debug(f"Revoking sign-in sessions for {user_principal_name}")

    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/revokeSignInSessions"
    headers = get_headers(bearer_token)

    response = make_graph_api_request(
        method="POST",
        url=url,
        headers=headers,
        context="revoke_ms_sessions"
    )

    if response is False:
        logging.debug(f"revoke_ms_sessions for {user_principal_name} failed.")
        return False
    return True


def reset_ms_password(bearer_token, user_principal_name, password):
    logging.debug(f"Resetting password for {user_principal_name}")

    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}"
    headers = get_headers(bearer_token)
    headers.update({'Accept': "application/json"})

    payload = {
        'passwordProfile': {
            'forceChangePasswordNextSignIn': False,
            'password': password
        }
    }

    response = make_graph_api_request(
        method="PATCH",
        url=url,
        headers=headers,
        payload=payload,
        context="reset_ms_password"
    )

    return response is not False


def get_user_direct_group_memberships(bearer_token, user_principal_name):
    logging.debug(f"Fetching group memberships for {user_principal_name}")

    url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/memberOf"
    headers = get_headers(bearer_token)

    response = make_graph_api_request(
        method="GET",
        url=url,
        headers=headers,
        context="get_user_direct_group_memberships"
    )

    return response if isinstance(response, dict) else False
