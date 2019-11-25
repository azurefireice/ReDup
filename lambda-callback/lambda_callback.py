from typing import Optional, Any, Dict

import requests


def lambda_handler(event, context) -> Dict[str, Any]:
    """Obtains user access token from GitHub
     and creates a copy of provided repository to a user authenticated with provided token
    """
    print("event: ", event)
    try:
        code = event["queryStringParameters"]["code"]
    except KeyError:
        code = None

    if not code:
        return respond_failure(f"No code provided to obtain GitHub oauth token.")

    try:
        token = get_user_access_token(code)
        create_repo(token)
    except AccessTokenError as err:
        return respond_failure(f"Failure while obtaining GitHub user token. Code: {err.code}, Reason: {err.message}")
    except RepositoryCreationError as err:
        return respond_failure(
            f"Failure while creating GitHub repository copy. Code: {err.code}, Reason: {err.message}")

    return respond_success()


def get_user_access_token(code: str) -> str:
    """Obtains user access token from GitHub"""
    json_body = {
        "client_id": "fd6f4a7813e39f0ee022",
        "client_secret": "446091d75336c9546f9f10f626fa51e1dba97665",
        "code": code
    }
    resp = requests.post("https://github.com/login/oauth/access_token", json=json_body,
                         headers={"Accept": "application/json"})
    resp_json = resp.json()
    print("get user token response json: ", resp_json)
    if resp.status_code != 200:
        print(f"Failure with code: {resp.status_code} and reason: {resp_json['error']}")
        raise AccessTokenError(resp.status_code, f"Github http error: {resp_json['error']}")

    if resp_json.get("error", ""):
        print(f"Failure with error: {resp_json['error']}")
        raise AccessTokenError(400, f"GitHub response error: {resp_json['error_description']}")

    return resp_json["access_token"]


def create_repo(token: str) -> None:
    """Creates copy of this application's repository for a user with provided authentication token.
    repository creation currently requires custom "preview" header in request, as this is a preview feature from github.
    """
    template_owner = "azurefireice"
    template_repo = "ReDup"
    url = f"https://api.github.com/repos/{template_owner}/{template_repo}/generate"
    params = {"access_token": token}
    headers = {"Accept": "application/json, application/vnd.github.baptiste-preview+json"}
    body = {
        "name": "ReDup",
        "description": "An instance of repository copied by ReDup ©2019 Andrii Gryshchenko."
                       " For more details please see https://github.com/azurefireice/ReDup."
    }
    print(f"Making request to {url} with params: token, headers: {headers}, body: {body}")
    resp = requests.post(url=url, json=body, params=params, headers=headers)
    resp_json = resp.json()
    print("create repo response json: ", resp_json)
    if resp.status_code == 422:
        raise DuplicateRepositoryError(resp.status_code, f"We have likely already created a repository for you,"
                                                         f" as the repository with our name already"
                                                         f" exists on your profile. Check it out.")

    if resp.status_code == 404:
        raise RepositoryNotFoundError(resp.status_code, f"Seems like we can't find a repository to copy to you."
                                                        f" Retrying will probably not help,"
                                                        f" unless you let us know of the issue.")
    if resp.status_code != 201:
        raise RepositoryCreationError(resp.status_code, f"Failure: {resp_json['errors']}")


class GithubError(Exception):
    """Generic exception raised for errors while communicating with GitHub

    Attributes:
        code -- code associated with error
        message -- explanation of the error
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class AccessTokenError(GithubError):
    """Exception raised while trying to get user access token from GitHub"""
    pass


class RepositoryCreationError(GithubError):
    """Exception raised while trying to copy repository to user's GitHub"""
    pass


class DuplicateRepositoryError(RepositoryCreationError):
    """Exception raised if a user already has the repository with the same naming as we are trying to create."""
    pass


class RepositoryNotFoundError(RepositoryCreationError):
    """Exception raised if we can't find source(template) repository to copy to a user."""
    pass


def respond_success() -> Dict[str, Any]:
    return respond(None, "We have successfully copied our repository to your account! Enjoy!")


def respond_failure(msg: str) -> Dict[str, Any]:
    return respond(msg)


def respond(error_msg: Optional[str], res: Optional[str] = None) -> Dict[str, Any]:
    return {
        "statusCode": "400" if error_msg else "200",
        "body": error_msg if error_msg else res,
        "headers": {
            "Content-Type": "application/json",
        },
    }
