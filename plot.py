import sqlite3
from matplotlib import pyplot as plt

# Connect to the database
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

# Retrieve the dates from the Dates table and insert them into a list
def retrieve_dates(cr):
    cr.execute('SELECT date FROM Dates')
    temp = cr.fetchall()

    dates = list()
    for i in temp:
        date = i[0]
        dates.append(date)

    return dates

# Retrieve the ids for the restaurants in the Restaurants table
def retrieve_ids(cr):
    cr.execute('SELECT id FROM Restaurants')
    temp = cr.fetchall()

    ids = list()
    for i in temp:
        id = i[0]
        ids.append(id)

    return ids

# Retrieve the ratings for a restaurant from the Ratings table and insert them into a list
def retrieve_ratings(id, cr):
    cr.execute('SELECT rating FROM Ratings WHERE restaurant_id = ?', (id, ))
    temp = cr.fetchall()

    ratings = list()
    for i in temp:
        print(i)
        rating = i[0]
        ratings.append(rating)

    return ratings

# Retrieve the name for a restaurant from the Restaurants table 
def retrieve_name(id, cr):
    cr.execute('SELECT name, address, reviews FROM Restaurants WHERE id = ?', (id, ))
    name = cr.fetchone()[0]

    return name

# Plot the data from the database using matplotlib
def plot_data(cr):
    dates = retrieve_dates(cr)
    ids = retrieve_ids(cr)
    for id in ids:
        ratings = retrieve_ratings(id, cr)
        name = retrieve_name(id, cr)

        plt.plot(dates, ratings, label=name)
        
    plt.title('Change in Ratings of New Restaurants')
    plt.xlabel('Date')
    plt.ylabel('Rating')
    plt.legend(fontsize=8)

    plt.show()

plot_data(cur)
