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
import pandas as pd
import time 

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
    st.subheader("🕷️ Scraping Review Produk")

    st.info(
        "⚠️ Proses scraping mengakses API pihak ketiga (Sociolla & Sephora).\n"
        "Gunakan tombol ini seperlunya untuk menghindari pembatasan API."
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    scraping_path = os.path.join(BASE_DIR, "Data", "Raw", "data_scrapping.csv")

    # TOMBOL SELALU ADA (ambil / update data)
    if st.button("🔄 Ambil / Perbarui Data Scraping Terbaru"):
        with st.spinner("⏳ Sedang melakukan scraping review..."):
            scrapping_data.main()
        st.success("✅ Scraping selesai! Data berhasil diperbarui.")

    # JIKA DATA SUDAH ADA → TAMPILKAN
    if os.path.exists(scraping_path):
        df_scrap = pd.read_csv(scraping_path)

        # Informasi metadata
        last_update = os.path.getmtime(scraping_path)
        st.caption(f"🕒 Terakhir diperbarui: {time.ctime(last_update)}")
        st.caption(f"📄 Total review: {len(df_scrap)}")

        st.dataframe(df_scrap, use_container_width=True)

        st.download_button(
            label="⬇️ Download Data Scraping",
            data=df_scrap.to_csv(index=False),
            file_name="data_scrapping.csv",
            mime="text/csv"
        )

    else:
        st.warning("📂 Data scraping belum tersedia. Silakan klik tombol di atas.")


# ======================
elif selected == "Cleaning":
    st.subheader("🧹 Data Cleaning Review")

    st.info(
        "ℹ️ Proses cleaning mengolah data hasil scraping:\n"
        "- Menghapus duplikasi\n"
        "- Normalisasi teks ulasan\n\n"
        "Pastikan data scraping sudah tersedia sebelum menjalankan cleaning."
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(BASE_DIR, "Data", "Raw", "data_scrapping.csv")
    clean_path = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")

    # Tombol SELALU ADA
    if st.button("🔄 Jalankan / Perbarui Data Cleaning"):
        if not os.path.exists(raw_path):
            st.error("❌ Data scraping belum tersedia. Silakan jalankan scraping terlebih dahulu.")
        else:
            with st.spinner("⏳ Sedang membersihkan data..."):
                data_cleaning.main()
            st.success("✅ Data cleaning selesai!")

    # JIKA DATA CLEAN SUDAH ADA → TAMPILKAN
    if os.path.exists(clean_path):
        df_clean = pd.read_csv(clean_path)

        # Metadata
        last_update = os.path.getmtime(clean_path)
        st.caption(f"🕒 Terakhir diperbarui: {time.ctime(last_update)}")
        st.caption(f"📄 Total data bersih: {len(df_clean)} baris")

        st.dataframe(df_clean, use_container_width=True)

        st.download_button(
            label="⬇️ Download Data Cleaning",
            data=df_clean.to_csv(index=False),
            file_name="data_cleaning.csv",
            mime="text/csv"
        )

    else:
        st.warning("📂 Data cleaning belum tersedia. Silakan klik tombol di atas.")

# ======================
elif selected == "Rating Outlet":
    st.subheader("⭐ Rating Outlet (Bayesian Average)")

    st.info(
        "ℹ️ Rating outlet dihitung menggunakan metode Bayesian Average.\n"
        "Data ini berasal dari hasil cleaning review dan digunakan\n"
        "sebagai dasar visualisasi dan analisis GIS."
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    clean_path = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")
    rating_path = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")

    # TOMBOL SELALU ADA
    if st.button("🔄 Hitung / Perbarui Rating Outlet"):
        if not os.path.exists(clean_path):
            st.error("❌ Data cleaning belum tersedia. Silakan jalankan cleaning terlebih dahulu.")
        else:
            with st.spinner("⏳ Menghitung rating outlet..."):
                rating_outlet.main()
            st.success("✅ Rating outlet berhasil diperbarui!")

    # JIKA DATA RATING SUDAH ADA → TAMPILKAN
    if os.path.exists(rating_path):
        df_rating = pd.read_csv(rating_path)

        # Metadata
        last_update = os.path.getmtime(rating_path)
        st.caption(f"🕒 Terakhir diperbarui: {time.ctime(last_update)}")
        st.caption(f"🏬 Total outlet: {df_rating['outlet_id'].nunique()}")

        st.dataframe(df_rating, use_container_width=True)

        st.download_button(
            label="⬇️ Download Data Rating Outlet",
            data=df_rating.to_csv(index=False),
            file_name="data_rating_outlet.csv",
            mime="text/csv"
        )

    else:
        st.warning("📂 Data rating outlet belum tersedia. Silakan klik tombol di atas.")

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
    st.subheader("🗺️ Peta Outlet dengan Rating Tinggi")

    st.info(
        "ℹ️ Peta menampilkan outlet Sociolla & Sephora berdasarkan rating.\n"
        "Marker biru = lokasi Anda, pink/black = outlet."
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(BASE_DIR, "Data", "Visualisasi", "peta_outlet_final.html")
    rating_path = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")

    # =====================
    # Input lokasi & rating
    # =====================
    col1, col2, col3 = st.columns(3)
    with col1:
        user_lat = st.number_input("📍 Latitude", value=-6.9175, format="%.6f")
    with col2:
        user_lon = st.number_input("📍 Longitude", value=107.6191, format="%.6f")
    with col3:
        min_rating = st.slider("⭐ Minimal Rating Outlet", 3.0, 5.0, 4.3)

    # =====================
    # Tombol Generate / Perbarui Peta
    # =====================
    if st.button("🗺️ Tampilkan / Perbarui Peta"):
        if not os.path.exists(rating_path):
            st.error("❌ Data rating outlet belum tersedia. Jalankan Rating Outlet terlebih dahulu.")
        else:
            with st.spinner("⏳ Membuat peta GIS..."):
                GIS.main(user_lat, user_lon, min_rating)
            st.success("✅ Peta berhasil diperbarui!")

    # =====================
    # Tampilkan peta jika tersedia
    # =====================
    if os.path.exists(map_path):
        last_update = os.path.getmtime(map_path)
        st.caption(f"🕒 Terakhir diperbarui: {time.ctime(last_update)}")

        with open(map_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600)

        with open(map_path, "rb") as f:
            st.download_button(
                "⬇️ Download Peta (HTML)",
                f,
                file_name="peta_outlet_rating.html",
                mime="text/html"
            )
    else:
        st.warning("📂 Peta belum tersedia. Silakan klik tombol di atas.")


