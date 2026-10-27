
from datetime import date, timedelta
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="WeatherScope | Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

C = {
    "blue": "#3478F6",
    "navy": "#16365C",
    "cyan": "#0FA9B7",
    "orange": "#E99A32",
    "text": "#172B4D",
    "muted": "#6A7F96",
    "grid": "#E5EDF5",
}

WEATHER = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Light rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Moderate snow", "🌨️"),
    75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Heavy rain showers", "⛈️"),
    85: ("Snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Severe thunderstorm", "⛈️"),
}


# -------------------- DESIGN SYSTEM --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root { color-scheme: light; }

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #e0efff 0%, transparent 35%),
        linear-gradient(180deg, #f8fbff 0%, #f1f6fc 100%);
    color: #172b4d;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #172b4d;
    letter-spacing: -0.035em;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e4edf6;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #f9fcff);
    border: 1px solid #e0eaf5;
    border-radius: 18px;
    padding: 20px;
    min-height: 120px;
    box-shadow: 0 8px 25px rgba(38, 75, 115, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #6a7f96;
    font-size: 0.88rem;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #172b4d;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

.hero {
    background: linear-gradient(120deg, #102d52, #174c80 55%, #217b9c);
    border-radius: 26px;
    padding: 34px;
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 18px 40px rgba(24, 68, 112, 0.15);
}

.hero:after {
    content: '☀';
    position: absolute;
    right: 35px;
    top: -45px;
    font-size: 190px;
    color: rgba(255,255,255,0.07);
}

.eyebrow {
    color: #8de7e6;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

.hero-title {
    color: white;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800;
    line-height: 1.12;
    margin: 12px 0;
    position: relative;
    z-index: 1;
}

.hero-sub {
    color: #d3e4f5;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 700px;
    position: relative;
    z-index: 1;
}

.section-label {
    color: #6e849b;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 15px 0 12px;
}

div[data-testid="stTabs"] button {
    font-weight: 700;
    color: #657a91;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2468d9;
    border-bottom-color: #3478f6;
}

.stButton button, .stDownloadButton button {
    border-radius: 11px;
    font-weight: 700;
    min-height: 2.7rem;
    transition: 0.2s ease;
}

.stButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 7px 16px rgba(52,120,246,0.14);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #e0eaf5;
    border-radius: 14px;
    overflow: hidden;
}

div[data-testid="stExpander"] {
    border: 1px solid #e0eaf5;
    border-radius: 14px;
    background: rgba(255,255,255,0.75);
}

div[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #b7cce2;
    border-radius: 16px;
    padding: 12px;
}

hr { border-color: #e1eaf4; }

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 23px;
        border-radius: 20px;
    }
    .hero:after {
        right: -30px;
        font-size: 140px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- API HELPERS --------------------

def api_get(url, params):
    try:
        response = requests.get(
            url,
            params=params,
            timeout=25,
            headers={"User-Agent": "WeatherScope/1.0"},
        )
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            raise RuntimeError(data.get("reason", "Weather API error."))

        return data

    except requests.Timeout:
        raise RuntimeError("The weather service timed out. Please try again.")
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to the weather service: {exc}"
        )


@st.cache_data(ttl=3600, show_spinner=False)
def find_city(city):
    data = api_get(GEO_URL, {
        "name": city,
        "count": 10,
        "language": "en",
        "format": "json",
    })

    results = data.get("results", [])

    if not results:
        raise RuntimeError(f"No location found for '{city}'.")

    item = next(
        (x for x in results
         if x.get("name", "").casefold() == city.casefold()),
        results[0],
    )

    return {
        "name": item.get("name", city),
        "region": item.get("admin1", ""),
        "country": item.get("country", ""),
        "lat": item["latitude"],
        "lon": item["longitude"],
        "timezone": item.get("timezone", "auto"),
    }


@st.cache_data(ttl=900, show_spinner=False)
def get_forecast(lat, lon, timezone, days):
    return api_get(FORECAST_URL, {
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone or "auto",
        "forecast_days": days,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "is_day,precipitation,weather_code,cloud_cover,pressure_msl,"
            "wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        ),
        "hourly": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "precipitation_probability,precipitation,weather_code,"
            "cloud_cover,wind_speed_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "apparent_temperature_max,apparent_temperature_min,"
            "sunrise,sunset,uv_index_max,precipitation_sum,"
            "precipitation_probability_max,wind_speed_10m_max"
        ),
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
    })


@st.cache_data(ttl=3600, show_spinner=False)
def get_history(lat, lon, start, end, timezone):
    data = api_get(ARCHIVE_URL, {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "timezone": timezone or "auto",
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "temperature_2m_mean,precipitation_sum,rain_sum,"
            "precipitation_hours,wind_speed_10m_max"
        ),
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
    })

    daily = data.get("daily", {})

    if not daily or not daily.get("time"):
        return pd.DataFrame()

    df = pd.DataFrame(daily)
    df["date"] = pd.to_datetime(df.pop("time"), errors="coerce")
    return df


def condition(code):
    if pd.isna(code):
        return "Unknown"
    return WEATHER.get(int(code), ("Unknown", "🌡️"))[0]


def weather_icon(code):
    if pd.isna(code):
        return "🌡️"
    return WEATHER.get(int(code), ("Unknown", "🌡️"))[1]


def number(value, unit="", digits=1):
    try:
        if value is None or pd.isna(value):
            return "—"
        return f"{float(value):.{digits}f}{unit}"
    except (ValueError, TypeError):
        return "—"


def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="DM Sans", color=C["text"]),
        margin=dict(l=12, r=12, t=55, b=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hovermode="x unified",
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=C["grid"],
        tickfont=dict(color=C["muted"]),
    )

    fig.update_yaxes(
        gridcolor=C["grid"],
        zerolinecolor=C["grid"],
        tickfont=dict(color=C["muted"]),
    )

    return fig


