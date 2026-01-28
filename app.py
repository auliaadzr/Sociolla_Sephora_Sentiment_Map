import streamlit as st
import os
from streamlit_option_menu import option_menu
import sys
from Scraping import scrapping_data
from Cleaning import data_cleaning
from Visualisasi import rating_outlet
from Visualisasi import pie_chart
from Visualisasi import bar_chart
from GIS import GIS



st.set_page_config(
    page_title="Analisis Kepuasan Pelanggan",
    page_icon="📊",
    layout="wide"
)

with st.sidebar:
    selected = option_menu(
        "Dashboard",
        [
            "Beranda",
            "Scraping",
            "Cleaning",
            "Rating Outlet",
            "Pie Chart",
            "Bar Chart",
            "Peta GIS"
        ],
        icons=[
            "house",
            "cloud-download",
            "brush",
            "star-fill",
            "pie-chart-fill",
            "bar-chart-fill",
            "geo-alt-fill"
        ],
        menu_icon="grid",
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#FF69B4"},
        }
    )

st.title("📊 Analisis Kepuasan Pelanggan")
st.caption("Sociolla vs Sephora – Bandung")

# ======================
if selected == "Beranda":
    st.markdown("""
    Tujuan Aplikasi
    Aplikasi ini menganalisis kepuasan pelanggan berdasarkan:
    - Review pelanggan
    - Bayesian Rating
    - Visualisasi Grafik
    - Analisis Spasial (GIS)
    """)

# ======================
elif selected == "Scraping":
    if st.button("🕷️ Mulai Scraping"):
        scrapping_data.main()
        st.success("Scraping selesai")

# ======================
elif selected == "Cleaning":
    if st.button("🧹 Mulai Cleaning"):
        data_cleaning.main()
        st.success("Cleaning selesai")

# ======================
elif selected == "Rating Outlet":
    if st.button("⭐ Hitung Rating Outlet"):
        rating_outlet.main()
        st.success("Rating outlet selesai")

# ======================
elif selected == "Pie Chart":
    pie_chart.main()
    st.image("Data/Visualisasi/perbandingan_kepuasan_outlet.png")

# ======================
elif selected == "Bar Chart":
    bar_chart.main()
    st.image("Data/Visualisasi/bar_chart_rating.png")

# ======================
elif selected == "Peta GIS":
    st.subheader("🗺️ Peta Outlet Rating Tinggi")

    user_lat = st.number_input("Latitude Anda", value=-6.9175)
    user_lon = st.number_input("Longitude Anda", value=107.6191)
    min_rating = st.slider("Minimal Rating Outlet", 3.0, 5.0, 4.3)

    if st.button("Tampilkan Peta"):
        GIS.main(user_lat, user_lon, min_rating)

    map_path = "Data/Visualisasi/peta_outlet_final.html"
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600)


