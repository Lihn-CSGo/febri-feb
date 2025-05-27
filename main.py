from flask import Flask, render_template , request , redirect , flash
import os
import sqlite3

app= Flask(__name__)

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS buku (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          judul text,
          penulis_id text,
          penerbit_id text,
          tahun_terbit text,
          isbn text,
          stok integer
          )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS penerbit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        alamat TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS penulis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        negara TEXT
    )
''')

conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('dashboard/index.html')

@app.route('/buku', methods=['GET','post'])
def buku():
    if request.method == 'post':
            judul = request.form['judul']
            penulis_id = request.form['penulis_id']
            penerbit_id = request.form['penerbit_id']
            tahun_terbit = request.form['tahun_terbit']
            isbn = request.form['isbn']
            stok = request.form['stok']

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO buku (judul, penulis_id, penerbit_id, tahun_terbit, isbn, stok) VALUES (?, ?, ?, ?, ?, ?)'),
            (judul, penulis_id, penerbit_id, tahun_terbit, isbn, stok)
            conn.commit()
            conn.close()

            print("data berhasil disimpan")

            return redirect('/daftar')
    return render_template('buku/buku.html')

@app.route('/daftar')
def daftar_buku():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM buku")
    buku_list = c.fetchall()
    conn.close()

    return render_template('buku/daftar.html', buku_list=buku_list)

@app.route('/penulis')
def daftar_penulis():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM penulis")
    penulis_list = cursor.fetchall()
    conn.close()
    return render_template('penulis/penulis.html', penulis_list=penulis_list)

@app.route('/penerbit')
def daftar_penerbit():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM penerbit")
    penerbit_list = cursor.fetchall()
    conn.close()
    return render_template('penerbit/penerbit.html', penerbit_list=penerbit_list)

if __name__ == '__main__':
    app.run(debug=True)