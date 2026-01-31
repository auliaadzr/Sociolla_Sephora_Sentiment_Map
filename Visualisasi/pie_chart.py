import pandas as pd
import streamlit as st
import plotly.express as px
import os

def main():
    # Konfigurasi Streamlit
    st.set_page_config(page_title="Analisis Kepuasan Brand", layout="wide")

    # PENGATURAN PATH
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    importPath = os.path.join(project_root, "Data", "Clean", "data_cleaning.csv")

    if not os.path.exists(importPath):
        st.error(f"File tidak ditemukan di: {importPath}")
        st.code(importPath)
        st.stop()

    # LOAD & PREPARASI DATA
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

    # AGREGASI DATA
    brand_stats = df.groupby('e-commere').agg(
        Rata_Kepuasan=('positif', 'mean'),
        Daftar_Mall=('Nama_Mall', lambda x: "<br>• ".join(x.unique())) 
    ).reset_index()
    
    # WARNA
    color_map = {
        'Sociolla': '#FF69B4',
        'Sephora': '#000000'
    }

    # VISUALISASI PIE CHART
    fig = px.pie(
        brand_stats,
        values='Rata_Kepuasan',
        names='e-commere',
        color='e-commere',
        color_discrete_map=color_map,
        hole=0.3, 
    )

    # KUSTOMISASI POP-UP
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

# MAIN
if __name__ == "__main__":
    main()
