import re

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import requests

df_final = pd.DataFrame()

page = 11700
while page != 11820:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.get(f"https://en.volleyballworld.com/volleyball/competitions/vnl-2021/schedule/{page}/")
    sleep(6)
    site = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    teams_name = []
    regex5 = re.compile('vbw-mu__team__name')
    for x in site.find_all("div", {'class': regex5}):
        teams_name.append(x.text)

    regex6 = re.compile('vbw-mu__score--home')
    placar_home = site.find('div', {'class': regex6}).text

    regex7 = re.compile('vbw-mu__score--away')
    placar_away = site.find('div', {'class': regex7}).text

    placar_home = int(placar_home)
    placar_away = int(placar_away)

    result = placar_home - placar_away

    if result < 0:
        home_vencedor = False
    else:
        home_vencedor = True

    n_sets = placar_home + placar_away

    regex = re.compile('vbw-o-table__cell stats-score ')

    points = []
    for pn in site.findAll("td", {'class': regex}):
        points.append(pn.text)

    home_attack_points = int(points[0])
    away_attack_points = int(points[1])
    home_block_points = int(points[2])
    away_block_points = int(points[3])

    errors = []
    regex2 = re.compile('vbw-o-table__cell errors')

    for pn in site.findAll("td", {'class': regex2}):
        errors.append(pn.text)

    total_attacks_errors_home = errors[14:28]
    total_attacks_errors_home = list(map(int, total_attacks_errors_home))
    total_attacks_errors_home_sum = sum(total_attacks_errors_home)

    total_attacks = []
    regex3 = re.compile('vbw-o-table__cell total')

    for pn in site.findAll("td", {'class': regex3}):
        total_attacks.append(pn.text)

    total_attacks_home = total_attacks[14:28]
    total_attacks_home = list(map(int, total_attacks_home))
    total_attacks_home_sum = sum(total_attacks_home)

    total_reception_home = total_attacks[56:70]
    for n, i in enumerate(total_reception_home):
        if i == '':
            total_reception_home[n] = 0
    total_reception_home = list(map(float, total_reception_home))
    total_reception_home = list(map(int, total_reception_home))
    total_reception_home_sum = sum(total_reception_home)

    successful_reception = []
    regex4 = re.compile('vbw-o-table__cell successful')

    for x in site.findAll("td", {'class': regex4}):
        successful_reception.append(x.text)

    successful_reception_home = successful_reception[:14]
    successful_reception_home = list(map(int, successful_reception_home))
    successful_reception_home_sum = sum(successful_reception_home)

    serve_errors_home = errors[42:56]
    serve_errors_home = list(map(int, serve_errors_home))
    serve_errors_home_sum = sum(serve_errors_home)

    if n_sets == 3:
        total_attacks_away = total_attacks[406:420]
        total_attacks_away = list(map(int, total_attacks_away))
        total_attacks_away_sum = sum(total_attacks_away)
        total_attacks_errors_away = errors[406:420]
        total_attacks_errors_away = list(map(int, total_attacks_errors_away))
        total_attacks_errors_away_sum = sum(total_attacks_errors_away)

        serve_errors_away = errors[434:448]
        serve_errors_away = list(map(int, serve_errors_away))
        serve_errors_away_sum = sum(serve_errors_away)

        total_reception_away = total_attacks[448:462]
        for n, i in enumerate(total_reception_away):
            if i == '':
                total_reception_away[n] = 0
        total_reception_away = list(map(int, total_reception_away))
        total_reception_away_sum = sum(total_reception_away)

        successful_reception_away = successful_reception[112:126]
        successful_reception_away = list(map(int, successful_reception_away))
        successful_reception_away_sum = sum(successful_reception_away)

    elif n_sets == 4:
        total_attacks_away = total_attacks[504:518]
        total_attacks_away = list(map(int, total_attacks_away))
        total_attacks_away_sum = sum(total_attacks_away)
        total_attacks_errors_away = errors[504:518]
        total_attacks_errors_away = list(map(int, total_attacks_errors_away))
        total_attacks_errors_away_sum = sum(total_attacks_errors_away)

        serve_errors_away = errors[532:546]
        serve_errors_away = list(map(int, serve_errors_away))
        serve_errors_away_sum = sum(serve_errors_away)
        print(serve_errors_away_sum)
        total_reception_away = total_attacks[546:560]
        for n, i in enumerate(total_reception_away):
            if i == '':
                total_reception_away[n] = 0
        total_reception_away = list(map(int, total_reception_away))
        total_reception_away_sum = sum(total_reception_away)

        successful_reception_away = successful_reception[140:154]
        successful_reception_away = list(map(int, successful_reception_away))
        successful_reception_away_sum = sum(successful_reception_away)
    else:
        total_attacks_away = total_attacks[602:616]
        total_attacks_away = list(map(int, total_attacks_away))
        total_attacks_away_sum = sum(total_attacks_away)
        total_attacks_errors_away = errors[602:616]
        total_attacks_errors_away = list(map(int, total_attacks_errors_away))
        total_attacks_errors_away_sum = sum(total_attacks_errors_away)

        serve_errors_away = errors[630:644]
        serve_errors_away = list(map(int, serve_errors_away))
        serve_errors_away_sum = sum(serve_errors_away)

        total_reception_away = total_attacks[644:658]
        for n, i in enumerate(total_reception_away):
            if i == '':
                total_reception_away[n] = 0
        total_reception_away = list(map(int, total_reception_away))
        total_reception_away_sum = sum(total_reception_away)

        successful_reception_away = successful_reception[168:182]
        successful_reception_away = list(map(int, successful_reception_away))
        successful_reception_away_sum = sum(successful_reception_away)


    dict_game = {
        'game id': page,
        'team home': teams_name[0],
        'total atq home': total_attacks_home_sum,
        'pontos ataques home': home_attack_points,
        'atq error home': total_attacks_errors_home_sum,
        '% atq home': round((home_attack_points / total_attacks_home_sum) * 100),
        '% rec home': round((successful_reception_home_sum / total_reception_home_sum) * 100),
        'bloqueio home': home_block_points,
        'server error home': serve_errors_home_sum,
        'team away': teams_name[2],
        'total atq away': total_attacks_away_sum,
        'pontos ataques away': away_attack_points,
        'atq error away': total_attacks_errors_away_sum,
        '% atq away': round((away_attack_points / total_attacks_away_sum) * 100),
        '% rec away': round((successful_reception_away_sum / total_reception_away_sum) * 100),
        'bloqueio away': away_block_points,
        'server error away': serve_errors_away_sum,
        'qts sets': n_sets,
        'vencedor': home_vencedor
    }

    # 18 colunas no dataframe original
    page = page + 1
    df_final = df_final.append([dict_game])
    print('Jogo: ' + teams_name[0] + ' x ' + teams_name[2])
    sleep(1)


df_final.to_csv('vnl_2021_preliminaryRound_mens.csv')