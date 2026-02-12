from flask import Flask
from config import Config
from models import db
from routes.image_routes import image_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(image_bp)

@app.route("/images", methods=["GET"])
def list_images():
    from models import Image
    images = Image.query.all()

    result = []
    for img in images:
        result.append({
            "id": img.id,
            "name": img.name,
            "storage_path": img.storage_path,
            "size": img.size,
            "mime_type": img.mime_type
        })

    return {"images": result}

@app.route("/images/<folder_id>", methods=["GET"])
def list_images_by_folder(folder_id):
    from models import Image
    images = Image.query.filter_by(folder_id=folder_id).all()

    result = []
    for img in images:
        result.append({
            "id": img.id,
            "name": img.name,
            "storage_path": img.storage_path,
            "size": img.size,
            "mime_type": img.mime_type
        })

    return {"images": result}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

