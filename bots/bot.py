import requests
from requests_html import HTMLSession
import asyncio
from websockets import connect

client = requests.session()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,gl;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'http://localhost:8000',
    'Referer': 'http://localhost:8000/o/authorize/?response_type=code&client_id=7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R&state=random_state_string&scope=read_2%20write',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'response_type': 'code',
    'client_id': '7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R',
    'state': 'random_state_string',
    'scope': 'read_2 write',
}

TM = "http://localhost:8002"

# DOES USER AGENT REQUEST
playgame = client.get(
    f"{TM}/play_game?game=peixinho&skill=eq&behaviour=eq&granularity=2&return=http://localhost:8003/match"
)

browser_csrftoken = playgame.cookies.items()[0][1]

login_form_csrftoken = str(
    playgame.content.split(b'name="csrfmiddlewaretoken" value="')[1].split(b'"')[0],
    "utf-8",
)

headers = {"User-Agent": "Mozilla/5.0"}
payload = {
    "username": "robert",
    "password": "6HaQgt4v8Leabr9",
    "csrfmiddlewaretoken": login_form_csrftoken,
}
cookies = {"csrftoken": browser_csrftoken}
cookies['TMSESSIONS'] = playgame.request.headers["Cookie"].split("TMSESSIONS=")[1]

# SUBMITS LOGIN FORM
login = client.post(playgame.url, headers=headers, data=payload, cookies=cookies)

authorize_form_csrftoken = str(
    login.content.split(b'name="csrfmiddlewaretoken" value="')[1].split(b'"')[0],
    "utf-8",
)

redirect_uri = f"{TM}/exchange/"
scope = "read_2 write"
client_id = "7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R"
state = "random_state_string"
response_type = "code"

data = {
    "csrfmiddlewaretoken": f"{authorize_form_csrftoken}",
    "redirect_uri": f"{redirect_uri}",
    "scope": f"{scope}",
    "nonce": "",
    "client_id": f"{client_id}",
    "state": "random_state_string",
    "response_type": "code",
    "code_challenge": "",
    "code_challenge_method": "",
    "claims": "",
    "allow": "Authorize",
}

browser_csrftoken = login.cookies.items()[0][1]

sessionid_cookie = login.request.headers["Cookie"].split("sessionid=")[-1]
messages_cookie = login.request.headers["Cookie"].split("messages=")[1].split(";")[0]

cookies = {
    "csrftoken": f"{browser_csrftoken}",
    "sessionid": f"{sessionid_cookie}",
    "messages": f"{messages_cookie}",
    "TMSESSIONS": playgame.request.headers["Cookie"].split("TMSESSIONS=")[1]
}

## SUBMITS AUTHORIZE PAGE FORM

response = client.post('http://localhost:8000/o/authorize/', headers=headers, params=params, data=data, cookies=cookies)

## response has room
response = client.get(response.url)

html_sess = HTMLSession()
resp = html_sess.get(response.url)

# resp.html.find('#myElementID').text

roomid = response.url[-6]


async def connect(uri):
    async with connect(uri) as websocket:
        await websocket.recv()


asyncio.run(connect(f"ws://localhost:8002/ws/matchmaker/{roomid}"))
