from flask import Flask, render_template, request, redirect, url_for
from pony.orm import Database, PrimaryKey, Required, db_session, Set, Optional
from datetime import datetime

app = Flask(__name__)

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    naziv = Required(str)
    opis = Optional(str)
    vrsta_djelatnosti = Required(str)
    datum = Optional(datetime)

db.generate_mapping(create_tables=True)

@app.route('/')
@db_session
def index():
    eventi=Event.select()
    return render_template('index.html', eventi=eventi)

@app.route('/dodaj_event', methods=['POST'])
@db_session
def dodaj_event():
    naziv=request.form['naziv']
    opis=request.form['opis']
    vrsta_djelatnosti=request.form['vrsta_djelatnosti']
    datum=request.form['datum']
    datum = datetime.strptime(datum, '%Y-%m-%d')
    Event(naziv=naziv, opis=opis, vrsta_djelatnosti=vrsta_djelatnosti, datum=datum)
    return redirect(url_for('index'))  

@app.route('/uredi_event/<int:event_id>', methods=['GET', 'POST'])
@db_session
def uredi_event(event_id):
    event = Event[event_id]
    
    if request.method == 'POST':
        
        event.naziv = request.form['naziv']
        event.opis = request.form['opis']
        event.vrsta_djelatnosti = request.form['vrsta_djelatnosti']
        datum = request.form['datum']
        event.datum = datetime.strptime(datum, '%Y-%m-%d')
        
        return redirect(url_for('index'))
    
    return render_template('uredi_event.html', event=event)


@app.route('/obrisi_event/<int:event_id>', methods=['POST'])
@db_session
def obrisi_event(event_id):
    event=Event[event_id]
    event.delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int("5000"),)
    
"""
pokretanje uz docker: docker run -p 5000:5000 eventi:3.1
kreiranje docker imagea: docker build --p tag eventi:3.1 .

"""