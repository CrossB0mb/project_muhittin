import folium
import pandas as pd

# Load your data
df = pd.read_csv("D:\\tasarim_proje\project_muhittin\\adsb_test_files\\adsb_deneme.csv")  # Replace with your data path

# Create a base map centered at a rough central coordinate
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=6)

# Add plane markers
for _, row in df.iterrows():
    popup_text = f"Callsign: {row['Callsign']}<br>Altitude: {row['Altitude']} ft"
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='plane', prefix='fa')
    ).add_to(m)

# Save to HTML
m.save("adsb_planes_map.html")
