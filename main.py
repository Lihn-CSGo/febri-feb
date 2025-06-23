from flask import Flask, render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app= Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    _tablename_ = 'mahasiswa'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)

class Penulis(db.Model):
    _tablename_ = 'penulis'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)

class Penerbit(db.Model):
    _tablename_ = 'penerbit'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)

class Buku(db.Model):
    _tablename_ = 'buku'
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    
    id_penulis = db.Column(db.Integer, db.ForeignKey('penulis.id'))
    id_penerbit = db.Column(db.Integer, db.ForeignKey('penerbit.id'))
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'))

    penulis = db.relationship('Penulis', backref='buku')
    penerbit = db.relationship('Penerbit', backref='buku')
    mahasiswa = db.relationship('Mahasiswa', backref='buku')


@app.route('/')
def loginpage():
     return render_template('login_page.html')

@app.route('/coba.html')
def user():
     return render_template('coba.html')

@app.route('/index.html')
def dashboard():
    return render_template('dashboard/index.html')

@app.route('/mahasiswa')
def index():
    data = Mahasiswa.query.all()
    return render_template('mahasiswa/index.html', mahasiswa=data)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        id = request.form.get('id')
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        mhs = Mahasiswa(nama=nama, id=id, jurusan=jurusan)
        db.session.add(mhs)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('mahasiswa/tambah.html')

@app.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    mhs = Mahasiswa.query.get_or_404(id)
    db.session.delete(mhs)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/buku')
def buku():
    data = Buku.query.all()
    return render_template('buku/buku.html', buku=data)

@app.route('/buku/tambah', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        judul = request.form['judul']
        id_penulis = request.form['id_penulis']
        id_penerbit = request.form['id_penerbit']
        mahasiswa_id = request.form['mahasiswa_id']

        buku = Buku(
            judul=judul,
            id_penulis=id_penulis,
            id_penerbit=id_penerbit,
            mahasiswa_id=mahasiswa_id
        )
        db.session.add(buku)
        db.session.commit()
        return redirect(url_for('buku'))

    penulis = Penulis.query.all()
    penerbit = Penerbit.query.all()
    mahasiswa = Mahasiswa.query.all()
    return render_template('buku/tambah.html', penulis=penulis, penerbit=penerbit, mahasiswa=mahasiswa)

@app.route('/buku/hapus/<int:id>', methods=['GET'])
def hapus_buku(id):
    buku = Buku.query.get_or_404(id)
    db.session.delete(buku)
    db.session.commit()
    return redirect(url_for('buku'))  # Pastikan fungsi bukunya bernama 'buku'

@app.route('/penulis')
def penulis():
    data = Penulis.query.all()
    return render_template('penulis/penulis.html', data=data)

@app.route('/penulis/tambah', methods=['GET', 'POST'])
def tambah_penulis():
    if request.method == 'POST':
        id = request.form.get('id')
        nama = request.form['nama']
        penulis_baru = Penulis(id=id, nama=nama)
        db.session.add(penulis_baru)
        db.session.commit()

        
        return redirect(url_for('penulis'))
    return render_template('penulis/tambah.html')

@app.route('/penulis/hapus/<int:id>')
def hapus_penulis(id):
    penulis = Penulis.query.get_or_404(id)
    db.session.delete(penulis)
    db.session.commit()
    return redirect(url_for('penulis'))

@app.route('/penerbit')
def penerbit():
    data = Penerbit.query.all()
    return render_template('penerbit/penerbit.html', penerbit=data)

# Tambah penerbit
@app.route('/penerbit/tambah', methods=['GET', 'POST'])
def tambah_penerbit():
    if request.method == 'POST':
        id = request.form.get('id')
        nama = request.form.get('nama')
        penerbit_baru = Penerbit(id=id, nama=nama)
        db.session.add(penerbit_baru)
        db.session.commit()
        return redirect(url_for('penerbit'))
    return render_template('penerbit/tambah.html')

# Hapus penerbit
@app.route('/penerbit/hapus/<int:id>')
def hapus_penerbit(id):
    penerbit = Penerbit.query.get_or_404(id)
    db.session.delete(penerbit)
    db.session.commit()
    return redirect(url_for('penerbit'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)