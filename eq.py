import requests
from flask import Flask, render_template, abort
import folium

app = Flask(__name__)

def get_earthquake_data():
    """P2PQuake APIから最新の地震データを取得する関数"""
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    
    try:
        response = requests.get(p2pquake_url)
        response.raise_for_status()  # リクエストが成功したか確認
        data = response.json()
        if not data:
            raise ValueError("データが空です")
        return data[0]
    except (requests.RequestException, ValueError) as e:
        print(f"データ取得エラー: {e}")
        return None

def create_map(latitude, longitude, eq_name, magnitude, eq_day, eq_time):
    """地震の場所を示す地図を作成する関数"""
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker(
        [latitude, longitude], 
        popup=f"Location: {eq_name}\nMagnitude: {magnitude}\nDate: {eq_day}\nTime: {eq_time}"
    ).add_to(my_map)
    my_map.save('templates/map.html')

@app.route('/', methods=["GET"])
def index():
    earthquake_data = get_earthquake_data()
    
    if earthquake_data is None:
        abort(500, description="地震データの取得に失敗しました")
    
    # 地震データを抽出
    hypocenter = earthquake_data["earthquake"]["hypocenter"]
    latitude = hypocenter["latitude"]
    longitude = hypocenter["longitude"]
    eqdt = earthquake_data["earthquake"]["time"]
    eq_day, eq_time = eqdt.split()
    eq_name = hypocenter["name"]
    magnitude = hypocenter["magnitude"]
    tunami = earthquake_data["earthquake"]["domesticTsunami"]
    
    if tunami == "None":
        tunami = "津波はありません"
    else:
        return tunami
    # 地図を作成
    create_map(latitude, longitude, eq_name, magnitude, eq_day, eq_time)
    
    # テンプレートにデータを渡してレンダリング
    return render_template("eq.html", eq_day=eq_day, eq_time=eq_time, magnitude=magnitude, eq_name=eq_name, latitude=latitude, longitude=longitude,tunami = tunami)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
