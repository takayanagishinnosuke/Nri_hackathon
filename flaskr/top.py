from crypt import methods
from distutils.log import error
from email import message
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64
import flaskr.api
import pandas as pd
import flaskr.Line_notify
import json
from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ['access_token']
id = os.environ['accountId']

bp = Blueprint('top', __name__)
sunabar_url = 'https://bank.sunabar.gmo-aozora.com/bank/notices/important'

"""一覧画面の処理"""
@bp.route('/', methods=('GET','POST'))
def index():
  data,json = flaskr.api.deposit()
  db = get_db()
  #pandasDFをSQL格納(最新を上書き)
  data.to_sql('deposit', con=db, if_exists='replace')
  
  # print(json) #apiのjsonを確認

  return render_template('top/index.html',json=json)


"""おばあちゃんの振り込み画面"""

@bp.route('/clianttop', methods=('GET','POST'))
def clianttop():
  #POST時の処理
  if request.method == 'POST':
    date = request.form['date'] #日付
    transferAmount = request.form['transferAmount'] #金額
    beneficiaryBankCode = request.form.get('beneficiaryBankCode') #金融機関コード
    beneficiaryBranchCode = request.form.get('beneficiaryBranchCode') #支店コード
    accountTypeCode = request.form.get('accountTypeCode') #口座種別
    accountNumber = request.form.get('accountNumber') #口座番号
    beneficiaryName = request.form.get('beneficiaryName') #受取人名
  #json_dataを作る
    data = {
    "accountId": id,
    "remitterName": "ｱｵｿﾞﾗ ﾃｽﾄ",
    "transferDesignatedDate": date, #日付
    "transferDateHolidayCode": "1",
    "totalCount": "1",
    "totalAmount": transferAmount, #金額
    "transfers": [
        {
            "itemId": 1,
            "transferAmount": transferAmount, #金額
            "beneficiaryBankCode": beneficiaryBankCode, #金融コード
            # "beneficiaryBankName": "ｱｵｿﾞﾗ", #金融機関名(参考値)
            "beneficiaryBranchCode": beneficiaryBranchCode, #支店コード
            # "beneficiaryBranchName": "ﾎﾝﾃﾝ", #支店名(参考値)
            "accountTypeCode": accountTypeCode, #普通1 当座2 
            "accountNumber": accountNumber, #口座番号
            "beneficiaryName": beneficiaryName  #受取人名
            }
    ]}
  # APIを叩いて作ったjsonを渡す
    status = flaskr.api.transfer(data)
    applyno = status['applyNo'] #applyNoの取得
  #DBに情報を格納
    flag = 2
    db = get_db()
    db.execute(
      'INSERT INTO apidata (author_id, money, beneficiaryName, applyNo, flag)'
      ' VALUES (?, ?, ?, ?, ?)',
      (g.user['id'],transferAmount, beneficiaryName, applyno, flag)
    )
    db.commit()

    #LINE送信
    msg = 'おばあちゃんから振り込み要求がありました。下記から確認して下さい' + sunabar_url
    flaskr.Line_notify.main(msg)

    return status

  else:
    return render_template('top/clianttop.html')

  






