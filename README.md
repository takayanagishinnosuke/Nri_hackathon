# 離れて暮らす家族のアナリティクスアプリ
## 機能一覧
- 入出金履歴サマリー
- 振込依頼
- 振込キャンセル
- 家族登録
- 振込用アカウント登録
- LINE通知

## 注意点
- APIトークンが書き込んである環境ファイルは上げてません。

```
#ライブラリのinstallと更新
pip install -r requirements.txt
```
```
export FLASK_APP=__init__.py
```
```
flask run
```
- 管理者ログインIDとパスワード
```
ID: admin
PW: admin
```
- ユーザーログインIDとパスワード
```
ID: user
PW: user
```
