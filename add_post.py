import json
import re
import sys

def detect_platform(url):
    if "tiktok.com" in url:
        return "tiktok"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    elif "instagram.com" in url:
        return "instagram"
    elif "twitter.com" in url or "x.com" in url:
        return "x"
    else:
        return "unknown"

def process_url(url, posts, file_path, data):
    if not url:
        return False
        
    # Detect Platform
    platform = detect_platform(url)
    if platform == "unknown":
        print(f"⚠️  URL tidak dikenali: {url}")
        return False

    # Get Next ID
    next_id = 1
    if posts:
        next_id = max(p['id'] for p in posts) + 1

    # Create Object
    new_post = {
        "id": next_id,
        "platform": platform,
        "isEmbedded": True,
        "embedUrl": url
    }

    # Save & Append
    posts.append(new_post)
    # Important: Update the main dictionary reference if posts was re-assigned/cleared (though list is mutable, good practice)
    data['socialPosts'] = posts
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Berhasil: ID {next_id} | {platform} | {url}")
    return True

def add_post():
    file_path = 'data.json'
    
    # Load existing data
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            posts = data.get('socialPosts', [])
    except FileNotFoundError:
        data = {"socialPosts": []}
        posts = []

    # Check for Command Line Argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        process_url(url, posts, file_path, data)
        return

    # Interactive Mode
    print("\n=== Penambah Konten Otomatis ===")
    print("Paste URL sosmed (TikTok/IG/FB/X) di bawah ini.")
    print("Ketik 'exit' untuk selesai.\n")

    while True:
        try:
            url = input("Masukkan URL: ").strip()
        except KeyboardInterrupt:
            print("\nKeluar.")
            break
        
        if url.lower() == 'exit':
            break
        
        process_url(url, posts, file_path, data)
        print("------------------------------------------------")

if __name__ == "__main__":
    add_post()
