import folium

# Criar um mapa centrado em São Paulo
mapa = folium.Map(
    location=[-23.5505, -46.6333],
    zoom_start=12
)

# Lista de cafeterias
cafeterias = [
    {"localizacao": [-23.5673, -46.6483], "nome": "Cafeteria A"},
    {"localizacao": [-23.5685, -46.6621], "nome": "Cafeteria B"},
    {"localizacao": [-23.5489, -46.6366], "nome": "Cafeteria C"},
    {"localizacao": [-23.5550, -46.6250], "nome": "Cafeteria D"},
]

# Adicionando marcadores ao mapa
for cafe in cafeterias:
    folium.Marker(
        location=cafe['localizacao'],
        popup=cafe['nome'],
        icon=folium.Icon(color='blue', icon='coffee')
    ).add_to(mapa)

# Salvar mapa interativo em HTML
mapa.save('datasets/mapa.html')
