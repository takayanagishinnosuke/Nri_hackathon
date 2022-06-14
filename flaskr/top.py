import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pandas as pd

bp = Blueprint('top', __name__,)

@bp.route('/top', methods=('GET', 'POST'))
def index():
  db = get_db()
 
  return render_template('top/index.html')