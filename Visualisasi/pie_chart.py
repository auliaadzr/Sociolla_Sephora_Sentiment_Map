import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Konfigurasi Streamlit
st.set_page_config(page_title="Analisis Kepuasan Brand", layout="wide")

def main():
    # 1. PENGATURAN PATH
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    importPath = os.path.join(project_root, "Data", "Clean", "data_cleaning.csv")

    try:
        if not os.path.exists(importPath):
            st.error(f"File tidak ditemukan di: {importPath}")
            return

        # 2. LOAD & PREPARASI DATA
        df = pd.read_csv(importPath)

        # Definisi Sentimen Positif
        kata_positif = [
            'bagus', 'puas', 'enak', 'suka', 'mantap', 'recommended',
            'recomended', 'cocok', 'love', 'best', 'original',
            'keren', 'ramah', 'good', 'nice', 'terbaik'
        ]

        def is_positif(teks):
            teks = str(teks).lower()
            return any(kata in teks for kata in kata_positif)

        df['positif'] = df['review'].apply(is_positif)
        df['e-commere'] = df['e-commere'].str.strip().str.capitalize()
        
        # Nama Mall dari kolom Outlet
        df['Nama_Mall'] = df['Outlet'].str.replace('_', ' ').str.title()

        # 3. AGREGASI DATA
        # Mengumpulkan daftar mall unik untuk ditampilkan di pop-up
        brand_stats = df.groupby('e-commere').agg(
            Rata_Kepuasan=('positif', 'mean'),
            Daftar_Mall=('Nama_Mall', lambda x: "<br>• ".join(x.unique()[:5])) 
        ).reset_index()

        st.title('📊 Perbandingan Kepuasan Rata-rata Brand')

        # 4. WARNA (Pink untuk Sociolla, Hitam untuk Sephora)
        color_map = {
            'Sociolla': '#FF69B4',
            'Sephora': '#000000'
        }

        # 5. VISUALISASI PIE CHART (PLOTLY)
        fig = px.pie(
            brand_stats,
            values='Rata_Kepuasan',
            names='e-commere',
            color='e-commere',
            color_discrete_map=color_map,
            hole=0.3, 
        )

        # 6. KUSTOMISASI POP-UP (HOVER) - MENGHAPUS KATA "CONTOH"
        fig.update_traces(
            hovertemplate="<b>Brand: %{label}</b><br>Kepuasan: %{percent}<br><br><b>Mall:</b><br>• %{customdata[0]}<extra></extra>",
            customdata=brand_stats[['Daftar_Mall']]
        )

        fig.update_layout(
            legend_title="Brand",
            margin=dict(t=50, b=50, l=0, r=0)
        )

        # 7. TAMPILKAN KE STREAMLIT
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()