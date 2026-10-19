import pandas as pd
from pathlib import Path

EXCEL_FILE = "バス停緯度経度時刻.xlsx"

ROUTES = [
    ("本庁1・2・3・4便", "honcho", [1, 2, 3, 4]),
    ("首里1・2・3・4便", "syuri", [1, 2, 3, 4]),
    ("真和志1・2便", "mawashi", [1, 2]),
    ("真和志3・4便", "mawashi", [3, 4]),
    ("小禄1・2便", "oroku", [1, 2]),
    ("小禄3・4", "oroku", [3, 4]),
]

REGION_NAME = {
    "honcho": "本庁",
    "syuri": "首里",
    "mawashi": "真和志",
    "oroku": "小禄",
}


def create_header(region, bus_no):

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="style.css">

<title>{REGION_NAME[region]}コース{bus_no}便</title>
</head>

<body style="
margin:0;
padding:0;
background:#a35050;
">

<div class="home-container">

<h1 class="page-title">
🚌 {REGION_NAME[region]} {bus_no}便
</h1>

<div class="page-header">

<a href="index.html">
<button class="top-button">
🏠トップへ<br>
もどる
</button>
</a>

<a href="map-map.html
<button class="map-button">
🗺️地図を<br>
見る
</button>
</a>

{region}.html
<button class="top-button back-course-button">
🌻<br>
{REGION_NAME[region]}コースへ<br>
もどる
</button>
</a>

</div>

<div class="stop-list">
<div class="stops">
"""


def create_footer():

    return """
</div>
</div>

</div>

</body>
</html>
"""


for sheet_name, region, bus_list in ROUTES:

    print(f"処理中: {sheet_name}")

    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name=sheet_name,
        engine="openpyxl"
    )

    columns = list(df.columns)

    stop_col = columns[0]
    lat_col = columns[1]
    lon_col = columns[2]

    for bus_no in bus_list:

        time_col = f"{bus_no}便"

        html = create_header(region, bus_no)

        for _, row in df.iterrows():

            stop_name = row[stop_col]

            if pd.isna(stop_name):
                continue

            bus_time = row[time_col]
            lat = row[lat_col]
            lon = row[lon_col]

            if pd.isna(bus_time):
                continue

            html += f"""
<button class="busstop"
onclick="window.location.href='https://www.google.com/maps?q={lat},{lon}'"
style="background:white; color:black;">
{bus_time}　{stop_name}
</button>
"""

        html += create_footer()

        output_file = f"{region}_{bus_no}_auto.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"作成: {output_file}")

print("完了")