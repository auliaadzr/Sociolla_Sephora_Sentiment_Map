import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # KONFIGURASI PATH 
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    importPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")
    exportPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "perbandingan_kepuasan_outlet.png")

    try:
        # BACA DATA
        df = pd.read_csv(importPath)

        # ULASAN POSITIF 
        kata_positif = ['bagus', 'puas', 'enak', 'suka', 'mantap', 'recomended', 'cocok', 'love', 'best', 
                        'original', 'keren', 'ramah', 'good', 'nice', 'recommended', 'terbaik']

        def is_positif(teks):
            teks = str(teks).lower()
            return any(kata in teks for kata in kata_positif)

        df_positif = df[df['review'].apply(is_positif)].copy()

        # Menghapus spasi dan memastikan format 'Sociolla' / 'Sephora'
        df_positif['e-commere'] = df_positif['e-commere'].str.strip().str.capitalize()
        counts = df_positif['e-commere'].value_counts()

        # VISUALISASI PIE CHART 
        plt.figure(figsize=(10, 8))

        # Mapping warna 
        color_map = {
            'Sociolla': '#FF69B4', # Pink
            'Sephora': '#4F4F4F'   # Abu-abu Tua/Hitam
        }

        # Mengambil warna 
        current_colors = [color_map.get(brand, '#D3D3D3') for brand in counts.index]

        plt.pie(
            counts, 
            labels=counts.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=current_colors,
            explode=[0.05 if i == 0 else 0 for i in range(len(counts))], 
            shadow=True
        )

        plt.title('Dominasi Kepuasan Pelanggan: Sociolla vs Sephora\n(Berdasarkan Proporsi Ulasan Positif)', 
                  fontsize=14, fontweight='bold')

        # SIMPAN HASIL
        plt.tight_layout()
        if not os.path.exists(os.path.dirname(exportPath)):
            os.makedirs(os.path.dirname(exportPath))
        plt.savefig(exportPath, dpi=300)

        print(f"Visualisasi Berhasil!")
        print(f"Detail Statistik: {counts.to_dict()}")
        plt.show()

    except Exception as e:
        print(f"Terjadi kesalahan visualisasi: {e}")

# JIKA FILE DIJALANKAN LANGSUNG
if __name__ == "__main__":
    main()