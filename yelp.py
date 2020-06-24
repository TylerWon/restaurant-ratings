from datetime import datetime
from hidden import key
import requests
import sqlite3

# API Key
API_KEY = key

# API Constants - Business Search
BASE_URL1 = 'https://api.yelp.com/v3/businesses/search'
RADIUS = 15000
CATEGORIES = 'restaurants'
ATTRIBUTES = 'hot_and_new'

# API Constants - Business ID
BASE_URL2 = 'https://api.yelp.com/v3/businesses/'

# Connect to the database
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

# Create a database with 3 tables: Restaurants, Ratings, and Dates
def create_database(cr):
    cr.executescript('''
    CREATE TABLE IF NOT EXISTS Restaurants (
        id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        yelpid          TEXT UNIQUE,
        name            TEXT,
        address         TEXT UNIQUE,
        category        TEXT,
        reviews         INTEGER
    );
    CREATE TABLE IF NOT EXISTS Dates (
        id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date            TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Ratings (
        id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        rating          DECIMAL,
        date_id         INTEGER,
        restaurant_id   INTEGER
    )
    ''')
    
create_database(cur)

# Check if an API key was entered
def key_check(key):
    if key is not False:
        print('API key entered.')
    else:
        print('API key not entered.')
        quit()

key_check(API_KEY)

# Check the database to see if there is data already
def check_database(cr):
    cr.execute('SELECT * FROM Restaurants')
    total = cr.fetchone()

    if total is None:
        print('No data found.')
        indicator = False

    else:
        print('Data found, checking for new ratings...')
        indicator = True
    
    return indicator

indicator = check_database(cur)

# Retrieve the yelp ids of the restaurants in the database and return them
def retrieve_yelpids(cr):
    cr.execute('SELECT yelpid FROM Restaurants ORDER BY id')
    temp = cr.fetchall()

    yelpids = list()
    for i in temp:
        yelpid = i[0]
        yelpids.append(yelpid)

    return yelpids

# Conduct a business id search using the Yelp API and return the data
def get_data_id(ypid):
    id = ypid
    headers = {'Authorization': 'Bearer %s' % API_KEY}

    response = requests.get(BASE_URL2 + id, headers=headers)
    data = response.json()

    return (data, response)

# Update reviews in Restaurants table, add new ratings in Ratings table, and add new date (if applicable) in Dates table
def update_data(d, cr, cn, ypid):
    # Dates Table
    date = datetime.date(datetime.now())
    cr.execute('INSERT OR IGNORE INTO Dates (date) VALUES (?)', (date, ))

    # Restarants Table
    new_reviews = d['review_count']
    cr.execute('UPDATE Restaurants SET reviews = ? WHERE yelpid = ?', (new_reviews, ypid))

    # Ratings Table
    new_rating = d['rating']

    cr.execute('SELECT id FROM Restaurants WHERE yelpid = ?', (ypid, ))
    restaurant_id = cr.fetchone()[0]

    cr.execute('SELECT id FROM Dates WHERE date = ?', (date, ))
    date_id = cr.fetchone()[0]

    cr.execute('''
    INSERT INTO Ratings (rating, date_id, restaurant_id)
    VALUES (?, ?, ?)''',
    (new_rating, date_id, restaurant_id))

    cn.commit()
    
    name = d['name']
    print('Added new rating for',name)

# Conduct a business search of the city entered by the user using the Yelp API and return the data
def get_data_search():
    location = input('Enter a city: ')
    params = {'location': location, 'radius': RADIUS, 'categories': CATEGORIES, 'attributes': ATTRIBUTES}
    headers = {'Authorization': 'Bearer %s' % API_KEY}

    response = requests.get(BASE_URL1, params=params, headers=headers)
    data = response.json()

    return (data, response)

# Insert data into Restaurants, Ratings, and Dates table
def insert_data(res, cr, cn):
    # Dates Table
    date = datetime.date(datetime.now())
    cr.execute('INSERT OR IGNORE INTO Dates (date) VALUES (?)', (date, ))
   
    # Restaurants Table
    yelpid = res['id']
    name = res['name']
    category = res['categories'][0]['title']
    reviews = res['review_count']
    
    street = res['location']['address1']
    city = res['location']['city']
    zipcode = res['location']['zip_code']
    state = res['location']['state']
    address = '%s, %s, %s %s' % (street, city, state, zipcode)

    cr.execute('''
    INSERT OR IGNORE INTO Restaurants (yelpid, name, address, category, reviews)
    VALUES (?, ?, ?, ?, ?)''', 
    (yelpid, name, address, category, reviews))
    
    # Ratings Table
    rating = res['rating']

    cr.execute('SELECT id FROM Restaurants WHERE yelpid = ?', (yelpid, ))
    restaurant_id = cr.fetchone()[0]

    cr.execute('SELECT id FROM Dates WHERE date = ?', (date, ))
    date_id = cr.fetchone()[0]

    cr.execute('''
    INSERT INTO Ratings (rating, date_id, restaurant_id)
    VALUES (?, ?, ?)''',
    (rating, date_id, restaurant_id))

    cn.commit()

    print('Added',name,'to the database.')

# Update tables if data is already present or insert data if database is empty
def update_or_insert(ind, cr, cn):
    if ind:
        yelpids = retrieve_yelpids(cr)
        for yelpid in yelpids:
            data, response = get_data_id(yelpid)
            try:
                update_data(data, cr, cn, yelpid)
                
            except:
                error = data['error']['code']
                print('A',error,'occurred.')
                quit()

    else:
        data, response = get_data_search()
        try:
            restaurants = data['businesses']
            
        except:
            error = data['error']['code']
            print('A',error,'occurred.')
            quit()

        for restaurant in restaurants:
            insert_data(restaurant, cur, conn)

    limit = str(int(response.headers['RateLimit-Remaining']) - 1)
    print('Remaining API calls:',limit)

update_or_insert(indicator, cur, conn)
