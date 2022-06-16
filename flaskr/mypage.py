import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pandas as pd

bp = Blueprint('mypage', __name__,)

@bp.route('/user', methods=('GET', 'POST'))
def index():
  user_id = session.get('user_id')
  db = get_db()
  postdata = db.execute(
    'SELECT username, id'
    ' FROM user'
    ' WHERE id = ?', (user_id,)
  ).fetchone()

  return render_template('mypage/user.html', postdata=postdata)