import os
import hashlib
from app import app
from flask import Flask, flash, request, redirect, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

api = Api(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


files = [

]


class upload(Resource):
    def put(self):
        if request.method == 'PUT':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('success')
                str = filename
                result = hashlib.sha256(str.encode('ASCII'))
                files.append({"name": filename, "id": result.hexdigest()})
                return (result.hexdigest()), 200

    def delete(self):

        if len(files) == 0:
            return "not present", 404
        for f in files:
            f.clear()
        return "Deleted", 200


class Download(Resource):
    def get(self, id):
        for file in files:
            if id == file["id"]:
                return (send_from_directory(directory='C:/Users/madhu/Desktop/uploads', filename=file["name"])), 200

    def delete(self, id):
        global files
        files = [file for file in files if file["id"] != id]
        if (len(files) == 0):
            return "", 404
        return "object {} deleted successfully.".format(id), 200


class List(Resource):
    def get(self):
        if (len(files) == 0):
            return "", 404

        Dict = {'list': {}}
        Dict['list'] = files
        return Dict, 200


api.add_resource(Download, "/files/<string:id>")
api.add_resource(List, "/files/list")
api.add_resource(upload, "/files")

if __name__ == "__main__":
    app.run(debug=True,port=5000)
