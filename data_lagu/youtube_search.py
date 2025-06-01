from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Inisialisasi YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def cari_youtube_video(query):
    """
    Fungsi mencari video di YouTube berdasarkan query
    Mengembalikan ID video pertama yang ditemukan
    """
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()

        if response["items"]:
            return response["items"][0]["id"]["videoId"]
        else:
            print(f"❌ Tidak ditemukan: {query}")
            return None
    except Exception as e:
        print(f"⚠️ Error saat mencari '{query}': {e}")
        return None