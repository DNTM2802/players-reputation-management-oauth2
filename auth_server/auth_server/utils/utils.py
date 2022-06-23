import json
import re
import urllib

import requests
from django.contrib.auth.hashers import make_password


def pop_scopes(token, request_type):
    """
    Used to pop reputation read ('read_*') and write ('write')
    scopes of a token upon their usage, in order to limit the
    token usage to 1 write and 1 read only.

    :param token: OAuth2 token model
    :param request_type: "GET" or "POST"
    :return: list containing the popped scopes from the token
    """

    read_regex = re.compile("read_([2-9]|10)")
    token_scopes = token.scope.split(' ')
    popped_scopes = []

    # If GET, pop all 'read_*' scopes from token
    if request_type == "GET":
        new_scopes = []
        for scope in token_scopes:
            if read_regex.match(scope):
                popped_scopes.append(scope)
            else:
                new_scopes.append(scope)
        token.scope = ' '.join(new_scopes)
        token.save()
        return popped_scopes

    # If POST, pop 'write' scope from token
    elif request_type == "POST":
        if 'write' in token_scopes:
            token_scopes.remove('write')
            token.scope = ' '.join(token_scopes)
            token.save()
            return ['write']
        else:
            return []


def retrieve_and_transform_resource(cmd_oauth2_token):
    """
    Retrieves a transformation of the protected resource from the Autenticacao.gov OAuth2
    provider, according to the documentation in https://github.com/amagovpt/doc-AUTENTICACAO

    :param cmd_oauth2_token: Autenticacao.gov OAuth2 token
    :return: Citizen ID Number transformed with PBKDF2 function. None in case of any problem.
    """

    cmd_attribute_manager_url = 'https://preprod.autenticacao.gov.pt/oauthresourceserver/api/AttributeManager'

    # Ask CMD oauthresourceserver for authenticationContextId
    try:
        body_json = {"token": cmd_oauth2_token, "attributesName": ["http://interop.gov.pt/MDC/Cidadao/NIC"]}
        attribute_manager_request = requests.post(cmd_attribute_manager_url, json=body_json)
        authenticationContextId = json.loads(attribute_manager_request.text)["authenticationContextId"]

        # Use oauth2 token and authenticationContextId to retrieve resources
        params = {'token': cmd_oauth2_token, 'authenticationContextId': authenticationContextId}
        resources_url = cmd_attribute_manager_url + '?' + urllib.parse.urlencode(params)
        resources_request = requests.get(resources_url)
        user_nic = json.loads(resources_request.text)[0]["value"]
    except Exception as e:
        return None

    # One-way expensive transformation
    user_nic_pbkdf2 = make_password(user_nic, hasher='pbkdf2_sha256', salt='1AAF047H3W1N')

    return user_nic_pbkdf2
