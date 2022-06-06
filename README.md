# players-reputation-management-oauth2

## OAuth2-Resource Server
Authorization endpoint example:
```
http://localhost:8000/o/authorize?state=random_state_string&client_id=7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R&response_type=code&scope=read_3%20write
```
`client_id` asks for an authorization grant to read player's reputation with level 3 of anonymity and to write player's reputation.

When an Access Token is provided for the above grant, it has the following constraints:
- Can be used to read a player's reputation with level 3 of anonymity through a GET request to `http://<auth-resource-server>/api/reputation`
- Can be used to write a player's reputation through a POST request to `http://{auth-resource-server}/api/reputation` with a JSON body according to the following representation: `{'skill_update':<int>,'behaviour_update':<int>}`
- It can only be used once to read the reputation and once to write it.

If some of the above constraints are not met, the auth-resource server responds with an appropriate HTTP code and a JSON with some feedback.
