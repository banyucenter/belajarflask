from app import app
from app.controller import DosenController
from app.controller import UserController
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

# @app.route('/createadmin', methods=['POST'])
# def admins():
#     return UserController.buatAdmin()

@app.route('/dosen/<id>', methods=['GET','PUT','DELETE'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)

@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()


