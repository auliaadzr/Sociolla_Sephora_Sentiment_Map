import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # 1. KONFIGURASI PATH
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Ambil data dari hasil cleaning (data_cleaned.csv)
    importPath = os.path.join(BASE_DIR, "Data", "Clean", "data_cleaning.csv")
    exportVisualPath = os.path.join(BASE_DIR, "Data", "Visualisasi", "pie_chart_total_kepuasan.png")

    try:
        # 2. BACA DATA
        df = pd.read_csv(importPath)
        
        # 3. KATA KUNCI KEPUASAN (Keyword Matching)
        # Menentukan ulasan positif berdasarkan teks
        kata_positif = ['bagus', 'puas', 'enak', 'suka', 'mantap', 'recomended', 'cocok', 'love', 'best', 'original', 'keren', 'ramah']
        
        def cek_sentimen(teks):
            teks = str(teks).lower()
            if any(kata in teks for kata in kata_positif):
                return 'Puas (Review Positif)'
            else:
                return 'Netral / Tidak Puas'

        # Terapkan analisis pada kolom review
        df['Sentimen_Teks'] = df['review'].apply(cek_sentimen)

        # 4. HITUNG TOTAL GABUNGAN
        total_counts = df['Sentimen_Teks'].value_counts()

        # 5. BUAT PIE CHART
        plt.figure(figsize=(10, 8))
        colors = ['#FF69B4', '#D3D3D3'] # Pink untuk Puas, Abu-abu untuk Netral

        plt.pie(
            total_counts, 
            labels=total_counts.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            explode=(0.05, 0), # Menonjolkan bagian 'Puas'
            shadow=True
        )

        # 6. KUSTOMISASI
        plt.title('Ringkasan Kepuasan Konsumen Retail Kecantikan di Bandung\n(Berdasarkan Analisis Teks 1.666 Ulasan)', 
                  fontsize=14, fontweight='bold')

        # 7. SIMPAN HASIL
        plt.tight_layout()
        plt.savefig(exportVisualPath, dpi=300)
        
        print("-" * 30)
        print(f"Berhasil! Pie Chart total kepuasan disimpan di: {exportVisualPath}")
        print(f"Statistik: {total_counts.to_dict()}")
        plt.show()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()