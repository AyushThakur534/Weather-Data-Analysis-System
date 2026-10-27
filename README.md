# WeatherScope — Weather Intelligence & Analytics Dashboard

A portfolio-quality Python weather analytics web app built with Streamlit, Pandas, NumPy, Plotly, and the Open-Meteo APIs.

## Features

- Search for a city using Open-Meteo geocoding.
- Live/current weather-model conditions.
- Hourly charts for temperature, precipitation probability, humidity, and wind.
- Daily forecast charts and a downloadable forecast CSV.
- Historical daily weather archive retrieval for a chosen date range.
- Historical temperature, precipitation, temperature-versus-rainfall, and correlation visualizations.
- Upload a CSV dataset and explore data quality, descriptive statistics, and charts.
- Download cleaned CSV, historical CSV, and forecast CSV.
- Responsive dark dashboard styling.
- No machine-learning temperature prediction.

## Requirements

- Python 3.11 or newer (Python 3.11–3.13 recommended for a predictable setup).
- Internet connection for live and historical API data.
- Windows, macOS, or Linux.

## Quick start (Windows PowerShell)

```powershell
cd WeatherScope
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, you can run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Quick start (macOS/Linux)

```bash
cd WeatherScope
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## How to use

1. Enter a city in the sidebar (the initial example is Ludhiana).
2. Choose the forecast horizon.
3. Inspect current conditions and the Live Overview tab.
4. Open Forecast to inspect daily highs/lows, precipitation, and UV index when available.
5. In Historical Analysis, select a date range and click **Load historical data**.
6. In Upload CSV, upload your own weather dataset to inspect missing values and descriptive statistics.
7. Use download buttons to export data.

## CSV dataset guidance

You can upload a CSV from a weather station, a course dataset, or a public data portal. Use a header row and a date/time column where possible.

Example compatible headers:

```csv
date,temperature,humidity,rainfall,wind_speed
2025-01-01,18.4,65,0.0,12.0
2025-01-02,20.1,58,2.2,10.5
2025-01-03,16.8,78,8.1,18.2
```

The numbers above are illustrative examples only, not real weather observations. The uploader recognizes common alternatives such as `datetime`, `temp`, `temperature_c`, `relative_humidity`, `rain_mm`, and `windspeed`. Unrecognized columns are preserved. The app does not invent or impute weather measurements.

For a real historical dataset, suitable sources include:
- Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api
- Open-Meteo API documentation: https://open-meteo.com/en/docs
- Official meteorological services or a dataset supplied by your instructor.

## API details

- Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
- Current and forecast: `https://api.open-meteo.com/v1/forecast`
- Historical archive: `https://archive-api.open-meteo.com/v1/archive`

The project uses HTTP requests with timeouts and Streamlit caching. API access requires internet connectivity. No API key is required for the standard Open-Meteo endpoints used here, subject to their applicable usage terms.

## Project structure

```text
WeatherScope/
├── app.py
├── requirements.txt
├── README.md
├── data/
└── assets/
```

The `data/` and `assets/` folders are intentionally included for your own datasets and design assets.

## Data handling and methodology

- Uploaded CSVs are parsed with Pandas.
- Common field names are normalized to consistent names.
- Numeric columns are converted to numeric types where recognized.
- Duplicate rows are removed from uploaded CSVs.
- Invalid dates and missing cells are reported rather than silently fabricated.
- Descriptive statistics, time-series trends, precipitation summaries, and correlations are visualized using Plotly.
- Historical archive values are reanalysis data; forecasts are model-based estimates. They are not guaranteed station observations.

## Troubleshooting

**`python` or `py` is not recognized**
- Install Python 3.11+ and select “Add Python to PATH” in the Windows installer.
- Reopen the terminal after installing Python.

**Streamlit command is not found**
- Activate `.venv`, then run `python -m streamlit run app.py`.

**API connection error**
- Check your internet connection, retry, and verify that your network allows access to Open-Meteo endpoints.
- Try a nearby major city if geocoding returns no match.

**Historical API returns no data**
- Check the selected date range and try a shorter range. Data availability varies by location and variable.

**CSV chart has no date axis**
- Ensure your file has a column named `date`, `time`, `datetime`, or `timestamp`. Otherwise, numeric distributions can still be visualized.

## Deployment

You can deploy the repository to Streamlit Community Cloud by pushing it to GitHub, selecting `app.py` as the app entry point, and using `requirements.txt` for dependencies. Do not commit private data or secrets. For public deployment, review Open-Meteo's current terms, attribution requirements, fair-use limits, and your application's expected request volume.

Streamlit deployment docs: https://docs.streamlit.io/deploy

## Academic project summary

**Title:** Weather Data Analysis System Using Python  
**Application name:** WeatherScope — Weather Intelligence & Analytics Dashboard  
**Objective:** Collect, validate, analyze, visualize, and export live, forecast, historical, and user-provided weather data in an interactive dashboard.  
**Tools:** Python, Streamlit, Pandas, NumPy, Plotly, Requests, Open-Meteo API.  
**Expected outcome:** An interactive dashboard that presents weather indicators, forecast trends, historical summaries, data-quality diagnostics, and downloadable datasets.

## License and attribution

This project code is provided as an educational starter project. Weather data is supplied by Open-Meteo; attribute the source and review its current terms: https://open-meteo.com/
