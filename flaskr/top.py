from base64 import encode
import functools
from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pandas as pd
import json
from flaskr.auth import login_required

bp = Blueprint('top', __name__,)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
  db = get_db()
  kannondata = pd.read_sql_query('SELECT name, temple_name, address, latitude, longitude, kannon_img, place_img_1, place_img_2, place_img_3 FROM kannondata',db)
  # kanon_df = kannondata.dropna(how='any')
  kannon_dict = kannondata.to_dict(orient='index')

  #json.dumpsいらなかった
  # js_kannon_data = json.dumps(kannon_dict, ensure_ascii=False)

  #宿泊データのDBインポート
  # df = pd.read_csv('okukawamura_data.csv', encoding="utf-8")
  # df.to_sql(con=db,name='lodging')

  lodging_data = pd.read_sql_query('SELECT name, address, distance_km, latitude, longitude, type, project1, project2, project3 FROM lodging',db)

  lodging_dict = lodging_data.to_dict(orient='index')
  
  return render_template('top/index.html', kannon_dict=kannon_dict,lodging_dict=lodging_dict)