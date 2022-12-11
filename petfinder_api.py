import requests
import json 
import os
import sqlite3


api_key = "25KmFzF7mqAiSsReISZphGQ9S843SseGbfiQnzQH5hLc4qj6iK"
api_secret = "uhdeONDWDcqiWmU1sR9aNk5DVCQhVY8BKOe0pIut"



data = {
    'grant_type': 'client_credentials',
    'client_id': '25KmFzF7mqAiSsReISZphGQ9S843SseGbfiQnzQH5hLc4qj6iK',
    'client_secret': 'uhdeONDWDcqiWmU1sR9aNk5DVCQhVY8BKOe0pIut',
}

response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)
token = response.json()['access_token']

headers = {
    'Authorization': f'Bearer {token}',
}


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_orgs_table(cur,conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Orgs (id TEXT PRIMARY KEY, name TEXT, email TEXT, phone TEXT, url TEXT, distance REAL)')
    conn.commit()
    
def get_orgs():
    responses = {}
    #response = requests.get('https://api.petfinder.com/v2/organizations', params=params, headers=headers)
    #responses = response.json()
    #print(json.dumps(response.json(),indent=2))
    #note: only 61 orgs
    
    for i in range(1,5):
        params = {
            'limit':25,
            'location': '48104',
            'distance': 100,
            'page': i
        }
        responses[f"page{i}"] = requests.get(f'https://api.petfinder.com/v2/organizations',params=params, headers=headers).json()
    return responses
    #print(org_ids)

    #org_ids = ['MI452', 'MI648', 'MI524', 'MI144', 'MI484', 'MI1003', 'MI1089', 'MI833', 'MI935', 'MI857', 'MI175', 'MI382', 'MI721', 'MI866', 'MI937', 'MI820', 'MI235', 'MI504', 'MI60', 'MI170', 'MI120', 'MI116', 'MI337', 'MI915', 'MI951', 'MI998', 'MI318', 'MI1120', 'MI1086', 'MI579', 'MI590', 'MI1060', 'MI40', 'MI724', 'MI246', 'MI495', 'MI1140', 'MI380', 'MI679', 'MI253', 'MI1077', 'MI467', 'MI1146', 'MI704', 'MI1083', 'MI1151', 'MI1002', 'NY867', 'MI232', 'MI1153', 'MI1157', 'MI1141', 'MI193', 'MI453', 'MI1025', 'MI1111', 'MI1171', 'MI813', 'MI943', 'MI1112', 'MI408']

def add_orgs_from_responses(cur,conn,responses):
    count = 0
    for i in range(1,5):
        for org in responses[f"page{i}"]["organizations"]:
            if(count > 24): 
                break
            count += add_org_to_database(cur,conn,org)
        if(count > 24):
            break
    conn.commit()

def add_org_to_database(cur,conn,org):
    if(len(cur.execute("SELECT id FROM Orgs WHERE id = ?",(org["id"],)).fetchall()) == 0):
        cur.execute("INSERT OR IGNORE INTO Orgs (id, name, email, phone, url, distance) VALUES (?,?,?,?,?,?)", (org["id"],org["name"],org["email"],org["phone"],org["url"],org["distance"]))
        conn.commit()
        return 1
    else: 
        return 0
    
    



def create_animals_table(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Animals (id INTEGER PRIMARY KEY, organization_id TEXT, breed TEXT, gender TEXT, primary_color TEXT, age TEXT, status TEXT, distance REAL)")

def get_animals():
    responses = {}
    for i in range(1,5):
        params = {
            'limit':25,
            'location': '48104',
            'type': 'Cat',
            'distance': 100,
            'page': i
        }
        responses[f"page{i}"] = requests.get(f'https://api.petfinder.com/v2/animals',params=params, headers=headers).json()
    return responses

def add_animal_to_database(cur,conn,animal):
    if(len(cur.execute("SELECT id FROM Animals WHERE id = ?",(animal["id"],)).fetchall()) == 0):
        cur.execute("INSERT OR IGNORE INTO Animals (id, organization_id, breed, gender, primary_color, age, status, distance) VALUES (?,?,?,?,?,?,?,?)", (animal["id"],animal["organization_id"],animal["breeds"]["primary"],animal["gender"],animal["colors"]["primary"],animal["age"],animal["status"],animal["distance"]))
        conn.commit()
        return 1
    else: 
        return 0


def add_animals_from_responses(cur,conn,animal_responses):
    count = 0
    for key in animal_responses.keys():
        for animal in animal_responses[key]["animals"]:
            if(count > 24): 
                break
            count += add_animal_to_database(cur,conn,animal)
        if(count > 24):
            break
    conn.commit()

#create org database
def main():
    cur,conn = open_database("cat_database.db")
    create_orgs_table(cur,conn)
    org_responses = get_orgs()
    add_orgs_from_responses(cur,conn,org_responses)

    create_animals_table(cur,conn)
    animal_responses = get_animals()
    add_animals_from_responses(cur,conn,animal_responses)
    
    print(cur.execute("SELECT gender, COUNT(*) FROM Animals GROUP BY gender").fetchall())
    with open("breed_average_distances.txt",'w') as f:
        rows = (cur.execute("SELECT breed, AVG(distance) FROM Animals GROUP BY breed").fetchall())
        for item in rows:
            f.write(item[0] + ": "+ str(item[1]) + '\n')

    #join 
    rows = cur.execute("SELECT Animals.organization_id, Count(*) FROM Animals INNER JOIN Orgs ON Orgs.id=Animals.organization_id GROUP BY Animals.organization_id").fetchall()

if __name__ == "__main__":
    main()
