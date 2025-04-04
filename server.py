from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

# Creează directorul pentru stocarea imaginilor dacă nu există
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    print("Headers:", dict(request.headers))
    print("Form data:", request.form.to_dict())
    print("Files:", request.files)
    
    if 'image' not in request.files:
        return jsonify({
            'error': 'Nu a fost trimisă nicio imagine',
            'received_files': list(request.files.keys()),
            'content_type': request.content_type
        }), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Niciun fișier selectat'}), 400
    
    # Creează un nume unic pentru imagine folosind timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Salvează imaginea
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'message': 'Imaginea a fost încărcată cu succes',
        'filename': filename
    }), 200

@app.route('/images', methods=['GET'])
def list_images():
    images = os.listdir(UPLOAD_FOLDER)
    return jsonify({
        'images': images,
        'count': len(images)
    })

if __name__ == '__main__':
    # Pentru deplasare reală, ar trebui să utilizezi un server WSGI precum Gunicorn
    # și să configurezi corect 'host' pentru a permite conexiuni din exterior
    app.run(host='0.0.0.0', port=5000, debug=True)