# players-reputation-management-oauth2

## Run the whole project
You will have to run the 3 separate projects in order to interact with the whole project.

Start by running the OAuth2-Resource Server, by executing the following commands in a new terminal:
```
cd auth-server/auth_server
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py loaddata fixtures/player.json --app accounts.player
python3 manage.py loaddata fixtures/application.json --app oauth2_provider.application
python3 manage.py runserver 8000
```
The above commands create a Python virtual environment, install the requirements in it, populate the database with initial test data and run the project in the port 8000. You can access the OAuth2-Resource Server web interface in http://127.0.0.1:8000.

In the file `data.txt` you can find the credentials for the test users and the credentials for the admin user. If you want to interact with the admin panel, you can go to http://127.0.0.1:8000/admin. The admin panel allows to manipulate users directly, as well as manipulate OAuth2.0 tokens, applications and so on.

Now, you can run the Tables Matchmaker and the Match Manager. Start a new terminal and run the below commands:
```
cd tables_matchmaker
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
With the virtual environment created and the requirements installed, you will now have to run a docker container, which will work as a cache database for the Django Channels (websockets) module:
```
docker run -p 6379:6379 -d redis:5
```
Now, in a new terminal, run the Django Channels worker:
```
cd tables_matchmaker
source venv/bin/activate
python3 manage.py runworker channels --settings=tables_matchmaker.settings -v2
```
And finally, run the TM application:
```
cd tables_matchmaker
source venv/bin/activate
daphne tables_matchmaker.asgi:application --port 8002 --bind 127.0.0.1 -v2
```

The Tables Matchmaker web interface will be now available in port 8002. **You are not supposed to access this interface directly**. To interact with it, you will need to run the User Agent in a new terminal:
```
cd user_agent
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 run.py
```
The User Agent web interface will be available in http://127.0.0.1:8003. You should access it if you want to play a game.

## OAuth2-Resource Server usage
You may want to interact with the OAuth2-Resource Server without the given application (Tables Matchmaker). For that, the API description is below.
### Usage example
Authorization endpoint example:
```
http://localhost:8000/o/authorize?state=random_state_string&client_id=7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R&response_type=code&scope=read_3%20write
```
`client_id` asks for an authorization grant to read player's reputation with level 3 of anonymity and to write player's reputation. The above `client_id` is the TM, but you can create a new application by accessing the Admin panel in http://127.0.0.1:8000/admin with the Admin credentials in `auth-server/auth_server/data.txt`.

When an Access Token is provided for the above grant, it has the following constraints:
- It is provided by including the `Authorization` header in the request, with the value `Bearer {TOKEN}`
- Can be used to read a player's reputation with level 3 of anonymity through a GET request to `http://127.0.0.1:8000/api/reputation`. Example using curl:
```
curl --location --request GET 'http://127.0.0.1:8000/api/reputation' \
--header 'Authorization: Bearer ZNwbH3eMlViBHWahbVlkGWtPH6DgsO'
```
- Can be used to write a player's reputation through a POST request to `http://127.0.0.1:8000/api/reputation` with a JSON body according to the following representation: `{'skill_update':<int>,'behaviour_update':<int>}`. Example using curl:
```
curl --location --request POST 'http://127.0.0.1:8000/api/reputation' \
--header 'Authorization: Bearer ZNwbH3eMlViBHWahbVlkGWtPH6DgsO' \
--header 'Content-Type: application/json' \
--data-raw '{"skill_update":2,"behaviour_update":3}'
```
- It can only be used once to read the reputation and once to write it.

If some of the above constraints are not met, the auth-resource server responds with an appropriate HTTP code and a JSON with some feedback.
