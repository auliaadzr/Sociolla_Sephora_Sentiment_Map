import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ======================================================
# FUNGSI UTAMA VISUALISASI BAR CHART
# ======================================================
def main():
    # 1. KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Mengambil data dari hasil perhitungan rating outlet
    importPath = os.path.join(BASE_DIR, "Data", "Raw", "data_rating_outlet.csv")
    exportVisualPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "bar_chart_rating.png")

    try:
        # 2. BACA DATA
        df = pd.read_csv(importPath)
        
        # Urutkan berdasarkan rating tertinggi untuk estetika grafik
        df = df.sort_values(by='rating_outlet', ascending=False)

        # 3. SETTING KANVAS GRAFIK
        plt.figure(figsize=(12, 7))
        sns.set_style("whitegrid") # Memberi background garis halus

        # Penentuan Warna: Pink (Sociolla), Hitam (Sephora)
        colors = ['#FF69B4' if brand.lower() == 'sociolla' else '#000000' for brand in df['Outlet']]

        # Membuat Bar Plot
        plot = sns.barplot(
            x='Outlet', 
            y='rating_outlet', 
            data=df, 
            palette=colors
        )

        # 4. KUSTOMISASI JUDUL & LABEL
        plt.title('Peringkat Kepuasan Pelanggan: Sociolla vs Sephora (Bandung)', fontsize=15, fontweight='bold', pad=20)
        plt.xlabel('Outlet', fontsize=12)
        plt.ylabel('Skor Rating (Bayesian Average)', fontsize=12)
        plt.ylim(0, 5.5) # Skala bintang 1-5

        # Menambahkan Label Angka di Atas Setiap Batang
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.2f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points',
                   fontweight='bold',
                   fontsize=10)

        # 5. SIMPAN KE FOLDER VISUALISASI
        plt.tight_layout()
        plt.savefig(exportVisualPath, dpi=300)
        
        print("-" * 30)
        print(f"Visualisasi Berhasil!")
        print(f"Grafik disimpan di: {exportVisualPath}")
        plt.show()

    except Exception as e:
        print(f"Gagal membuat visualisasi: {e}")

# ======================================================
# JIKA FILE DIJALANKAN LANGSUNG
# ======================================================
if __name__ == "__main__":
    main()