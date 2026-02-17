from flask import Blueprint, request, jsonify
from services.drive_service import download_image, extract_folder_id, list_images_in_folder
from models import db, Image
import requests
import tempfile
from services.cloudinary_service import upload_image

image_bp = Blueprint("image_bp", __name__)
import threading

cancel_flag = {"stop": False}

@image_bp.route("/import/google-drive", methods=["POST"])
def import_images():
    cancel_flag["stop"] = False

    data = request.json
    folder_url = data.get("folder_url")

    folder_id = extract_folder_id(folder_url)

    if not folder_id:
        return jsonify({"error": "Invalid folder URL"}), 400

    files = list_images_in_folder(folder_id)
    print("Total files in folder:", len(files))

    imported_count = 0
    skipped_count = 0

    for file in files:
        if cancel_flag["stop"]:
            print("Import cancelled by user")
            break

        try:
            # Check if this file already exists
            existing = Image.query.filter_by(
                google_drive_id=file["id"]
            ).first()

            if existing:
                skipped_count += 1
                print("Skipping existing file:", file["name"])
                continue

            print("Processing:", file["name"])

            download_url = download_image(file["id"])
            response = requests.get(download_url, stream=True)

            if response.status_code != 200:
                continue

            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(response.content)
                temp_path = temp.name

            cloud_url = upload_image(temp_path)

            image = Image(
                name=file["name"],
                google_drive_id=file["id"],
                folder_id=folder_id,
                size=int(file.get("size", 0)),
                mime_type=file["mimeType"],
                storage_path=cloud_url,
            )
            

            db.session.add(image)
            db.session.commit()

            imported_count += 1
            print("Saved:", file["name"])

        except Exception as e:
            print("Error:", str(e))
            db.session.rollback()
            

    return jsonify({
        "imported": imported_count,
        "skipped": skipped_count
    })



@image_bp.route("/import/cancel", methods=["POST"])
def cancel_import():
    cancel_flag["stop"] = True
    return jsonify({"status": "cancelled"})

