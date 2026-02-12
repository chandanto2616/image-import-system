import requests
from config import Config


def extract_folder_id(folder_url):
    if "folders/" in folder_url:
        return folder_url.split("folders/")[1].split("?")[0]
    return None


def list_images_in_folder(folder_id):
    url = "https://www.googleapis.com/drive/v3/files"

    params = {
        "q": f"'{folder_id}' in parents",
        "key": Config.GOOGLE_API_KEY,
        "fields": "files(id,name,mimeType,size)",
    }

    response = requests.get(url, params=params)

    print("Drive API response:", response.text)  # debug

    data = response.json()

    images = []
    for file in data.get("files", []):
        if file["mimeType"].startswith("image/"):
            images.append(file)

    return images


def download_image(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"
