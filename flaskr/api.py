import os
from base64 import encode
from email.encoders import encode_7or8bit
from encodings import utf_8
import http.client
from textwrap import indent
import requests
import pandas as pd
import json
import sqlite3
from dotenv import load_dotenv
load_dotenv()

token = os.environ['access_token']
id = os.environ['accountId']


"""apiを叩いてpandasのdfにする"""
def deposit():
    conn = http.client.HTTPSConnection("api.gmo-aozora.com")

    headers = {
        'x-access-token': token,
        'accept': "application/json;charset=UTF-8"
        }

    conn = requests.get("https://api.sunabar.gmo-aozora.com/personal/v1/accounts/transactions?accountId="+id+"&dateFrom=2022-04-30", headers=headers)


    print(conn.status_code) #ステータスコードの確認
    jsondata = conn.json() #json型で読み込み
    
    jsondict = jsondata['transactions'] #json[transactions]keyだけ取得
    
    df_s = pd.DataFrame(jsondict) #pandasのdf型にする

    #dfのculumnsを変更
    df_s.columns=['Date', 'ValueDate', 'Type', 'Amount', 'Remarks','Balance','Itemkey']
    df_s.head() #確認用で表示

    return df_s

"""振り込み時のapi"""
def transfer(jsondata):
    conn = http.client.HTTPSConnection("api.gmo-aozora.com")

    headers = {
            'Accept': "application/json;charset=UTF-8",
            'Content-Type': "application/json",
            'x-access-token': token,
            # 'Idempotency-Key': "your idempotency key"
            }

    conn = requests.post(
        "https://api.sunabar.gmo-aozora.com/personal/v1/transfer/request",
        data= json.dumps(jsondata),
        headers=headers)

    print(conn.status_code)
    print(conn.json()) #json型で読み込み

    status = conn.json()
    return status

"""振込依頼結果照会"""
def tfrequest(applyno):
    conn = http.client.HTTPConnection("api.gmo-aozora.com")

    headers = {
    'Accept': "application/json;charset=UTF-8",
    'x-access-token': token
    }

    conn = requests.get("https://api.sunabar.gmo-aozora.com/personal/v1/transfer/request-result?accountId="+id+"&applyNo=" + applyno, headers=headers)

    print(conn.status_code)

    result = conn.json()
    print(result)

    return result

"""振り込み取り消し依頼"""
def cancel(applyno):
    conn = http.client.HTTPConnection("api.gmo-aozora.com")

    payload = {
        "accountId":id,
        "cancelTargetKeyClass": "2",
        "applyNo":applyno
        }

    headers = {
        'Accept': "application/json;charset=UTF-8",
        'Content-Type': "application/json",
        'x-access-token': token
        }

    conn = requests.post("https://api.sunabar.gmo-aozora.com/personal/v1/transfer/cancel",data=json.dumps(payload), headers=headers)

    print(conn.status_code)
    result = conn.json()

    return result
