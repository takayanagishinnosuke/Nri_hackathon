from ensurepip import bootstrap
import os
from flask_bootstrap import Bootstrap
from flask import Flask


def create_app(test_config=None):
    # 初期設定
    app = Flask(__name__, instance_relative_config=True)
    # app.config['JSON_AS_ASCII'] = False
    app.config.from_mapping(
        SECRET_KEY='dev', #デプロイ時はKeyをしっかり暗号化する
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), #DBの指定
        bootstrap = Bootstrap(app),
    )

    if test_config is None:
        # インスタンス構成が存在する場合、テストしない場合はそれをロードする
        app.config.from_pyfile('config.py', silent=True)
    else:
        # で渡された場合、テストコンフィグをロードします。
        app.config.from_mapping(test_config)

    # インスタンスフォルダが存在することを確認する
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ルーティングの設定だよ
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import top
    app.register_blueprint(top.bp)

    from . import mypage
    app.register_blueprint(mypage.bp)
    
    return app