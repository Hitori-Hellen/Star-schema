# Star-schema
Basic knowledge about Star schema and a small demo using Python and PostgreSQL.
# Run
First, you will need to install some dependences for this project. You may need a virtualenv for this.

```
$ pip install -r requirements.txt
```
Note: if you are using Linux or Mac, the library for PostgreSQL will be pyscopg2-binary.

Second, you need to create database table in you database by running the create file

## Windows
```
$ python Create_Table.py
```

## Linux
```
$ python3 Create_Table.py
```
After that, change the connection url to your database.
Then run the etl file to load the data to the database

## Windows
```
$ python etl.py
```

## Linux
```
$ python3 etl.py
```
Done

# P/s:
This is just a small demo about Star schema by using python and PostgreSQL
