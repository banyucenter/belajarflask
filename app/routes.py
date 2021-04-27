from app import app, response
from app.controller import DosenController
from app.controller import UserController
from flask import request
from flask import jsonify

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@app.route('/')
def index():
    return 'Hello Flask App'

@app.route("/protected", methods=["GET"])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses')

@app.route('/dosen', methods=['GET', 'POST'])
@jwt_required
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


