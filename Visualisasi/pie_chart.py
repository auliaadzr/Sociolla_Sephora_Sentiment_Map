import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    importPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")
    exportPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "kepuasan_rata_rata_outlet.png")

    try:
        # LOAD DATA
        df = pd.read_csv(importPath)

        # DEFINISI ULASAN POSITIF
        kata_positif = [
            'bagus', 'puas', 'enak', 'suka', 'mantap', 'recommended',
            'recomended', 'cocok', 'love', 'best', 'original',
            'keren', 'ramah', 'good', 'nice', 'terbaik'
        ]

        def is_positif(teks):
            teks = str(teks).lower()
            return any(kata in teks for kata in kata_positif)

        df['positif'] = df['review'].apply(is_positif)

        # NORMALISASI BRAND
        df['e-commere'] = df['e-commere'].str.strip().str.capitalize()

        # PROPORSI POSITIF PER OUTLET
        outlet_stats = (
            df
            .groupby(['Outlet', 'e-commere'])['positif']
            .mean()
            .reset_index()
        )

        # RATA-RATA KEPUASAN PER BRAND
        brand_avg = (
            outlet_stats
            .groupby('e-commere')['positif']
            .mean()
        )

        # VISUALISASI PIE CHART
        plt.figure(figsize=(8, 8))

        color_map = {
            'Sociolla': '#FF69B4',  # Pink
            'Sephora': '#4F4F4F'    # Abu-abu tua
        }

        colors = [color_map.get(b, '#D3D3D3') for b in brand_avg.index]

        plt.pie(
            brand_avg,
            labels=brand_avg.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            explode=[0.05] * len(brand_avg),
            shadow=True
        )

        plt.title(
            'Perbandingan Kepuasan Rata-rata Outlet\nSociolla vs Sephora',
            fontsize=14,
            fontweight='bold'
        )

        plt.tight_layout()

        # SIMPAN FILE
        os.makedirs(os.path.dirname(exportPath), exist_ok=True)
        plt.savefig(exportPath, dpi=300)
        plt.close()

        print("📊 Pie chart rata-rata kepuasan per brand:")
        print(brand_avg)

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

# MAIN
if __name__ == "__main__":
    main()
