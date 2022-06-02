# 離れて暮らす家族のアナリティクスアプリ
## 機能一覧
- 入出金履歴サマリー
- 振込依頼
- 振込キャンセル
- 家族登録
- 振込用アカウント登録
- LINE通知

## 画面
<img width="1236" alt="スクリーンショット 2022-06-03 2 12 51" src="https://user-images.githubusercontent.com/97178451/171686809-95a1f3e7-e457-4a47-bd43-eb35dff79a8d.png">
<img width="512" alt="スクリーンショット 2022-06-03 2 13 09" src="https://user-images.githubusercontent.com/97178451/171687474-b3f11cef-52e3-4dfd-9423-dcda60c241af.png">
<img width="777" alt="スクリーンショット 2022-06-03 2 13 38" src="https://user-images.githubusercontent.com/97178451/171687595-b8dcf0e4-bd94-4698-af57-10578dd5fad6.png">
<img width="983" alt="スクリーンショット 2022-06-03 2 14 22" src="https://user-images.githubusercontent.com/97178451/171687662-a8371181-71f4-48aa-886a-dfd87c20a3c8.png">


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
