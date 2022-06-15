import json
from random import randint
import os

os.environ.setdefault('TM_APPLICATION_CLIENT_ID', '7PX424fslBn2LZ7qWtd34Kog0VjWTSIVci16xA9R')
os.environ.setdefault('TM_APPLICATION_CLIENT_SECRET',
                      'MSbi0l3apzI5DHtFNEBdntkmzccAb7vO2ZANej2irDEiaTUfEvAb1VBUrfYUaghf5TKNypl5zU69a2EcyVUGil10Utq8qtkjFJyH47KsjnJDSEFQo971ZgWPEbRzjBd1')
os.environ.setdefault('TM_APPLICATION_REDIRECT_URI', 'http://0.0.0.0:8001/exchange')

from django.conf import settings

settings.configure()
from django.contrib.auth.hashers import make_password

data_to_txt = ""

pks = [i + 1 for i in range(18)]
nics = [str(randint(10000000, 99999999)) for _ in range(18)]
skills = [randint(-10, 20) for _ in range(18)]
behaviours = [randint(-10, 20) for _ in range(18)]
logins = [["quickvictorious", "5W3jCJwM"],
          ["thriftwrithe", "F2QzpTxy"],
          ["insidiousexaggerate", "BFMqK2xW"],
          ["rnawild", "rnHNXz45"],
          ["mournernautilus", "xTvMts74"],
          ["alongsat", "uVB6Qxda"],
          ["solvesalesman", "7Zvw4MeT"],
          ["bozohuh", "vN2Lppfa"],
          ["dugoutbrag", "d7dRzURL"],
          ["mosquitoefleet", "9eGZSuLj"],
          ["clowntransparent", "Seych9gF"],
          ["wheelhouseinstruct", "wD8AErCD"],
          ["arraypair", "WVvSxM5e"],
          ["tabooregister", "S2GtyJDE"],
          ["adorablepig", "2xX5AzUx"],
          ["anxietyremaining", "9YQ3LfjY"],
          ["tibiafirst", "RG2cL8bF"],
          ["oceansquawk", "k6P897mB"]
          ]

final_list = []

data_to_txt += "## PLAYERS ##\n\n"

for p in range(18):
    template = json.loads(
        '{"model":"accounts.player","pk":7,"fields":{"password":"pbkdf2_sha256$320000$kTKsx6gVOPk2jPMJ0U7MP4$7go4N4GqEFt9E87DlL16mtAf6dr8M9fTg6aZEcA0C94=","last_login":"2022-06-15T15:48:09.089Z","is_superuser":false,"username":"duarte","first_name":"","last_name":"","email":"","is_staff":false,"is_active":true,"date_joined":"2022-06-15T15:48:08.797Z","nic":"pbkdf2_sha256$320000$1AAF047H3W1N$/jaQfDph6WuEDpMsEaxncX+xLxbbXrqNtqR9m1QrflI=","skill":0,"behaviour":0,"auth_status":"CMD","groups":[],"user_permissions":[]}}')
    template["pk"] = pks[p]
    template["fields"]["password"] = make_password(logins[p][1], hasher='pbkdf2_sha256', salt='1AAF047H3W1N')
    template["fields"]["is_superuser"] = False
    template["fields"]["username"] = logins[p][0]
    template["fields"]["nic"] = make_password(nics[p], hasher='pbkdf2_sha256', salt='1AAF047H3W1N')
    template["fields"]["skill"] = skills[p]
    template["fields"]["behaviour"] = behaviours[p]
    template["fields"]["auth_status"] = "NULL"
    final_list.append(template)

    data_to_txt += f"username: {logins[p][0]}\n"
    data_to_txt += f"nic: {nics[p]}\n"
    data_to_txt += f"password: {logins[p][1]}\n\n"

template = json.loads(
    '{"model":"accounts.player","pk":7,"fields":{"password":"pbkdf2_sha256$320000$kTKsx6gVOPk2jPMJ0U7MP4$7go4N4GqEFt9E87DlL16mtAf6dr8M9fTg6aZEcA0C94=","last_login":"2022-06-15T15:48:09.089Z","is_superuser":false,"username":"duarte","first_name":"","last_name":"","email":"","is_staff":false,"is_active":true,"date_joined":"2022-06-15T15:48:08.797Z","nic":"pbkdf2_sha256$320000$1AAF047H3W1N$/jaQfDph6WuEDpMsEaxncX+xLxbbXrqNtqR9m1QrflI=","skill":0,"behaviour":0,"auth_status":"CMD","groups":[],"user_permissions":[]}}')
template["pk"] = 0
template["fields"]["password"] = make_password("Cda77Hg26ABsKy7K", hasher='pbkdf2_sha256', salt='1AAF047H3W1N')
template["fields"]["is_superuser"] = True
template["fields"]["is_staff"] = True
template["fields"]["username"] = "admin"
template["fields"]["nic"] = make_password("00000000", hasher='pbkdf2_sha256', salt='1AAF047H3W1N')
template["fields"]["skill"] = 0
template["fields"]["behaviour"] = 0
template["fields"]["auth_status"] = "NULL"
final_list.append(template)

f = open("code/fixtures/player.json", "w")
f.write(json.dumps(final_list, indent=4))
f.close()

data_to_txt += "--------------------\n\n"
data_to_txt += "## OAUTH2 APPLICATIONS ##\n\n"

final_list = []
template = json.loads(
    '{"model":"oauth2_provider.application","pk":1,"fields":{"client_id":"","user":0,"redirect_uris":"","client_type":"confidential","authorization_grant_type":"authorization-code","client_secret":"","name":"Tables\' Manager","skip_authorization":false,"created":"2022-06-15T17:15:59.817Z","updated":"2022-06-15T17:15:59.817Z","algorithm":""}}')
template["fields"]["client_id"] = os.environ.get('TM_APPLICATION_CLIENT_ID')
template["fields"]["client_secret"] = os.environ.get('TM_APPLICATION_CLIENT_SECRET')
template["fields"]["redirect_uris"] = os.environ.get('TM_APPLICATION_REDIRECT_URI')
final_list.append(template)

f = open("code/fixtures/application.json", "w")
f.write(json.dumps(final_list, indent=4))
f.close()

data_to_txt += "name: Tables\' Manager\n"
data_to_txt += f"client_id: {os.environ.get('TM_APPLICATION_CLIENT_ID')}\n"
data_to_txt += f"client_secret: {os.environ.get('TM_APPLICATION_CLIENT_SECRET')}\n"
data_to_txt += f"redirect_uris: {os.environ.get('TM_APPLICATION_REDIRECT_URI')}\n"

f = open("code/data.txt", "w")
f.write(data_to_txt)
f.close()

