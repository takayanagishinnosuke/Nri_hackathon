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
  kannondata = pd.read_sql_query('SELECT name, temple_name, address, latitude, longitude FROM kannondata',db)
  kanon_df = kannondata.dropna(how='any')
  kannon_dict = kanon_df.to_dict(orient='index')
  # js_kannon_data = json.dumps(kannon_dict, ensure_ascii=False)
  
  
  return render_template('top/index.html', kannon_dict=kannon_dict)