# Climate-API

![Hawaii Surfer](images/surfs-up.jpeg)

In this demonstration, I will build an API exposing historical weather measurements in Hawaii. It will allow a user to select vacation location and dates, and see typical climate during their prosepective trip.

I will explain how to go from data contained in .csv files, to a functional, useful web-hosted API. Let's get started!

## Data Exploration

Data source: [NOAA Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/datasets)

The data we will be working with is comprised of two .csv files, contained in the Input folder:
- `hawaii_measurements.csv`, a collection of weather measurements with the following columns:
    - `station`, a unique station code
    - `date`, a yyyy-mm-dd format date
    - `prcp`, precipitation, in inches
    - `tobs`, observed temperature, in degrees Farenheit

- `hawaii_stations.csv`, a collection of station-specific information with the following columns:
    - `station`, a unique station code
    - `name`, a unique station name
    - `latitude`
    - `longitude`
    - `elevation`, in feet

As you can see, the `station` column is present in both .csv files, and serves to link the two.


## Strategy

In order to build a robust API from the .csv data, we will need to:
1. Clean the measurement data, and decide what to do with any missing values
2. Load the cleaned csv data into an SQLite database for portability and fast access, using SQLAlchemy
3. Create a Flask application to query and serve data from the database based on user input
4. Host the application on Heroku so others can use it

[SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/latest/)
[Flask Documentation](http://flask.pocoo.org/docs/1.0/)
[Heroku Documentation](https://devcenter.heroku.com/categories/reference)

## Data Cleaning

In order for the API to function well, we need to ensure that the source data is free from N/A and missing values. The simple strategy of dropping any incomplete rows from the two .csv files is outlined in `data_engineering.ipynb`. This resulted in a loss of 7.4% of the data, or 1447 dropped rows. Often so much data would be lost in this approach that it would be best to impute it, but this method is sufficient for our purposes in building the API.

The cleaned data is stored in the `Output` folder, and can now be converted to an SQLite database using SQLAlchemy

## Database

To make a performant API, we have to store the data in such a way that it can be accessed quickly and queried easily. In order to accomplish this, we will store the data in an SQLite database.

SQLAlchemy offers a method for interacting with relational databases like SQLite with Python, by creating a mapping between Python objects and records (rows) in the relational database. 

The steps to load a `.csv` file like ours into an SQLite database are as follows:
1. Write Python classes that describe the schema of each table in the database.
2. Create and establish a connection to a database.
3. Reflect the established schema to the database.
4. Convert rows of `.csv` data into Python class objects.
5. Open a session to convert these objects to relational database rows, and insert them into the database.

Once this is done, you can easily query the database inside of Python, and SQLAlchemy will convert these relational database rows back into objects for manipulation. SQLAlchemy tracks any subsequent changes to these objects during a session, and reflects changes to the database upon committing.

This approach is outlined in detail in `database_engineering.ipynb`.

## Climate Analysis

Now that the data 