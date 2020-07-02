# Restaurant Ratings
This is a simple Python application that retrieves information about new restaurants from the **Yelp Fusion API**, stores the data in a database using **SQLite**, and plots the data in the form of a line graph using **matplotlib**. 

## VISUAL (insert later)

## Setup
1. Clone this repository to your computer and use the command `$ pip install -r requirements.txt` to install the packages that are required to run the application.

2. Obtain an API key from the [Yelp Fusion API](https://www.yelp.com/fusion) website and paste it into `hidden.py` as a string.

## Usage
After following the steps outlined in [Setup](https://github.com/TylerWon/restaurant-ratings#setup), run `yelp.py`.
On the first run, it will ask you for the name of a city to start its initial search. For the subsequent runs, it will automatically retrieve information about the restaurants already stored in the database.

To see a visualization of the data, run `plot.py` which will create a line-graph of the data currently stored in the database.

**Note**: `dump.py` outputs information about each restaurant stored in the database and can be used to quickly ensure that the data is being properly retrieved from the API and inserted into the database.

## Built With
* [matplotlib](https://matplotlib.org/) - A Python library to create high-quality visualizations
* [SQLite](https://www.sqlite.org/index.html) - The database engine used
* [Yelp Fusion API](https://www.yelp.com/fusion) - Provides multiple endpoints to retrieve information about businesses, businesses categories, and events


## License
> You can check out the full license [here](https://github.com/TylerWon/restaurant-ratings/blob/master/LICENSE)

This project is licensed under the terms of the MIT license. 
