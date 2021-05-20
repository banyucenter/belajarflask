from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa

from app import response, app, db
from flask import request, jsonify,abort

import math

def index():
    try:
        dosen = Dosen.query.all()
        data = formatarray(dosen)
        return response.success(data, "success")
    except Exception as e:
        print(e)



def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    
    return array

def singleObject(data):
    data = {
        'id' : data.id,
        'nidn' : data.nidn,
        'nama' : data.nama,
        'phone' : data.phone,
        'alamat' : data.alamat
    }

    return data

def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu == id) | (Mahasiswa.dosen_dua == id))

        if not dosen:
            return response.badRequest([], 'Tidak ada data dosen')

        datamahasiswa = formatMahasiswa(mahasiswa)

        data = singleDetailMahasiswa(dosen, datamahasiswa)

        return response.success(data, "success")

    except Exception as e:
        print(e)

def singleDetailMahasiswa(dosen, mahasiswa):
    data = {
        'id': dosen.id,
        'nidn': dosen.nidn,
        'nama': dosen.nama,
        'phone': dosen.phone,
        'mahasiswa' : mahasiswa
    }

    return data

def singleMahasiswa(mahasiswa):
    data = {
        'id': mahasiswa.id,
        'nim': mahasiswa.nim,
        'nama': mahasiswa.nama,
        'phone': mahasiswa.phone
    }

    return data

def formatMahasiswa(data):
    array = []
    for i in data:
        array.append(singleMahasiswa(i))
    return array

def save():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        input = [{
            'nidn': nidn,
            'nama': nama,
            'phone': phone,
            'alamat': alamat
        }]

        dosens = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(dosens)
        db.session.commit()

        return response.success(input, 'Sukses Menambahkan Data Dosen')
    except Exception as e:
        print(e)

#update data
def ubah(id):
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        input = [
            {
                'nidn': nidn,
                'nama': nama,
                'phone': phone,
                'alamat': alamat
            }
        ]

        dosen = Dosen.query.filter_by(id=id).first()

        dosen.nidn = nidn
        dosen.nama = nama
        dosen.phone = phone
        dosen.alamat = alamat

        db.session.commit()

        return response.success(input, 'Sukses update data!')
    except Exception as e:
        print(e)

#hapus
def hapus(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], 'Data Dosen Kosong...')
        
        db.session.delete(dosen)
        db.session.commit()

        return response.success('', 'Berhasil menghapus data!')
    except Exception as e:
        print(e)

def get_paginated_list(clss, url, start, limit):
    # ambil query dari tabel dosen => class yang akan dibuat paginasi
    results = clss.query.all()
    #ubah format agar serialized 
    data = formatarray(results)
    #hitung semua isi value array
    count = len(data)

    obj = {}

    if (count < start):
        obj['success'] = False
        obj['message'] = "Page yang dipilih (start) melewati batas total data!"
        return obj
    else:
        # make response
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        #ceil agar bilangan menjadi bulat ke atas
        obj['total_page'] = math.ceil(count / limit)
        # make URLs
        # make previous url
        if start == 1:
            obj['previous'] = ''
        else:
            #ambil nilai start yg paling tinggi nilainya
            start_copy = max(1, start - limit)
            #ambil nilai data yg hendak ditampilkan querynya di previous page 
            #misal kiat punya 5 data, dengan limit tampil adalah 2 per page
            #saat di posisi page ke 5 maka kita bisa set previous limit yg tampil adalah 5 -1 = 4
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        # make next url
        #jika misal total data ada 5
        #kita set mulai dari page 2 dan limit 3
        #jumlah melebihi count maka nex = kosong
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # finally extract result hasil sesuai batasnya
        #slicing array dimana dimulai dari start - 1 + limit
        obj['results'] = data[(start - 1):(start - 1 + limit)]
        return obj

#buat fungsi paginate
def paginate():
    #ambil parameter get 
    #sample http://127.0.0.1:5000/api/dosen/page?start=3&limit=4
    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        #default display first page
        if start == None or limit == None:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/api/dosen/page', 
            start=request.args.get('start',1), 
            limit=request.args.get('limit',5)
            ))
            #custom parameters
        else:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/api/dosen/page', 
            start=int(start), 
            limit=int(limit)
            ))

    except Exception as e:
        print(e)