from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, DATA
from pymongo import MongoClient

app = Flask(__name__)

# Configure file uploads
app.config['UPLOADED_FILES_DEST'] = 'uploads/'  # Upload folder path
uploads = UploadSet('uploads', IMAGES + DATA)  # Allowed file types
configure_uploads(app, uploads)

# MongoDB connection (replace with your connection details)
# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb+srv://DeepCytes:DeepCytes@cluster0.xq93k2r.mongodb.net/")
db = client["Cluster0"]  # Replace with your database name
collection = db["MyCollection1"]  # Replace with your collection name

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded!'
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = uploaded_file.filename
            uploaded_file.save(app.config['UPLOADED_FILES_DEST'] + filename)
            # Save file metadata to MongoDB
            file_data = {'filename': filename, 'content_type': uploaded_file.content_type}
            collection.insert_one(file_data)
            return redirect(url_for('upload_file', message='File uploaded successfully!'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)