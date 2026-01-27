💄Analisis Sentimen & Sebaran Retail Kecantikan: Sociolla vs Sephora
=======================================================================
Aplikasi Live Web GIS yang dirancang untuk menganalisis tingkat kepuasan pelanggan terhadap outlet retail kecantikan (Sociolla & Sephora) di wilayah Bandung. Proyek ini menggunakan metode Bayesian Average untuk memberikan rating outlet yang akurat sebagai dasar pengambilan keputusan strategi pemasaran.

Tujuan
-------
Analisis Kompetitif: Membandingkan tingkat kepuasan pelanggan antara Sociolla dan Sephora berdasarkan ulasan nyata.

Visualisasi Komparatif (Bar & Pie Chart): 
- Pie Chart: Mengukur Dominasi Kepuasan untuk melihat proporsi sentimen positif antara kedua brand dalam satu pasar.
- Bar Chart: Melakukan ranking outlet dari yang terbaik hingga terendah berdasarkan skor Bayesian untuk memudahkan perbandingan antar cabang.
  
Visualisasi Spasial (GIS): Memetakan lokasi presisi setiap outlet pada peta interaktif dengan fitur tambahan yang tidak dimiliki platform asli:
- Informasi Rating Outlet : Menampilkan skor rating hasil perhitungan Bayesian yang memberikan gambaran kualitas layanan sebenarnya di titik tersebut.
- Rekomendasi Produk: Menyajikan 7 Produk Best Seller di setiap outlet dalam jendela popup, memudahkan pengambil keputusan atau pelanggan melihat keunggulan produk di lokasi tertentu.

Alur Pengolahan Data 
---------------------------
Scraping (Data Acquisition): Proses pengambilan data mentah secara otomatis dari API Sociolla dan Sephora. Data yang dikumpulkan meliputi:
- Informasi Produk: Nama produk dan rating global.
- Ulasan Pelanggan: Teks ulasan lengkap untuk analisis sentimen dan rating ulasan.
- Identitas Pengulas: Nama pengulas untuk memastikan keaslian data.
  
Cleaning : Tahap penyiapan data agar hasil analisis menjadi akurat melalui beberapa langkah:
- Deduplikasi: Menghapus data ulasan yang ganda/duplikat.
- Handling Missing Values: Membersihkan baris data yang kosong atau tidak lengkap.
- Case Folding: Mengubah seluruh teks ulasan menjadi huruf kecil (lowercase) untuk menyeragamkan format data sebelum proses pencarian kata kunci (keyword matching).

Analisis Bayesian: Menghitung Skor Rating Outlet yang telah divalidasi dengan menggabungkan rata-rata ulasan pelanggan dan rating produk global menggunakan konstanta kepercayaan k=5.

Visualisasi (Pie & Bar Chart): Menyajikan proporsi kepuasan pelanggan secara keseluruhan (Pie Chart) dan peringkat performa antar outlet (Bar Chart) untuk memudahkan perbandingan cepat.

GIS (Geographical Information System): Memetakan hasil analisis ke dalam peta interaktif Bandung. Peta ini menampilkan Rating Outlet (Hasil Bayesian) yang tidak tersedia di website asli, serta daftar 7 Produk Best Seller pada setiap koordinat outlet
