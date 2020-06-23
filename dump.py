import sqlite3

# Connect to the database
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

# Retrieve the most recent date from the Dates table
def recent_date(cr):
    cr.execute('SELECT MAX(date) FROM Dates')
    date = cr.fetchone()[0]

    return date

# Display information about each restaurant in the database
def show_restaurants(cr):
    date = recent_date(cr)

    cr.execute('''
    SELECT Restaurants.name, Restaurants.address, Restaurants.category, Restaurants.reviews, Ratings.rating 
    FROM Restaurants JOIN Ratings JOIN Dates
    ON Ratings.restaurant_id = Restaurants.id AND Ratings.date_id = Dates.id
    WHERE date = ?
    ''', 
    (date, ))

    info = cr.fetchall()
    
    print('Displaying information about each restaurant in the database:')
    for name, address, category, reviews, rating in info:
        print('======================================================')
        print('Name:', name)
        print('Address:', address)
        print('Category:',category)
        print('Number of reviews:',reviews)
        print('Rating:',rating)

show_restaurants(cur)
