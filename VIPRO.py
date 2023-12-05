import json
import requests

uri = 'https://api.football-data.org/v4/'
headers = { 'X-Auth-Token': '09158fc8680949dd8c7cb4644d5ee282' }

def main():
    select = input("리그 검색: 1, 팀 검색: 2\n")
    
    if select == '1':
        chooseLeague()
    elif select == '2':
        chooseTeam()
    else:
        print("잘못된 입력입니다")
        main()

def chooseLeague():
    uri_l = uri + "competitions"
    response = requests.get(uri_l, headers=headers)
    tmp = []
    i = 1
    for league in response.json()['competitions']:
        tmp.append([league['id'], league['name'], league['code']])
        print(str(i) + ": " + league['name'])
        i = i + 1
    
    n = ""
    while 1:
        n = input("위 리그 중, 검색하고 싶은 리그의 번호를 고르시오: ")
        if int(n) > 13 or int(n) < 1:
            print("입력값이 잘못됐습니다.")
        else:
            break
    leagueInfo(tmp[int(n)-1])
    
    
def chooseTeam():
    uri_t = uri + "teams?limit=200"
    tmp = []
    name = input("검색하고자 하는 팀 이름을 입력하세요: ")
    response = requests.get(uri_t, headers=headers)
    for teams in response.json()['teams']:
        val = name in teams['name']
        if val:
            tmp.append([teams['name'], teams['id']])
        else:
            continue
    
    idx = 1
    if len(tmp) > 1:
        for t, i in tmp:
            print(str(idx) + ": " + t)
            idx = idx + 1
        n = input("위 팀 중에서 검색하고 싶은 팀의 번호를 고르시오: ")
        teamMatch(tmp[int(n)-1])
    elif len(tmp) == 1:
        teamMatch(tmp[0])
    else:
        print("잘못 입력하셨습니다")
        chooseTeam()
    
def leagueInfo(tmp):
    uri_i = uri + "competitions/" + str(tmp[0])
    print("1: 순위 검색, 2: 참가 팀 검색, 3: 득점 랭킹 보기")
    n = input()
    if n == '1':
        rank(uri_i + "/standings")
    elif n == '2':
        team_sc(uri_i + "/teams")
    elif n == '3':
        scorers(uri_i + "/scorers")
    else:
        print("잘못된 입력입니다.")
        leagueInfo(tmp)

def rank(uri_r):
    year = input("검색하고 싶은 년도를 고르시오")
    uri_r = uri_r + "?season=" + year
    response = requests.get(uri_r, headers=headers)
    for ranks in response.json()['standings']:
        print(ranks)

def team_sc(uri_e):
    year = input("검색하고 싶은 년도를 고르시오")
    uri_e = uri_e + "?season=" + year
    response = requests.get(uri_e, headers=headers)
    for teams in response.json()['teams']:
        print(teams)
        
def scorers(uri_s):
    year = input("검색하고 싶은 년도를 고르시오")
    uri_s = uri_s + "?season=" + year
    response = requests.get(uri_s, headers=headers)
    for score in response.json()['scorers']:
        print(score)
        
def teamMatch(tmp):
    print(tmp[0])
    uri_m = uri + "teams/" + str(tmp[1])
    response = requests.get(uri_m, headers=headers)
    for team, team_i in response.json().items():
        if team == 'area':
            print('area: ', team_i['name'])
            continue
        elif team == 'name':
            print(team + ": ", team_i)
            continue
        elif team == 'venue':
            print(team + ": ", team_i)
            continue
        elif team == 'runningCompetitions':
            if len(team_i) > 1:
                rc = []
                for n in team_i:
                    rc.append(n['name'])
                print('runningCompetitions: ', rc)
                continue
            print('runningCompetitions: ', team_i['name'])
            continue
        elif team == 'coach':
            print('coach: ', team_i['name'])
            continue
        if team == "squad":
            mem = team_i
            print("squad: ")
            for mems in mem:    
                print(mems['position'], ": ", mems['name'])
            break

    




main()