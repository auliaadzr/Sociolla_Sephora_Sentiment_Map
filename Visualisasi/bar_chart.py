import pandas as pd
import plotly.express as px
import os
import streamlit as st

def main():
    # KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Mengambil data 
    importPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")

    # BACA DATA
    df = pd.read_csv(importPath)

    # URUTKAN BESAR KE KECIL 
    df = df.sort_values(by='rating_outlet', ascending=False)

    # Penentuan Warna
    color_map = {'sociolla': '#FF69B4', 'sephora': '#000000'}

    # Membuat Bar Plot Interaktif
    fig = px.bar(
        df,
        x='outlet_id', 
        y='rating_outlet',
        text='rating_outlet',
        color='e-commere',
        color_discrete_map=color_map,
        hover_name='Outlet', 
        labels={
            'outlet_id': 'Outlet ID',
            'rating_outlet': 'Skor Rating',
            'e-commere': 'Brand'
        },
    )

    # 2. KUSTOMISASI TEKS DI ATAS BATANG
    fig.update_traces(
        texttemplate='%{text:.2f}', 
        textposition='outside',
        textfont=dict(color='black', size=12),
        hovertemplate="<b>%{hovertext}</b><extra></extra>"
    )

    fig.update_layout(
    title_text="📊 Perbandingan Rating Oulet Sociolla vs Sephora",
    plot_bgcolor='white',
    xaxis={
        'categoryorder':'total descending',
        'tickangle': 0,
        'tickfont': dict(size=9)
    },
    yaxis=dict(range=[0, 5.5], gridcolor='lightgrey'),
    font=dict(family="Arial", size=12),
    title_font=dict(size=30, family="Arial", color="black"),
    margin=dict(t=60, b=80)
    )

    # TAMPILKAN DI STREAMLIT
    st.plotly_chart(fig, use_container_width=True)

# MAIN
if __name__ == "__main__":
    main()
