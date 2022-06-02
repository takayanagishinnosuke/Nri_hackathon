from crypt import methods
from distutils.log import error
from wsgiref.util import shift_path_info
from flask import Blueprint, flash, g, redirect, render_template, request, url_for,session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename
import base64

bp = Blueprint('family', __name__, url_prefix='/fam')

"""家族一覧ページ"""
@bp.route('/main', methods=('GET', 'POST'))
@login_required
def index():
  db = get_db()
  postfamily = db.execute(
    'SELECT f.id, ship, famname, addres, author_id, username, filepath'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' ORDER BY created DESC'
  ).fetchall()
  return render_template('fam/main.html', postfamily=postfamily)


"""家族登録"""
@bp.route('/createfamily', methods=('GET', 'POST'))
@login_required
def createfamily():
  
  if request.method == 'POST':
    ship = request.form['ship']
    famname = request.form['famname']
    addres = request.form['addres']
    files = request.files.get('file')
    filename = secure_filename(files.filename)
    filepath = 'static/family_img/' + filename
    
    error = None

    if not ship:
      error = '続柄が入力されてません'
    if not famname:
      error = '家族の名前が入力されてません'
    if not addres:
      error = '連絡先が入力されてません'
    if error is not None:
      flash(error)
    else:
      files.save(filepath)
      print(filepath)

      db = get_db()
      db.execute(
        'INSERT INTO family (ship, famname, addres, filepath, author_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (ship, famname, addres, filepath, g.user['id'])
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/createfamily.html')

"""更新の処理"""
"""更新するIDが一致しているか確認"""
def get_post(id, check_author=True):
  family = get_db().execute(
    'SELECT f.id, famname, addres, author_id, ship, filepath'
    ' FROM family f JOIN user u ON f.author_id = u.id'
    ' WHERE f.id = ?', (id,)
  ).fetchone()

  if family is None:
    abort(404, 'ID {0} は存在しません' .format(id))

  if check_author and family['author_id'] != g.user['id']:
    abort(403)

  return family

"""編集する処理"""
@bp.route('/<int:id>update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    ship = request.form['ship']
    famname = request.form['famname']
    addres = request.form['addres']
    error = None

    if not ship:
      error = '続柄は必須です'
    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE family SET ship = ?, famname = ?, addres = ?'
        ' WHERE id = ?',
        (ship, famname, addres, id)
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM family WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('family.index'))


"""おばあちゃん(クライアント登録)"""
@bp.route('/cliant', methods=('GET', 'POST'))
@login_required
def create_cliant():
  db = get_db()
  if request.method == 'POST':
    cliantname = request.form['cliantname']
    ship = request.form['ship']
    cliant_id = request.form['cliant_id']
    password = request.form['password']

    files = request.files.get('file')
    filename = secure_filename(files.filename)
    filepath = 'static/family_img/' + filename
    
    error = None

    if not cliantname:
      error = '名前が入力されてません'
    elif not ship:
      error = '続柄が入力されてません'
    elif not cliant_id:
      error = 'IDが入力されてません'
    elif not password:
      error = 'パスワードが入力されてません'
    elif error is not None:
      flash(error)
    elif db.execute(
          "SELECT id FROM cliant WHERE cliant_id = ?", (cliant_id,)
        ).fetchone() is not None:
          error = 'ID{}はすでに登録されています'.format(cliant_id)
    else:
      files.save(filepath)
      
      db.execute(
        'INSERT INTO cliant (cliantname, ship, cliant_id, password, filepath, author_id)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (cliantname, ship, cliant_id, generate_password_hash(password), filepath, g.user['id'])
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/cliant.html')


"""クライアント編集の処理"""
"""編集するIDが一致しているか確認"""
def get_post_cliant(id, check_author=True):
  cliant = get_db().execute(
    'SELECT c.id, author_id, cliantname, ship, cliant_id, filepath'
    ' FROM cliant c JOIN user u ON c.author_id = u.id'
    ' WHERE c.id = ?', (id,)
  ).fetchone()

  if cliant is None:
    abort(404, 'ID {0} は存在しません' .format(id))

  if check_author and cliant['author_id'] != g.user['id']:
    abort(403)

  return cliant

"""編集する処理"""
@bp.route('/<int:id>cliantupdate', methods=('GET', 'POST'))
@login_required
def updatecliant(id):
  cliant = get_post_cliant(id)
  error = None

  if request.method == 'POST':
    cliantname = request.form['cliantname']
    ship = request.form['ship']

    files = request.files.get('file')
    filename = secure_filename(files.filename)
    filepath = 'static/family_img/' + filename

    if not ship:
      error = '続柄は必須です'
    elif not cliantname:
      error = '名前が入力されてません'
    elif error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE cliant SET cliantname = ?, ship = ?, filepath = ?'
        ' WHERE id = ?',
        (cliantname, ship, filepath, id)
      )
      db.commit()
      return redirect(url_for('family.index'))
  return render_template('fam/cliantupdate.html', cliant=cliant)


@bp.route('/<int:id>/cliantdelete', methods=('POST',))
@login_required
def deletecliant(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM cliant WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('family.index'))