import json
import requests

uri = 'https://api.football-data.org/v4/'
headers = { 'X-Auth-Token': '09158fc8680949dd8c7cb4644d5ee282' }

def main():
    select = input("리그 검색: 1, 팀 검색: 2, 선수 검색: 3\n")
    
    if select == '1':
        chooseLeague()
    elif select == '2':
        chooseTeam()
    elif select == '3':
        choosePerson()
    else:
        print("잘못된 입력입니다")
        main()

def chooseLeague():
    uri_l = uri + "competitions"
    name = input("검색하고자 하는 리그를 입력하세요: ")
    tmp = []
    response = requests.get(uri_l, headers=headers)
    for league in response.json()['competitions']:
        val = name in league['name']
        if val:
            tmp.append([league['id'], league['name']])
        else:
            continue
        
    if len(tmp) > 1:
        for tmps in tmp['name']:
            print(tmps+'\n')
        n = input("위 리그 중에서 검색하고 싶은 리그의 번호를 입력하세요: ")
        print(tmp[n])
        
    elif len(tmp) == 1:
        print(tmp)
        
    else:
        print("검색 결과가 없습니다")
    
    
def chooseTeam():
    uri_t = uri + "teams?limit=200"
    name = input("검색하고자 하는 팀 이름을 입력하세요: ")
    response = requests.get(uri_t, headers=headers)
    for teams in response.json()['teams']:
        if name == teams['name']:
            uri_s = uri + "teams/" + str(teams['id'])
            response = requests.get(uri_s, headers=headers)
            print(response.json())
    
    
def choosePerson():
    uri_p = uri + "persons?limit=1000"
    
main()