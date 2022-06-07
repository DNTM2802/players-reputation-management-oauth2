import re


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
