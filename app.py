import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Used Vehicle Market Analysis',
    page_icon='🚗',
    layout='wide'
)

# =================
# DATA LOADING
# =================


@st.cache_data
def load_data():
    data = pd.read_csv('vehicles_us.csv')

    # Limpieza básica
    data['model_year'] = data['model_year'].fillna(data['model_year'].median())
    data['odometer'] = data['odometer'].fillna(data['odometer'].median())
    data['paint_color'] = data['paint_color'].fillna('unknown')
    data['is_4wd'] = data['is_4wd'].fillna(0)

    # Convert date
    data['date_posted'] = pd.to_datetime(data['date_posted'])

    return data


car_data = load_data()

# ==================
# TITLE
# ==================
st.title('🚗 Used Vehicle Market Analysis')

st.write(
    """
    This interactive dashboard allows users to explore a dataset of used vehicle listings
    in the United States. Analyze pricing, mileage, vehicle types, and market trends
    through interactive visualizations.
    """
)

st.markdown("---")

# ==================
# SIDEBAR FILTERS
# ==================
st.sidebar.header('Filters')

min_year = int(car_data['model_year'].min())
max_year = int(car_data['model_year'].max())

year_range = st.sidebar.slider(
    'Model Year Range',
    min_year,
    max_year,
    (min_year, max_year)
)

filtered_data = car_data[
    (car_data["model_year"] >= year_range[0]) &
    (car_data["model_year"] <= year_range[1])
]

st.subheader("Dataset Preview")
st.dataframe(filtered_data.head())

st.subheader("Mileage Distribution")
fig_hist = px.histogram(
    filtered_data,
    x="odometer",
    nbins=50,
    title="Distribution of Vehicle Mileage"
)
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Price vs Mileage")
fig_scatter = px.scatter(
    filtered_data,
    x="odometer",
    y="price",
    color="type",
    title="Vehicle Price vs Mileage",
    labels={"odometer": "Mileage", "price": "Price"}
)
st.plotly_chart(fig_scatter, use_container_width=True)
