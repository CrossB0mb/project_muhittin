import folium
import pandas as pd
import time

def create_map():
    df = pd.read_csv("adsb_data_info.csv")  # Fetch latest data

    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=4)

    for _, row in df.iterrows():
        popup = f"Callsign: {row['Callsign']}<br>Altitude: {row['Altitude']} ft"
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            icon=folium.Icon(color='blue', icon='plane', prefix='fa')
        ).add_to(m)

    m.save("adsb_planes_map.html")

    # Inject refresh tag
    with open("adsb_planes_map.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("<head>", "<head>\n<meta http-equiv='refresh' content='10'>\n")

    with open("adsb_planes_map.html", "w", encoding="utf-8") as f:
        f.write(html)

# Repeat every 10 seconds
while True:
    create_map()
    print("Map updated.")
    time.sleep(10)
