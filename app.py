import streamlit as st
import os
import sys
import pandas as pd
import time 
from streamlit_option_menu import option_menu
from Scraping import scraping_data
from Cleaning import cleaning
from Visualisasi import rating_outlet
from Visualisasi import pie_chart
from Visualisasi import bar_chart
from GIS import gis

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

# ======================
if selected == "Beranda":
    st.title("💄 Sociolla vs Sephora")
    st.subheader("Analisis Kepuasan Pelanggan Retail Kecantikan di Bandung")

    st.markdown("""
    Aplikasi ini menyajikan analisis kepuasan pelanggan berdasarkan **ulasan nyata konsumen**
    dengan pendekatan statistik dan visualisasi interaktif untuk memahami performa outlet
    secara objektif dan informatif.
    """)

    st.markdown("### 🎯 Tujuan Aplikasi")
    st.markdown("""
    - Membandingkan tingkat kepuasan pelanggan antara **Sociolla** dan **Sephora**
    - Menyediakan **rating outlet** yang tidak tersedia di website resmi
    - Menampilkan hasil analisis secara **visual dan mudah dipahami**
    """)

    st.markdown("### ✨ Fitur Utama")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        📝 **Analisis Review Pelanggan**  
        Mengolah ulasan konsumen sebagai dasar penilaian kepuasan
        
        ⭐ **Bayesian Rating Outlet**  
        Rating outlet yang lebih adil dan stabil
        """)

    with col2:
        st.markdown("""
        📊 **Visualisasi Interaktif**  
        Pie Chart & Bar Chart untuk perbandingan performa
        
        🗺️ **Peta GIS Interaktif**  
        Lokasi outlet, rating, jarak, dan 7 produk best seller
        """)

    st.markdown("---")
    st.caption("Gunakan menu di sebelah kiri untuk mulai menjelajahi hasil analisis ✨")

# ======================
elif selected == "Scraping":
    st.subheader("Scraping Review Produk")

    st.info(
        "⚠️ Proses scraping mengakses API pihak ketiga (Sociolla & Sephora).\n"
        "Gunakan tombol ini seperlunya untuk menghindari pembatasan API."
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    scraping_path = os.path.join(BASE_DIR, "Data", "Raw", "data_scraping.csv")

    # ambil / update data
    if st.button("🔄 Ambil / Perbarui Data Scraping Terbaru"):
        with st.spinner("⏳ Sedang melakukan scraping review..."):
            scraping_data.main()
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
            file_name="data_scraping.csv",
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
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(BASE_DIR, "Data", "Raw", "data_scraping.csv")
    clean_path = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")

    # Tombol SELALU ADA
    if st.button("🔄 Jalankan / Perbarui Data Cleaning"):
        if not os.path.exists(raw_path):
            st.error("❌ Data scraping belum tersedia. Silakan jalankan scraping terlebih dahulu.")
        else:
            with st.spinner("⏳ Sedang membersihkan data..."):
                cleaning.main()
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
    st.subheader("⭐ Rating Outlet")

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

# ======================
elif selected == "Bar Chart":
    bar_chart.main()

# ======================
elif selected == "Peta GIS":
    st.subheader("🗺️ Peta Outlet dengan Rating Tinggi")

    st.info(
        "ℹ️ Peta menampilkan outlet Sociolla & Sephora berdasarkan rating.\n"
        "Marker biru = lokasi Anda, pink/black = outlet."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        user_lat = st.number_input("📍 Latitude", value=-6.9175, format="%.6f")
    with col2:
        user_lon = st.number_input("📍 Longitude", value=107.6191, format="%.6f")
    with col3:
        min_rating = st.slider("⭐ Minimal Rating Outlet", 3.0, 5.0, 4.3)

    if st.button("🗺️ Tampilkan / Perbarui Peta"):
        with st.spinner("⏳ Membuat peta GIS..."):
            try:
                map_path = gis.generate_map(user_lat, user_lon, min_rating)
                st.success("✅ Peta berhasil diperbarui!")
            except Exception as e:
                st.error(str(e))

    if os.path.exists("Data/Visualisasi/peta_outlet.html"):
        with open("Data/Visualisasi/peta_outlet.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600)
