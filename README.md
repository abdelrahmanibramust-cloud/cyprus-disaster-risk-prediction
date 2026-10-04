# Cyprus Multi-Hazard Risk Prediction

Machine learning system that predicts flood and wildfire risk across Cyprus from weather data, and shows the results on interactive city maps (green = low, orange = medium, red = high).

Summer training project, Software Engineering, Near East University.

Live demo (Hugging Face Space): ADD-YOUR-LINK-HERE

## What it does

- Collects rainfall and weather data for both the northern and southern parts of Cyprus
- Engineers features that capture rainfall build-up, soil saturation and storm strength
- Trains and compares four models, then keeps the best one
- Serves predictions through a FastAPI backend deployed with Docker on Hugging Face Spaces
- Draws color-coded risk maps for 27 Cyprus cities

## Data

- CHIRPS rainfall data for Cyprus, 1981 to 2024 (259,921 rows: time, latitude, longitude, rain_mm, rain_3d, rain_7d)
- Hourly weather observations from the Open-Meteo API, 2020 to 2024 (temperature, humidity, wind speed, precipitation), used for wildfire
- Live forecasts from the Open-Meteo API for real-time predictions

## Method

1. Cleaned the data and removed missing values
2. Engineered features: rain_3d, rain_7d, soil saturation, rain intensity, storm index
3. Stratified 80/20 train/test split with a fixed random state (207,937 train rows, 51,984 test rows)
4. Trained Logistic Regression, Random Forest, Decision Tree and Gradient Boosting
5. Selected Gradient Boosting based on accuracy, precision, recall and F1-score
6. Saved the model with joblib and exposed it through FastAPI

## Tech stack

Python, pandas, NumPy, scikit-learn, XGBoost, joblib, FastAPI, Uvicorn, Folium, Leaflet, Docker, Hugging Face Spaces

## Run it locally

```
pip install -r requirements.txt
python cyprus_flood_map.py
python cyprus_wildfire_map.py
```

Run each script from the folder that contains its model file (`flood_model_cyprus.pkl` or `wildfire_model_cyprus.pkl`). Each script writes an HTML map; open it in your browser.

## Known limitations

- In the flood map, the circle colors currently come from rainfall thresholds applied to the live 3-day forecast (under 20 mm low, under 50 mm medium, otherwise high). The trained model is loaded but does not yet drive the colors.
- The wildfire map currently uses simulated weather values with small geographic variations, not live forecasts.
- Training data covers specific periods only (rainfall 1981 to 2024, wildfire weather 2020 to 2024).

## Next steps

- Feed live Open-Meteo forecasts into the wildfire map
- Let the trained flood model decide the flood risk colors
- Add a model comparison chart and test-set metrics to this README
