from base64 import encode
import functools
from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pandas as pd
import json

bp = Blueprint('top', __name__,)

@bp.route('/top', methods=('GET', 'POST'))
def index():
  db = get_db()
  kannondata = pd.read_sql_query('SELECT name, temple_name, address, latitude, longitude, kannon_img, place_img_1, place_img_2, place_img_3 FROM kannondata',db)
  # kanon_df = kannondata.dropna(how='any')
  kannon_dict = kannondata.to_dict(orient='index')

  #json.dumpsはいらなかった
  # js_kannon_data = json.dumps(kannon_dict, ensure_ascii=False)

  #宿泊データのDBインポート
  # df = pd.read_csv('nishiaizu_lodging_facilities.csv', encoding="shift-jis")
  # df2 = df.drop(df.columns[6],axis=1)
  # df2.to_sql(con=db,name='syukuhaku')

  lodging_data = pd.read_sql_query('SELECT name, address, distance_km, latitude, longitude FROM syukuhaku',db)

  lodging_df = lodging_data.dropna(how='any')
  lodging_dict = lodging_df.to_dict(orient='index')

  print(lodging_dict)

  
  return render_template('top/index.html', kannon_dict=kannon_dict, lodging_dict=lodging_dict)