from crypt import methods
from distutils.log import error
from webbrowser import get
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64
import requests
import flaskr.Line_notify
import flaskr.api

bp = Blueprint('history', __name__,url_prefix='/history')
sunabar_url = 'https://bank.sunabar.gmo-aozora.com/bank/notices/important'

"""一覧画面の処理"""
@bp.route('/main')
@login_required
def index():
  db = get_db()
  postdata = db.execute(
    'SELECT a.id, a.author_id, a.date, a.money, a.beneficiaryName, a.applyNo, a.flag, a.permit'
    ' FROM apidata AS a LEFT OUTER JOIN user AS u ON a.author_id = u.id'
    ' ORDER BY a.id DESC'
  ).fetchall()
  return render_template('history/main.html', postdata=postdata)


"""認証画面に遷移する際にIDが一致しているか確認"""
def get_post(id, check_author=True):
  postdata = get_db().execute(
    'SELECT a.id, author_id, date, money, beneficiaryName, applyNo, flag, permit'
    ' FROM apidata a JOIN user u ON a.author_id = u.id'
    ' WHERE a.id = ?', (id,)
  ).fetchone()

  if postdata is None:
    abort(404, 'ID {0} は存在しません' .format(id))

  if check_author and postdata['author_id'] != g.user['id']:
    abort(403)

  return postdata

"""認証画面の処理"""
@bp.route('history/<int:id>permission', methods=('GET','POST'))
@login_required
def permission(id):
  postdata = get_post(id)
  applyNo = postdata['applyNo']
  collback = flaskr.api.tfrequest(applyNo)
  resultcode = collback['resultCode']
  
  db = get_db()
  db.execute(
    'UPDATE apidata SET flag = ?'
    ' WHERE id = ?',
    (resultcode, id)
  )
  db.commit()
  data = get_post(id)

  db = get_db()
  postfamily = db.execute(
    'SELECT f.id, ship, famname, addres, author_id, username'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()


  ##--認証ボタン押されたときの処理--##
  if request.method == 'POST':
    db = get_db()
    famname = request.form.get('family') #承認者の名前
    jsonmsg = flaskr.api.cancel(applyNo) #API叩く
    
    msg = famname + 'から取消要求がありました。下記から確認して下さい' + sunabar_url
    flaskr.Line_notify.main(msg) #LINEに通知
    db.execute(
        'UPDATE apidata SET permit = ?'
        ' WHERE id = ?',
        (famname, id)
      )
    db.commit()
    
    return redirect(url_for('history.index'))

  return render_template('history/permission.html', postfamily=postfamily, data=data)












