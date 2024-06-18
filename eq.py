import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    # リクエストするURLを指定
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    
    # リクエスト(データを取得する)
    p2pquake_json = requests.get(p2pquake_url).json()
    
    # 緯度
    latitude = p2pquake_json[0]["earthquake"]["hypocenter"]["latitude"]
    # 経度
    longitude = p2pquake_json[0]["earthquake"]["hypocenter"]["longitude"]
    # 地震発生時刻
    eqtime = p2pquake_json[0]["earthquake"]["time"]
    # 発生地
    eq_name = p2pquake_json[0]["earthquake"]["hypocenter"]["name"]
    # マグニチュード
    magnitude = p2pquake_json[0]["earthquake"]["hypocenter"]["magnitude"]
    
    # 取得したデータをテンプレートに渡す
    return render_template("eq.html", eqtime=eqtime, magnitude=magnitude, eq_name=eq_name, latitude=latitude, longitude=longitude)

if __name__ == "__main__":
    app.run(port=8000, debug=True)