def metric(label, value, help_text=None):
    st.metric(label, value, help=help_text)


def normalize_csv(raw):
    df = pd.read_csv(BytesIO(raw))

    if df.empty:
        raise ValueError("This CSV file has no rows.")

    aliases = {
        "date": ["date", "time", "datetime", "timestamp"],
        "temperature_2m_mean": [
            "temperature_2m_mean", "temperature", "temp",
            "temperature_c", "mean_temperature", "avg_temp",
        ],
        "temperature_2m_max": [
            "temperature_2m_max", "max_temperature", "temp_max",
        ],
        "temperature_2m_min": [
            "temperature_2m_min", "min_temperature", "temp_min",
        ],
        "relative_humidity_2m_mean": [
            "relative_humidity_2m_mean", "humidity",
            "relative_humidity", "humidity_percent",
        ],
        "precipitation_sum": [
            "precipitation_sum", "rainfall", "rainfall_mm",
            "precipitation", "rain", "rain_mm",
        ],
        "wind_speed_10m_max": [
            "wind_speed_10m_max", "wind_speed", "windspeed", "wind_kmh",
        ],
    }

    lookup = {
        str(c).strip().lower().replace(" ", "_"): c
        for c in df.columns
    }

    rename = {}

    for target, candidates in aliases.items():
        for candidate in candidates:
            if candidate in lookup:
                rename[lookup[candidate]] = target
                break

    df = df.rename(columns=rename)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in [
        "temperature_2m_mean", "temperature_2m_max",
        "temperature_2m_min", "relative_humidity_2m_mean",
        "precipitation_sum", "wind_speed_10m_max",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates()

    return df, duplicate_count


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 🌦️ WeatherScope")
    st.caption("Weather intelligence & analytics")
    st.divider()

    st.markdown("### 📍 Location")
    city = st.text_input("Search city", value="Ludhiana")

    forecast_days = st.slider(
        "Forecast horizon",
        min_value=1,
        max_value=16,
        value=7,
        format="%d days",
    )

    st.divider()
    st.markdown("### 📅 Historical data")

    today = date.today()
    history_end_default = today - timedelta(days=5)
    history_start_default = history_end_default - timedelta(days=89)

    history_start = st.date_input(
        "Start date",
        value=history_start_default,
        max_value=history_end_default,
    )

    history_end = st.date_input(
        "End date",
        value=history_end_default,
        min_value=history_start,
        max_value=history_end_default,
    )

    if st.button("↻ Refresh weather", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.caption("Weather data powered by Open-Meteo.")
    st.caption("For educational and informational use.")


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">WEATHER INTELLIGENCE PLATFORM     AYUSH THAKUR</div>
    <div class="hero-title">
        Understand the weather.<br>
        See the bigger picture.
    </div>
    <div class="hero-sub">
        Explore live conditions, upcoming forecasts, historical patterns,
        and your own weather datasets — all in one workspace.
    </div>
</div>
""", unsafe_allow_html=True)


if not city.strip():
    st.info("Enter a city name in the sidebar.")
    st.stop()

try:
    with st.spinner(f"Loading weather for {city}..."):
        location = find_city(city.strip())

        forecast = get_forecast(
            location["lat"],
            location["lon"],
            location["timezone"],
            forecast_days,
        )

except RuntimeError as exc:
    st.error(str(exc))
    st.info("Check your internet connection and try again.")
    st.stop()


place = ", ".join(
    x for x in [
        location["name"],
        location["region"],
        location["country"],
    ] if x
)

current = forecast.get("current", {})
current_time = current.get("time", "Unavailable")
current_code = current.get("weather_code")

st.markdown(
    f"## {weather_icon(current_code)} {place}"
)

st.caption(
    f"Local model time: {current_time}  ·  "
    f"{location['lat']:.3f}, {location['lon']:.3f}  ·  "
    f"Time zone: {location['timezone']}"
)


# -------------------- CURRENT WEATHER --------------------

st.markdown(
    '<div class="section-label">CURRENT CONDITIONS</div>',
    unsafe_allow_html=True,
)

columns = st.columns(5)

with columns[0]:
    metric("Temperature", number(current.get("temperature_2m"), " °C"))

with columns[1]:
    metric("Feels like", number(current.get("apparent_temperature"), " °C"))

with columns[2]:
    metric("Humidity", number(current.get("relative_humidity_2m"), "%", 0))

with columns[3]:
    metric("Wind speed", number(current.get("wind_speed_10m"), " km/h"))

with columns[4]:
    metric("Precipitation", number(current.get("precipitation"), " mm"))

with st.expander("View additional atmospheric measurements"):
    extra = st.columns(4)

    values = [
        ("Pressure", current.get("pressure_msl"), " hPa"),
        ("Cloud cover", current.get("cloud_cover"), "%"),
        ("Wind gusts", current.get("wind_gusts_10m"), " km/h"),
        ("Wind direction", current.get("wind_direction_10m"), "°"),
    ]

    for i, (label, value, unit) in enumerate(values):
        with extra[i]:
            metric(label, number(value, unit))


st.divider()

live_tab, forecast_tab, history_tab, upload_tab, about_tab = st.tabs([
    "🌤️ Live Overview",
    "📆 Forecast",
    "📈 Historical Analysis",
    "📂 CSV Explorer",
    "ℹ️ About",
])


# -------------------- LIVE OVERVIEW --------------------

with live_tab:
    st.markdown("### Today's weather")
    st.caption("Explore the hourly weather outlook for the selected location.")

    hourly = pd.DataFrame(forecast.get("hourly", {}))

    if not hourly.empty:
        hourly["time"] = pd.to_datetime(hourly["time"], errors="coerce")

        current_dt = pd.to_datetime(current_time, errors="coerce")

        if pd.notna(current_dt):
            day_data = hourly[
                hourly["time"].dt.date == current_dt.date()
            ].copy()
        else:
            day_data = hourly.head(24).copy()

        if day_data.empty:
            day_data = hourly.head(24).copy()

        left, right = st.columns([1.5, 1])

        with left:
            if "temperature_2m" in day_data:
                fig = px.area(
                    day_data,
                    x="time",
                    y="temperature_2m",
                    title="Hourly temperature",
                    labels={
                        "time": "Local time",
                        "temperature_2m": "Temperature (°C)",
                    },
                )

                fig.update_traces(
                    line_color=C["blue"],
                    fillcolor="rgba(52,120,246,0.14)",
                )

                st.plotly_chart(
                    style_chart(fig, 350),
                    use_container_width=True,
                )

        with right:
            if "precipitation_probability" in day_data:
                fig = px.bar(
                    day_data,
                    x="time",
                    y="precipitation_probability",
                    title="Chance of precipitation",
                    labels={
                        "time": "Local time",
                        "precipitation_probability": "Probability (%)",
                    },
                )

                fig.update_traces(marker_color=C["cyan"])

                st.plotly_chart(
                    style_chart(fig, 350),
                    use_container_width=True,
                )

        if {
            "relative_humidity_2m",
            "wind_speed_10m",
        }.issubset(day_data.columns):
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=day_data["time"],
                y=day_data["relative_humidity_2m"],
                name="Humidity (%)",
                mode="lines",
                line=dict(color=C["cyan"], width=3),
            ))

            fig.add_trace(go.Scatter(
                x=day_data["time"],
                y=day_data["wind_speed_10m"],
                name="Wind (km/h)",
                mode="lines",
                yaxis="y2",
                line=dict(color=C["orange"], width=3),
            ))

            fig.update_layout(
                title="Humidity and wind",
                yaxis=dict(title="Humidity (%)"),
                yaxis2=dict(
                    title="Wind speed (km/h)",
                    overlaying="y",
                    side="right",
                ),
            )

            st.plotly_chart(
                style_chart(fig, 330),
                use_container_width=True,
            )

    daily = pd.DataFrame(forecast.get("daily", {}))

    if not daily.empty:
        daily["time"] = pd.to_datetime(daily["time"], errors="coerce")
        daily["Condition"] = daily["weather_code"].apply(condition)

        show = [
            c for c in [
                "time", "Condition",
                "temperature_2m_min", "temperature_2m_max",
                "precipitation_sum", "precipitation_probability_max",
                "wind_speed_10m_max",
            ] if c in daily.columns
        ]

        st.markdown("### Forecast at a glance")

        st.dataframe(
            daily[show].rename(columns={
                "time": "Date",
                "temperature_2m_min": "Low (°C)",
                "temperature_2m_max": "High (°C)",
                "precipitation_sum": "Rain (mm)",
                "precipitation_probability_max": "Rain chance (%)",
                "wind_speed_10m_max": "Max wind (km/h)",
            }),
            use_container_width=True,
            hide_index=True,
        )


# -------------------- FORECAST --------------------

with forecast_tab:
    st.markdown("### Forecast explorer")
    st.caption("Forecast values are model estimates and may change as models update.")

    daily = pd.DataFrame(forecast.get("daily", {}))

    if not daily.empty:
        daily["time"] = pd.to_datetime(daily["time"], errors="coerce")

        left, right = st.columns(2)

        with left:
            if {
                "temperature_2m_min",
                "temperature_2m_max",
            }.issubset(daily.columns):
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=daily["time"],
                    y=daily["temperature_2m_max"],
                    name="Daily high",
                    mode="lines+markers",
                    line=dict(color=C["orange"], width=3),
                ))

                fig.add_trace(go.Scatter(
                    x=daily["time"],
                    y=daily["temperature_2m_min"],
                    name="Daily low",
                    mode="lines+markers",
                    line=dict(color=C["blue"], width=3),
                ))

                fig.update_layout(
                    title="Daily temperature range",
                    yaxis_title="Temperature (°C)",
                )

                st.plotly_chart(
                    style_chart(fig, 370),
                    use_container_width=True,
                )

        with right:
            if "precipitation_sum" in daily:
                fig = px.bar(
                    daily,
                    x="time",
                    y="precipitation_sum",
                    title="Expected daily precipitation",
                    labels={
                        "time": "Date",
                        "precipitation_sum": "Precipitation (mm)",
                    },
                )

                fig.update_traces(marker_color=C["cyan"])

                st.plotly_chart(
                    style_chart(fig, 370),
                    use_container_width=True,
                )

        if "uv_index_max" in daily:
            fig = px.line(
                daily,
                x="time",
                y="uv_index_max",
                markers=True,
                title="Daily maximum UV index",
                labels={
                    "time": "Date",
                    "uv_index_max": "UV index",
                },
            )

            fig.update_traces(line_color=C["orange"])

            st.plotly_chart(
                style_chart(fig, 300),
                use_container_width=True,
            )

        daily["Condition"] = daily["weather_code"].apply(condition)

        if "sunrise" in daily and "sunset" in daily:
            daily["Sunrise"] = pd.to_datetime(
                daily["sunrise"], errors="coerce"
            ).dt.strftime("%H:%M")

            daily["Sunset"] = pd.to_datetime(
                daily["sunset"], errors="coerce"
            ).dt.strftime("%H:%M")

        show = [
            c for c in [
                "time", "Condition",
                "temperature_2m_min", "temperature_2m_max",
                "apparent_temperature_min", "apparent_temperature_max",
                "precipitation_probability_max", "precipitation_sum",
                "wind_speed_10m_max", "uv_index_max",
                "Sunrise", "Sunset",
            ] if c in daily.columns
        ]

        st.dataframe(
            daily[show].rename(columns={
                "time": "Date",
                "temperature_2m_min": "Low °C",
                "temperature_2m_max": "High °C",
                "apparent_temperature_min": "Feels-like low °C",
                "apparent_temperature_max": "Feels-like high °C",
                "precipitation_probability_max": "Rain chance %",
                "precipitation_sum": "Rain mm",
                "wind_speed_10m_max": "Max wind km/h",
                "uv_index_max": "Max UV",
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇ Download forecast CSV",
            data=daily.to_csv(index=False).encode("utf-8"),
            file_name="weatherscope_forecast.csv",
            mime="text/csv",
        )


# -------------------- HISTORICAL ANALYSIS --------------------

with history_tab:
    st.markdown("### Historical weather analytics")
    st.write(
        "Retrieve historical daily weather data for the selected location "
        "and date range."
    )

    if st.button("Load historical data", type="primary"):
        if history_start > history_end:
            st.error("The start date must not be after the end date.")
        else:
            try:
                with st.spinner("Retrieving historical weather data..."):
                    history = get_history(
                        location["lat"],
                        location["lon"],
                        history_start.isoformat(),
                        history_end.isoformat(),
                        location["timezone"],
                    )

                st.session_state["weather_history"] = history

            except RuntimeError as exc:
                st.error(str(exc))

    history = st.session_state.get("weather_history")

    if history is not None and not history.empty:
        temp_col = (
            "temperature_2m_mean"
            if "temperature_2m_mean" in history
            else "temperature_2m_max"
        )

        rain_col = (
            "precipitation_sum"
            if "precipitation_sum" in history
            else None
        )

        stats = st.columns(4)

        with stats[0]:
            metric("Records", f"{len(history):,}")

        with stats[1]:
            metric(
                "Average temperature",
                number(history[temp_col].mean(), " °C"),
            )

        with stats[2]:
            maximum = (
                history["temperature_2m_max"].max()
                if "temperature_2m_max" in history
                else np.nan
            )
            metric("Highest temperature", number(maximum, " °C"))

        with stats[3]:
            total_rain = (
                history[rain_col].sum()
                if rain_col else np.nan
            )
            metric("Total precipitation", number(total_rain, " mm"))

        temp_fields = [
            c for c in [
                "temperature_2m_min",
                "temperature_2m_mean",
                "temperature_2m_max",
            ] if c in history.columns
        ]

        if temp_fields:
            fig = px.line(
                history,
                x="date",
                y=temp_fields,
                title="Historical temperature trends",
                labels={
                    "date": "Date",
                    "value": "Temperature (°C)",
                    "variable": "Measure",
                },
            )

            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True,
            )

        if rain_col:
            fig = px.bar(
                history,
                x="date",
                y=rain_col,
                title="Daily precipitation",
                labels={
                    "date": "Date",
                    rain_col: "Precipitation (mm)",
                },
            )

            fig.update_traces(marker_color=C["cyan"])

            st.plotly_chart(
                style_chart(fig, 340),
                use_container_width=True,
            )

        if temp_col and rain_col:
            fig = px.scatter(
                history,
                x=temp_col,
                y=rain_col,
                hover_data=["date"],
                title="Temperature versus precipitation",
                labels={
                    temp_col: "Temperature (°C)",
                    rain_col: "Precipitation (mm)",
                },
            )

            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True,
            )

        numeric = history.select_dtypes(include=np.number)

        if numeric.shape[1] >= 2:
            corr = numeric.corr()

            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Weather variable correlation matrix",
            )

            st.plotly_chart(
                style_chart(fig, 420),
                use_container_width=True,
            )

        with st.expander("View historical records"):
            st.dataframe(
                history,
                use_container_width=True,
                hide_index=True,
            )

        st.download_button(
            "⬇ Download historical CSV",
            data=history.to_csv(index=False).encode("utf-8"),
            file_name="weatherscope_historical_data.csv",
            mime="text/csv",
        )

    elif history is not None:
        st.warning("No historical data was returned for this date range.")


# -------------------- CSV EXPLORER --------------------

with upload_tab:
    st.markdown("### Explore your weather dataset")

    st.write(
        "Upload a CSV from a weather station, public dataset, "
        "or your coursework project."
    )

    st.info(
        "Common fields include date, temperature, humidity, rainfall, "
        "and wind speed. Missing measurements are reported, not invented."
    )

    uploaded = st.file_uploader(
        "Upload weather CSV",
        type=["csv"],
    )

    if uploaded is not None:
        try:
            df, duplicates = normalize_csv(uploaded.getvalue())

            a, b, c, d = st.columns(4)

            with a:
                metric("Rows", f"{len(df):,}")

            with b:
                metric("Columns", str(len(df.columns)))

            with c:
                metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

            with d:
                metric("Duplicates removed", str(duplicates))

            st.markdown("#### Data quality report")

            summary = pd.DataFrame({
                "Column": df.columns,
                "Type": [str(df[col].dtype) for col in df.columns],
                "Missing values": [
                    int(df[col].isna().sum()) for col in df.columns
                ],
                "Missing (%)": [
                    round(df[col].isna().mean() * 100, 2)
                    for col in df.columns
                ],
                "Unique values": [
                    int(df[col].nunique()) for col in df.columns
                ],
            })

            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True,
            )

            numeric_cols = df.select_dtypes(
                include=np.number
            ).columns.tolist()

            if numeric_cols:
                selected = st.selectbox(
                    "Select a numeric variable",
                    numeric_cols,
                )

                if "date" in df.columns and df["date"].notna().any():
                    chart_data = df.dropna(subset=["date"]).sort_values("date")

                    fig = px.line(
                        chart_data,
                        x="date",
                        y=selected,
                        markers=True,
                        title=f"{selected.replace('_', ' ').title()} over time",
                    )
                else:
                    fig = px.histogram(
                        df,
                        x=selected,
                        nbins=30,
                        title=f"Distribution of {selected}",
                    )

                st.plotly_chart(
                    style_chart(fig, 370),
                    use_container_width=True,
                )

                st.markdown("#### Descriptive statistics")

                st.dataframe(
                    df[numeric_cols].describe().T,
                    use_container_width=True,
                )

            with st.expander("Preview uploaded records"):
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

            st.download_button(
                "⬇ Download cleaned CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="weatherscope_cleaned_data.csv",
                mime="text/csv",
            )

        except Exception as exc:
            st.error(f"Could not process this CSV: {exc}")


# -------------------- ABOUT --------------------

with about_tab:
    st.markdown("### About WeatherScope")

    st.write(
        "WeatherScope is a Python-based weather data analysis system "
        "that combines live conditions, forecasts, historical records, "
        "and uploaded CSV datasets in an interactive dashboard."
    )

    st.markdown("#### Analysis workflow")

    st.markdown("""
    **01 — Data collection**  
    Retrieve live, forecast, and historical data from Open-Meteo.

    **02 — Data preprocessing**  
    Parse dates, normalize column names, convert numeric fields,
    identify missing values, and remove duplicate uploaded rows.

    **03 — Exploratory analysis**  
    Calculate descriptive statistics, inspect weather trends,
    compare precipitation, and examine correlations.

    **04 — Data visualization**  
    Display interactive charts and data tables with Plotly.

    **05 — Export**  
    Download historical data, forecasts, and cleaned CSV files.
    """)

    st.markdown("#### Important limitations")

    st.markdown("""
    - Weather forecasts are model-based estimates and can change.
    - Historical archive values may differ from local station readings.
    - Correlation does not prove causation.
    - This application does not perform machine-learning prediction.
    - It is not intended for emergency or safety-critical decisions.
    """)

    st.markdown(
        "Weather data: [Open-Meteo](https://open-meteo.com/)  \n"
        "[Forecast API documentation](https://open-meteo.com/en/docs)  \n"
        "[Historical API documentation](https://open-meteo.com/en/docs/historical-weather-api)"
    )


# -------------------- FOOTER --------------------

st.markdown("---")

left, right = st.columns(2)

with left:
    st.caption("🌦️ WeatherScope · Weather intelligence & analytics")

with right:
    st.caption("Built with Python · Streamlit · Pandas · Plotly · Open-Meteo")
