import requests
import pandas as pd
import time
import os

# ======================================================
# FUNGSI UTAMA SCRAPING
# ======================================================
def main():
    """
    Fungsi utama untuk menjalankan proses scraping review
    dari beberapa e-commerce (Sociolla & Sephora)
    berdasarkan data statis.
    """

    # ======================================================
    # KONFIGURASI PATH ROOT PROJECT
    # ======================================================
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    FILE_STATIC = os.path.join(BASE_DIR, "Data", "Raw", "data_website_baru.csv")     
    FILE_OUTPUT = os.path.join(BASE_DIR, "Data", "Raw", "data_scrapping.csv")  

    REVIEW_LIMIT = 30  

    # ======================================================
    # BACA DATA STATIS
    # ======================================================
    df_static = pd.read_csv(FILE_STATIC)            
    df_static.columns = df_static.columns.str.strip()

    all_reviews = []  # Penampung seluruh review

    # ======================================================
    # LOOP DATA STATIS
    # ======================================================
    for idx, row in df_static.iterrows():

        # Lewati jika produk_id kosong
        if pd.isna(row["produk_id"]):
            continue
        
        Outlet = row["Outlet"]     
        outlet_id = row["outlet_id"]            
        product_id = str(row["produk_id"])           
        ecommerce = row["e-commere"].lower()          
        sampling_index = int(row["sampling_index"]) if not pd.isna(row["sampling_index"]) else 0

        offset = sampling_index * REVIEW_LIMIT        # Offset review

        # Data tambahan dari tabel statis
        Produk_BestSeller = row.get("Produk_BestSeller")
        lat = row.get("lat")
        lon = row.get("lon") if "lon" in row else row.get("long")
        rating_global = row.get("Rating_global_produk")
        jumlah_ulasan = row.get("Jumlah_ulasan")

        print(f"Scraping | {ecommerce.upper()} | Outlet {Outlet} | Product {product_id}")

        # ==================================================
        # SCRAPING SOCIOLLA
        # ==================================================
        if ecommerce == "sociolla":

            url = "https://soco-api.sociolla.com/reviews"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            # Parameter request API Sociolla
            params = {
                "skip": offset,
                "limit": REVIEW_LIMIT,
                "sort": "-created_at",
                "filter": f'{{"is_published":true,"elastic_search":true,"product_id":"{product_id}"}}'
            }

            res = requests.get(url, params=params, headers=headers)
            if res.status_code != 200:
                continue

            # Ambil data review Sociolla
            for r in res.json().get("data", []):
                all_reviews.append({
                    "Outlet": Outlet,
                    "outlet_id" : outlet_id,
                    "e-commere" : ecommerce,
                    "Produk_BestSeller" : Produk_BestSeller,
                    "produk_id": product_id,
                    "sampling_index": sampling_index,
                    "lat": lat,
                    "lon": lon,
                    "Rating_global_produk": rating_global,
                    "Jumlah_ulasan": jumlah_ulasan,
                    "review_id": r.get("_id"),
                    "nama_reviewer": r.get("name"),
                    "rating": r.get("average_rating"),
                    "review": r.get("detail"),
                    "tanggal": r.get("created_at"),
                })

        # ==================================================
        # SCRAPING SEPHORA
        # ==================================================
        elif ecommerce == "sephora":

            BASE_URL = "https://apps.bazaarvoice.com/bfd/v1/clients/sephora-au/api-products/cv2/resources/data/reviews.json"
            HEADERS = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
                "Origin": "https://www.sephora.co.id",
                "Referer": "https://www.sephora.co.id/",
                "bv-bfd-token": "19416,main_site,id_ID",
            }

            # Parameter request API Sephora
            params = [
                ("resource", "reviews"),
                ("action", "REVIEWS_N_STATS"),
                ("filter", f"productid:eq:{product_id}"),
                ("filter", "isratingsonly:eq:false"),
                ("include", "authors"),
                ("limit", REVIEW_LIMIT),
                ("offset", offset),
                ("sort", "submissiontime:desc"),
                ("apiversion", "5.5"),
                ("displaycode", "19416-id_id"),
            ]

            res = requests.get(BASE_URL, headers=HEADERS, params=params)
            if res.status_code != 200:
                continue

            response = res.json().get("response", {})
            total = response.get("TotalResults", 0)

            # Cegah offset melebihi total review
            if offset >= total:
                continue

            # Ambil data review Sephora
            for r in response.get("Results", []):
                all_reviews.append({
                    "Outlet": Outlet,
                    "outlet_id" : outlet_id,
                    "e-commere" : ecommerce,
                    "Produk_BestSeller" : Produk_BestSeller,
                    "produk_id": product_id,
                    "sampling_index": sampling_index,
                    "lat": lat,
                    "lon": lon,
                    "Rating_global_produk": rating_global,
                    "Jumlah_ulasan": jumlah_ulasan,
                    "review_id": r.get("Id"),
                    "nama_reviewer": r.get("UserNickname") or r.get("AuthorId"),
                    "rating": r.get("Rating"),
                    "review": r.get("ReviewText"),
                    "tanggal": r.get("SubmissionTime"),
                })

            time.sleep(0.5)  

    # ======================================================
    # SIMPAN KE FILE BARU
    # ======================================================
    df_output = pd.DataFrame(all_reviews)
    df_output.to_csv(FILE_OUTPUT, index=False)

    print("SELESAI | Total review:", len(df_output))


# ======================================================
# JIKA FILE DIJALANKAN LANGSUNG
# ======================================================
if __name__ == "__main__":
    main()
