import streamlit as st
from data_lagu.lagu_indonesia import lagu_indonesia
from data_lagu.lagu_barat import lagu_barat
from data_lagu.lagu_kpop import lagu_kpop
from data_lagu.lagu_jpop import lagu_jpop
import json
import time

# Inisialisasi playlist
if "playlist" not in st.session_state:
    st.session_state.playlist = []
    st.session_state.playlist.extend(lagu_indonesia)
    st.session_state.playlist.extend(lagu_barat)
    st.session_state.playlist.extend(lagu_kpop)
    st.session_state.playlist.extend(lagu_jpop)

# Set page config
st.set_page_config(page_title="🎵 Playlist Musik Digital", page_icon="assets/icon.png", layout="wide")

# Sidebar Menu
with st.sidebar:
    st.image("assets/logo.png", width=70)
    st.title("🎵 Zalvoria")
    menu = st.selectbox("Navigasi", ["Beranda", "Tambah Lagu", "Cari Lagu", "Urutkan", "Simpan/Muat", "Filter", "Statistik"])
    tema = st.radio("🎨 Warna Tema", ["Gelap", "Cerah"])

# Theme switch
if tema == "Gelap":
    st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d44;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: black;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f5;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# Efek loading saat halaman pertama kali dibuka
def show_loading():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <style>
        .loader {
            border: 16px solid #f3f3f3;
            border-top: 16px solid #3498db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 2s linear infinite;
            margin: auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        <center><div class="loader"></div><h4>Memuat playlist...</h4></center>
        """, unsafe_allow_html=True)
    time.sleep(1.5)  # Simulasi waktu loading
    placeholder.empty()

# Fungsi untuk menampilkan playlist dengan tombol hapus & edit
def display_playlist(filtered=None):
    lagu_list = filtered if filtered else st.session_state.playlist
    if not lagu_list:
        st.warning("Playlist kosong.")
        return

    cols = st.columns(3)
    for idx, song in enumerate(lagu_list):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background:#2d2f4a; border-radius:15px; padding:20px; text-align:center; color:white;">
                <img src="{song.get('cover', 'https://via.placeholder.com/300x300?text=No+Cover')}" width="100%" />
                <h4>{song['title']}</h4>
                <p>🎤 {song['artist']}</p>
                <p>🎵 Genre: {song.get('genre', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if song.get("audio_url"):
                try:
                    st.audio(song["audio_url"], format="audio/mp3")
                except Exception:
                    st.caption("🎵 Gagal memuat audio")
            else:
                st.caption("🎵 Preview tidak tersedia")


            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Hapus", key=f"hapus_{idx}_{song['title']}"):
                    st.session_state.playlist.remove(song)
                    st.success(f"Lagu '{song['title']}' dihapus.")
                    st.rerun()
            with col2:
                if st.button("✏️ Edit", key=f"edit_{idx}_{song['title']}"):
                    try:
                        idx_global = st.session_state.playlist.index(song)
                        st.session_state.edit_idx = idx_global
                        st.session_state.edit_mode = True
                        st.rerun()
                    except ValueError:
                        st.error("❌ Lagu tidak ditemukan di playlist.")
    lagu_list = filtered if filtered else st.session_state.playlist
    if not lagu_list:
        st.warning("Playlist kosong.")
        return

   
# Fungsi pencarian   
def cari_lagu(judul):
    return next((lagu for lagu in st.session_state.playlist if lagu["title"].lower() == judul.lower()), None)

# Merge Sort
def merge_sort(arr, key="title"):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] < right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Header Aplikasi
st.markdown("<h1 style='text-align:center;'>🎵 Zalvoria</h1>", unsafe_allow_html=True)

# Efek loading
show_loading()

# Menu Utama
if menu == "Beranda":
    st.subheader("🏠 Beranda - Semua Lagu")
    display_playlist()

elif menu == "Tambah Lagu":
    st.subheader("➕ Tambah Lagu ke Playlist")

    if "edit_mode" in st.session_state and st.session_state.edit_mode:
        try:
            idx_edit = st.session_state.edit_idx
            lagu_edit = st.session_state.playlist[idx_edit]

            title = st.text_input("Judul Lagu", value=lagu_edit["title"])
            artist = st.text_input("Penyanyi", value=lagu_edit["artist"])
            genre = st.text_input("Genre", value=lagu_edit.get("genre", ""))
            cover = st.text_input("URL Cover (opsional)", value=lagu_edit.get("cover", ""))
            audio_url = st.text_input("URL Audio (.mp3)", value=lagu_edit.get("audio_url", ""))

            if st.button("✅ Simpan Perubahan"):
                st.session_state.playlist[idx_edit] = {
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "cover": cover or "https://via.placeholder.com/300x300?text=No+Cover",
                    "audio_url": audio_url
                }
                del st.session_state.edit_mode
                del st.session_state.edit_idx
                st.success("Lagu berhasil diedit.")
                st.rerun()

            if st.button("❌ Batal"):
                del st.session_state.edit_mode
                del st.session_state.edit_idx
                st.rerun()

        except IndexError:
            st.error("❌ Indeks lagu tidak valid.")
            del st.session_state.edit_mode
            st.rerun()
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
            del st.session_state.edit_mode
            st.rerun()

    else:
        # Form tambah lagu 
        title = st.text_input("Judul Lagu")
        artist = st.text_input("Penyanyi")
        genre = st.text_input("Genre")
        cover = st.text_input("URL Cover (opsional)")
        audio_url = st.text_input("URL Audio (.mp3)")

        if st.button("➕ Tambahkan Lagu"):
            if title and artist and genre:
                st.session_state.playlist.append({
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "cover": cover or "https://via.placeholder.com/300x300?text=No+Cover",
                    "audio_url": audio_url
                })
                st.success(f"✅ '{title}' berhasil ditambahkan.")
                st.rerun()

elif menu == "Cari Lagu":
    st.subheader("🔍 Cari Lagu")
    judul = st.text_input("Masukkan judul:")
    if st.button("Cari"):
        hasil = cari_lagu(judul)
        if hasil:
            st.info(f"Lagu ditemukan: {hasil}")
            display_playlist([hasil])
        else:
            st.error("❌ Lagu tidak ditemukan.")

elif menu == "Urutkan":
    st.subheader("🔁 Urutkan Playlist")
    urutkan_berdasarkan = st.radio("Pilih metode pengurutan", ["Judul", "Genre"])
    key_map = {"Judul": "title", "Genre": "genre"}
    if st.button("Urutkan"):
        sorted_playlist = merge_sort(st.session_state.playlist, key=key_map[urutkan_berdasarkan])
        display_playlist(sorted_playlist)

elif menu == "Simpan/Muat":
    st.subheader("💾 Simpan & Muat Playlist")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Simpan ke JSON"):
            with open("playlist_simpan.json", "w") as f:
                json.dump(st.session_state.playlist, f, indent=4)
            st.success("✅ Playlist disimpan sebagai JSON")
        with open("playlist_simpan.json", "r") as f:
            st.download_button("⬇️ Unduh Playlist", f.read(), file_name="playlist_simpan.json")
    with col2:
        uploaded_file = st.file_uploader("📂 Upload playlist JSON", type=["json"])
        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                st.session_state.playlist = data
                st.success("✅ Playlist berhasil dimuat.")
            except Exception as e:
                st.error(f"❌ Gagal memuat playlist: {e}")

elif menu == "Filter":
    st.subheader("🎵 Filter Berdasarkan Genre")
    genre_list = sorted(set(lagu.get("genre", "Unknown") for lagu in st.session_state.playlist))
    genre = st.selectbox("Pilih Genre", genre_list)
    if st.button("Terapkan Filter"):
        hasil = [lagu for lagu in st.session_state.playlist if lagu.get("genre", "").lower() == genre.lower()]
        display_playlist(hasil)

elif menu == "Statistik":
    st.subheader("📊 Statistik Playlist")
    genre_durations = {}
    for lagu in st.session_state.playlist:
        genre = lagu.get("genre", "Unknown")
        genre_durations.setdefault(genre, []).append(lagu["duration"])
    avg_durations = {g: round(sum(d)/len(d)) for g, d in genre_durations.items()}
    st.bar_chart(avg_durations)

# Footer 
st.markdown("<br><hr><center>🎶 Zalvoria @2025. All right reserved</center>", unsafe_allow_html=True)