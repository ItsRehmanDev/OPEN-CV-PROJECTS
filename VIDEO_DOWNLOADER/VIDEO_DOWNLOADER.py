import os

# user se video link lo
video_url = input("Paste video link here: ")

# download folder
download_folder = "downloads"

# agar folder nahi hai to bana do
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# yt-dlp command
command = f'yt-dlp -o "{download_folder}/%(title)s.%(ext)s" {video_url}'

# command run karo
os.system(command)

print("Download completed!")
