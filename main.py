import os
import psycopg2
import json
import urlparse
from flask import Flask, request, abort

app = Flask(__name__, static_folder='static')
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

# Serves Static HTML
@app.route('/')
def main():
    return app.send_static_file('index.html')

# Find Guest and Return Guest Status
@app.route('/rsvp-get/<name>')
def rsvp_get(name):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    cur = conn.cursor()

    guest = get_guest(cur,name)

    cur.close()
    conn.close()

    return json.dumps(guest, ensure_ascii=False)

# Updates Guest List with RSVP Info
@app.route('/rsvp-set/<name>', methods=['POST'])
def rsvp_set(name):
    # TODO non existant input may cause an error
    rsvp1 = request.form.get('rsvp1')
    rsvp2 = request.form.get('rsvp2')
    plus1_name = request.form.get('plus1_name')
    note = request.form.get('note')
    location = request.form.get('location')

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    cur = conn.cursor()
    
    guest = get_guest(cur,name)

    # TO DO ADD NOTE
    if guest['name2'] == None and guest['plus1_allowed']:
        cur.execute('UPDATE guest SET rsvp1=(%s), plus1_name=(%s), note=(%s), location=(%s) WHERE name1=(%s)',
                (rsvp1,plus1_name,note,location,name,))
    elif guest['name2'] == None and not guest['plus1_allowed']:
        cur.execute('UPDATE guest SET rsvp1=(%s), note=(%s), location=(%s) WHERE name1=(%s)',
                (rsvp1,note,location,name,))
    else:
        cur.execute('UPDATE guest SET rsvp1=(%s), rsvp2=(%s), note=(%s), location=(%s) WHERE name1=(%s) OR name2=(%s)',
                (rsvp1,rsvp2,note,location,name,name,))
    conn.commit()
    cur.close()
    conn.close()
    
    return ""

# Create guest object with guest properties
def create_guest(guest_cols):
    guest={}
    guest['name1']=guest_cols[0]
    guest['name2']=guest_cols[1]
    guest['plus1_allowed']=guest_cols[2]
    guest['plus1_name']=guest_cols[3]
    guest['rsvp1']=guest_cols[4]
    guest['rsvp2']=guest_cols[5]
    guest['note']=guest_cols[6]
    guest['location']=guest_cols[7]
    return guest

def get_guest(cursor,name):
    cursor.execute('SELECT name1, name2, plus1_allowed, plus1_name, rsvp1, rsvp2, note, location ' +
        'FROM guest WHERE name1 = (%s) OR name2 = (%s)', (name,name,))
    guest_cols=cursor.fetchone()
    # if guest is not on the list
    if guest_cols == None:
        abort(401)
    # otherwise create the guest
    guest=create_guest(guest_cols)
    return guest

# Debug logger
if __name__ == "__main__":
    app.debug = True
    app.run()
