from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from gridfs import GridFS
from datetime import datetime
from dotenv import load_dotenv
from os import environ

app = Flask(__name__)
mongo = environ.get('MONGO')
# client = MongoClient('Mongo_url')
client = MongoClient(mongo)
db = client['Cluster0']
fs = GridFS(db)

@app.route('/')
def upload_form():
    return render_template('index.html')

def check_file_exists(filename):
    file_exists = fs.exists(filename=filename)
    return file_exists

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        # Check if the file already exists
        if check_file_exists(filename):
            return jsonify({'status': 'error', 'message': 'File already exists in the database.'}), 400
        else:
            # Get current date and time
            upload_datetime = datetime.now()
            
            # Store metadata along with the file
            metadata = {
                'upload_datetime': upload_datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
                'file_size': len(file.read())  # Get file size in bytes
            }
            
            fs.put(file.stream, filename=filename, content_type=file.content_type, **metadata)
            
            # Get file format
            file_format = file.content_type
            
            # Prepare response
            response_data = {
                'status': 'success',
                'message': 'File uploaded successfully!',
                'filename': filename,
                'file_format': file_format,
                'metadata': metadata
            }
            
            return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
