from flask import Flask, url_for, redirect, request, make_response, render_template, session, g 
import jinja2
import MySQLdb
import json

app = Flask("Prva flask aplikacija")

app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

@app.before_request
def before_request_func():
    g.connection = MySQLdb.connect(host="localhost", user="app", passwd="1234", db="Seminarski")
    g.cursor = g.connection.cursor()

    if request.path == '/login' or request.path.startswith('/static') or request.path.startswith('/rfid'):
        return
    if session.get('username') is None:
        return redirect(url_for('login'))
    

@app.after_request
def after_request_func(response):
    g.connection.commit()
    g.connection.close()

    return response


@app.get('/')
def index():
    ovl = session.get('ovlasti')
    id_korisnika = session.get('id')

    id = request.args.get('id')
    if id == '1' or id == None:
        g.cursor.execute(render_template('getSkenirano.sql', id_korisnika = id_korisnika))
        skenirano = g.cursor.fetchall()
        list_skeniranog = [
            {'naziv': naziv_proizvoda,'cijena': cijena_proizvoda,'barkod': barkod}
            for naziv_proizvoda, cijena_proizvoda, barkod in skenirano]
        response = render_template('index.html', naslov='Početna stranica', username=session.get('username').capitalize(), ovlasti = ovl, d=1, data=list_skeniranog, col1='Naziv', col2='Cijena', col3='Barkod', col4='', col5='')
        return response, 200
    
    if id == '2':
        g.cursor.execute(render_template('getKorisnike.sql'))
        korisnici = g.cursor.fetchall()
        list_korisnika = [
            {'id': id,'ime': ime,'prezime': prezime,'username': username,'id_ovlasti': id_ovlasti}
            for id, ime, prezime, username, id_ovlasti in korisnici]
        response = render_template('index.html', naslov='Korisnici', username=session.get('username').capitalize(), ovlasti = ovl, d=2, data=list_korisnika, col1='ID', col2='Ime', col3='Prezime', col4='Korisničko ime', col5='Ovlasti')
        return response, 200
    
    if id == '3':
        g.cursor.execute(render_template('getProizvode.sql'))
        proizvodi = g.cursor.fetchall()
        list_proizvoda = [
            {'id': id, 'ime': ime, 'cijena': cijena, 'barkod': barkod} 
            for id, ime, cijena, barkod in proizvodi]
        response = render_template('index.html', naslov='Proizvodi', username=session.get('username').capitalize(), ovlasti = ovl, d=3, data=list_proizvoda, col1='ID', col2='Naziv', col3='Cijena', col4='Barkod', col5='')   
        return response, 200


@app.get('/login')
def login():
    response = render_template('login.html', naslov='Stranica za prijavu')
    return response, 200


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))


@app.post('/login')
def check():
    g.cursor.execute(render_template('selectKorisnik.sql', user=request.form.get('username'), pasw=request.form.get('password')))
    korisnik = g.cursor.fetchall()

    if korisnik != ():
        session['id'] = korisnik[0][0]
        session['username'] = korisnik[0][1]
        session['ovlasti'] = korisnik[0][2]
        return redirect(url_for('index'))
    else:
        return render_template('login.html', naslov='Stranica za prijavu', poruka='Uneseni su pogrešni podatci!')


@app.post('/rfid')
def scanNUID():
    response = make_response()
    request_body = request.data.decode("utf-8")
    skenirano = json.loads(request_body)
    print(skenirano)
    g.cursor.execute(render_template('getKarticu.sql', nuid=skenirano['nuid']))
    upit = g.cursor.fetchall()
    if str(upit) == '()':
        return "BAD", 404
    id_kartice = upit[0][0]
    id_korisnika = id_korisnika=skenirano['user_id']
    print(f"kartica: {id_kartice}, Korisnik: {id_korisnika}")
    g.cursor.execute(render_template('addSkenirano.sql', id_kartice=id_kartice, id_korisnika=id_korisnika))
    print(skenirano)
    
    return response, 200

        

@app.post('/obrisiKorisnika')
def deleteUser():
    userid = request.form.get('id')
    g.cursor.execute(render_template('deleteKorisnik.sql', id=userid))
    return redirect('/?id=2')

@app.post('/dodajKorisnika')
def addUser():
    ime = request.form.get('ime')
    prezime = request.form.get('prezime')
    username = request.form.get('username')
    lozinka = request.form.get('lozinka')
    id_ovlasti = request.form.get('id_ovlasti')
    g.cursor.execute(render_template('addKorisnik.sql', ime=ime, prezime= prezime, username = username, lozinka = lozinka, id_ovlasti = id_ovlasti))
    return redirect('/?id=2')


@app.post('/obrisiProizvod')
def deleteProizovd():
    proizvodid = request.form.get('id')
    g.cursor.execute(render_template('deleteProizvod.sql', id=proizvodid))
    return redirect('/?id=1')

@app.post('/dodajProizovd')
def addProizvod():
    ime = request.form.get('ime')
    cijena = request.form.get('cijena')
    barkod = request.form.get('barkod')
    g.cursor.execute(render_template('addBarkod.sql', barkod=barkod))
    id_kartice = g.cursor.lastrowid
    g.cursor.execute(render_template('addProizvod.sql', ime=ime, cijena= cijena, id_kartice = id_kartice))
    return redirect('/?id=1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)