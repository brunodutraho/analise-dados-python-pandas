import pandas as pd
import folium

url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.csv'
df_terremotos = pd.read_csv(url)

terremotos_significativos = df_terremotos[
    df_terremotos['mag'].notna() & (df_terremotos['mag'] >= 6.0)
]

mapa_terremotos = folium.Map(
    location=[
        terremotos_significativos['latitude'].mean(),
        terremotos_significativos['longitude'].mean()
    ],
    zoom_start=2
)

for _, terremoto in terremotos_significativos.iterrows():
    folium.CircleMarker(
        location=[terremoto['latitude'], terremoto['longitude']],
        radius=terremoto['mag'] * 2,
        popup=(
            f"<b>Local:</b> {terremoto['place']}<br>"
            f"<b>Magnitude:</b> {terremoto['mag']}<br>"
            f"<b>Profundidade:</b> {terremoto['depth']} km"
        ),
        color='red',
        fill=True,
        fill_opacity=0.6
    ).add_to(mapa_terremotos)

mapa_terremotos.save('datasets/mapa_terremotos.html')
