import json
import requests
import string

uri = 'https://api.football-data.org/v4/'
headers = { 'X-Auth-Token': '09158fc8680949dd8c7cb4644d5ee282' }

def chooseTeam():
    uri_t = uri + "teams?limit=200"
    name = input("검색하고자 하는 팀 이름을 입력하세요: ")
    response = requests.get(uri_t, headers=headers)
    for teams in response.json()['teams']:
        if name == teams['name']:
            uri_s = uri + "teams/" + str(teams['id'])
            response = requests.get(uri_s, headers=headers)
            print(response.json())
    

chooseTeam()

