import time
import folium
import pandas as pd
import joblib
import requests

# ================================
# Load trained model
# ================================
model = joblib.load("flood_model_cyprus.pkl")

# ================================
# Cyprus cities (real locations)
# ================================
cities = {
    # Major cities
    "Nicosia": (35.1856, 33.3823),
    "Limassol": (34.7071, 33.0226),
    "Larnaca": (34.9182, 33.6233),
    "Paphos": (34.7754, 32.4218),
    "Famagusta": (35.1167, 33.9500),
    "Kyrenia": (35.3417, 33.3167),

    # North Cyprus
    "Morphou": (35.1989, 32.9931),
    "Lapta": (35.3389, 33.1611),
    "Alsancak": (35.3444, 33.1936),
    "Dikmen": (35.2681, 33.3408),
    "Değirmenlik": (35.2897, 33.4356),
    "Geçitkale": (35.2606, 33.7922),
    "Iskele": (35.2722, 33.9458),

    # South Cyprus
    "Geroskipou": (34.7567, 32.4547),
    "Chloraka": (34.8075, 32.4064),
    "Ypsonas": (34.6889, 32.9556),
    "Kato Polemidia": (34.6967, 33.0111),
    "Aradippou": (34.9517, 33.5928),
    "Athienou": (35.0608, 33.5419),

    # West / rural
    "Polis": (35.0367, 32.4250),
    "Peyia": (34.8833, 32.3833),
    "Kathikas": (34.9175, 32.4686),

    # East / villages
    "Ayia Napa": (34.9889, 34.0018),
    "Paralimni": (35.0394, 33.9819),
    "Deryneia": (35.0648, 33.9566),

    # Central / Troodos foothills
    "Kakopetria": (34.9894, 32.9033),
    "Platres": (34.8633, 32.8575)
}


# ================================
# Create map
# ================================
m = folium.Map(
    location=[35.1, 33.4],
    zoom_start=8,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri"
)

# ================================
# Predict & draw city circles
# ================================
for city, (lat, lon) in cities.items():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&daily=precipitation_sum"
        "&forecast_days=3"
        "&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    if "daily" not in data:
        print("FAILED:", city, response.status_code, data)
        continue

    daily_rain = data["daily"]["precipitation_sum"]

    rain_mm = daily_rain[-1]
    rain_3d = sum(daily_rain)

    time.sleep(0.2)

    X = pd.DataFrame({
        "rain_mm": [rain_mm],
        "rain_3d": [rain_3d]
    })

    # Risk levels
    if rain_3d < 20:
        color = "green"
        label = "Low Risk"
    elif rain_3d < 50:
        color = "orange"
        label = "Medium Risk"
    else:
        color = "red"
        label = "High Risk"

    folium.CircleMarker(
        location=[lat, lon],
        radius=8,           # 🔹 small circle
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=f"{city}: {label}"
    ).add_to(m)

# ================================
# Save map
# ================================
m.save("cyprus_flood_risk_cities.html")

print("🗺️ City flood risk map saved as cyprus_flood_risk_cities.html")