from youtube_search import cari_youtube_video
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import semua playlist
from data_lagu.lagu_indonesia import lagu_indonesia
from data_lagu.lagu_barat import lagu_barat
from data_lagu.lagu_kpop import lagu_kpop
from data_lagu.lagu_jpop import lagu_jpop
from data_lagu.lagu_jpop import lagu_anime

# Gabung semua lagu
semua_lagu = []
semua_lagu.extend(lagu_indonesia)
semua_lagu.extend(lagu_barat)
semua_lagu.extend(lagu_kpop)
semua_lagu.extend(lagu_jpop)
semua_lagu.extend(lagu_anime)

# Default cover jika tidak tersedia
DEFAULT_COVER = "https://via.placeholder.com/300x300?text=No+Cover"

# Proses penambahan otomatis 
for i, lagu in enumerate(semua_lagu):
    title = lagu.get("title")
    artist = lagu.get("artist")

    print(f"[{i+1}/{len(semua_lagu)}] Memproses: {title} - {artist}")

    # Tambahkan cover default jika kosong
    if not lagu.get("cover"):
        lagu["cover"] = DEFAULT_COVER

    # Ambil youtube_id jika belum ada
    if not lagu.get("youtube_id") and title and artist:
        query = f"{title} {artist}"
        yt_id = cari_youtube_video(query)
        lagu["youtube_id"] = yt_id

# Simpan ke file JSON
with open("playlist_enhanced.json", "w", encoding="utf-8") as f:
    json.dump(semua_lagu, f, indent=4, ensure_ascii=False)

print("\n✅ Playlist selesai diproses!")
print("📄 Simpan sebagai 'playlist_enhanced.json'")