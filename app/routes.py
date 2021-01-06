from app import app
from app.controller import DosenController
from flask import request

@app.route('/')
def index():
    return 'Hello Flask App'

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()


@app.route('/dosen/<id>', methods=['GET', 'PUT'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    else:
        return DosenController.ubah(id)

