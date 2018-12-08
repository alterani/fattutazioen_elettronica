#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 21:46:09 2018

Questo script è un client per le API HTTP REST del web service di fatturazione
elettronica ARUBA:


@author: enricoalterani
"""

import requests
import json

#LETTURA CREDENZIALI SERVER DA FILE JSON

with open('config.json') as f:
    credenziali = json.load(f)

utente = credenziali['ws_server_param']['username']
pwd = credenziali['ws_server_param']['password']



# LOGIN

url = "https://auth.fatturazioneelettronica.aruba.it/auth/signin"

payload = "grant_type=password&username="+utente+"&password=" + pwd
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'content-length': "53",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

datiRispsta = json.loads(response.text)

if (int(response.status_code) == 200):
    access_token = datiRispsta['access_token']
    refresh_token = datiRispsta['refresh_token']
    print('\n\n\nConnessione server Aruba avvenuta con successo\nIl token è: ' 
          + access_token[0:10] + '.....' 
          '\n' +
          'Il Refresh token è: ' + refresh_token)
    
else:
    print(datiRispsta)


#REFRESH TOKEN

url = "https://auth.fatturazioneelettronica.aruba.it/auth/signin"

payload = "grant_type=refresh_token&refresh_token=" + refresh_token
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'content-length': "53",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)


datiRispsta = json.loads(response.text)
if (int(response.status_code) == 200):
    access_token = datiRispsta['access_token']
    refresh_token = datiRispsta['refresh_token']
    print('\n\n\nConnessione ARUBA rinnovata!!\nIl token è: ' 
          + access_token[0:10] + '.....' 
          '\n' +
          'Il Refresh token è: ' + refresh_token)
    
else:
    print(datiRispsta)




# ELENCO FATTURE RICEVUTE
url = "https://ws.fatturazioneelettronica.aruba.it/services/invoice/out/findByUsername"

querystring = {"username":utente}

headers = {
    'accept': "application/json",
    'authorization': "Bearer " + access_token

    }

response = requests.request("GET", url,  headers=headers, params=querystring, verify=False)

datiRispsta = json.loads(response.text)
if (int(response.status_code) == 200):
    TotaleFattureRicevute = datiRispsta['totalElements']
    
    print('\n\n\nRICHIESTA ELENCO FATTURE\nHai ricevuto ' + str(TotaleFattureRicevute) +' fatture')
    
else:
    print(datiRispsta)



















