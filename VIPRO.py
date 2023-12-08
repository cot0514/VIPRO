import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        print(f'{ i }: { league["name"] }')
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
            print(f'{ idx }: { t }')
            idx = idx + 1
        n = input("위 팀 중에서 검색하고 싶은 팀의 번호를 고르시오: ")
        teamInfo(tmp[int(n)-1])
    elif len(tmp) == 1:
        teamInfo(tmp[0])
    else:
        print("잘못 입력하셨습니다")
        chooseTeam()
    
def leagueInfo(tmp):
    uri_i = uri + "competitions/" + str(tmp[0])
    print("1: 순위 검색, 2: 득점 랭킹 보기")
    n = input()
    if n == '1':
        rank(uri_i + "/standings")
    elif n == '2':
        scorers(uri_i + "/scorers")
    else:
        print("잘못된 입력입니다.")
        leagueInfo(tmp)

def rank(uri_r):
    year = input("검색하고 싶은 년도를 고르시오: ")
    uri_r = uri_r + "?season=" + year
    response = requests.get(uri_r, headers=headers)
    tables = response.json()['standings'][0]
    col = ['name', 'pg', 'form', 'won', 'draw', 'lost', 'points']
    ind = [x + 1 for x in range(20)]
    con = []
    for rank in tables['table']:
        co = []
        for tag, info in rank.items():
            if tag == 'team':
                co.append(info['name'])
                continue
            elif tag == 'playedGames':
                co.append(info)
                continue
            elif tag == 'form':
                co.append(info)
                continue
            elif tag == 'won':
                co.append(info)
                continue
            elif tag == 'draw':
                co.append(info)
                continue
            elif tag == 'lost':
                co.append(info)
                continue
            elif tag == 'points':
                co.append(info)
                continue
        con.append(co)
        
    df = pd.DataFrame(con, columns=col, index=ind)
    print(df)

def scorers(uri_s):
    year = input("검색하고 싶은 년도를 고르시오: ")
    uri_s = uri_s + "?season=" + year
    response = requests.get(uri_s, headers=headers)
    col = ['name', 'team', 'match', 'goals', 'assists', 'penalties']
    ind = [x + 1 for x in range(10)]
    con = []
    for score in response.json()['scorers']:
        co = []
        for tag, info in score.items():
            if tag == 'player':
                co.append(info['name'])
                continue
            elif tag == 'team':
                co.append(info['tla'])
                continue
            elif tag == 'playedMatches' or tag == 'goals' or tag == 'assists' or tag == 'penalties':
                co.append(info)
                continue
        con.append(co)
    
    df = pd.DataFrame(con, columns=col, index=ind)
    print(df)
        
def teamInfo(tmp):
    print(tmp[0])
    uri_m = uri + "teams/" + str(tmp[1])
    response = requests.get(uri_m, headers=headers)
    for team, team_i in response.json().items():
        if team == 'area':
            print(f'area: { team_i["name"] }')
            continue
        elif team == 'name' or team == 'venue':
            print(f'{ team }: { team_i }')
            continue
        elif team == 'runningCompetitions':
            if len(team_i) > 1:
                rc = []
                for n in team_i:
                    rc.append(n['name'])
                print(f'{ team }: { rc }')
                continue
            print(f'{ team }: { team_i["name"] }')
            continue
        elif team == 'coach':
            print(f'{ team }: { team_i["name"] }')
            continue
        if team == "squad":
            mem = team_i
            print("squad")
            for mems in mem:    
                print(f'{ mems["position"] }: { mems["name"] }')
            break
        
    uri_m = uri_m + "/matches"
    teamMatch(uri_m, tmp[1])

def teamMatch(uri_m, id_t):
    uri_mf = uri_m + "?status=FINISHED"
    col = ['league', 'date', 'home', 'away', 'home_sc', 'away_sc', 'result']
    con = []
    response = requests.get(uri_mf, headers=headers)
    for tag, info in response.json().items():
        if tag == 'resultSet':
            print(f'이번 시즌 경기 결과 {{win: { info["wins"] }, draw: { info["draws"] }, loss: { info["losses"] } }}')
            
        elif tag == 'matches':
            ind = [x + 1 for x in range(len(info))]
            for inf in info:
                co = []
                tmp = []
                for tag_m, info_m in inf.items():
                    if tag_m == 'competition':
                        co.append(info_m['code'])
                        continue
                    elif tag_m == 'utcDate':
                        co.append(info_m)
                        continue
                    elif tag_m == 'homeTeam' or tag_m == 'awayTeam':
                        co.append(info_m['tla'])
                        if info_m['id'] == id_t:
                            tmp.append(tag_m[0])
                        continue
                    elif tag_m == 'score':
                        score = info_m['fullTime']
                        co.append(score['home'])
                        co.append(score['away'])
                        if info_m['winner'] == 'HOME_TEAM':
                            if tmp[0] == 'h':
                                co.append('Win')
                            elif tmp[0] == 'a':
                                co.append('Loss')
                        elif info_m['winner'] == 'AWAY_TEAM':
                            if tmp[0] == 'h':
                                co.append('Loss')
                            elif tmp[0] == 'a':
                                co.append('Win')
                        else:
                            co.append('Draw')
                        continue
                con.append(co)
                    
    df = pd.DataFrame(con, columns=col, index=ind)
    print(df)
            
if __name__ == '__main__':
    main()