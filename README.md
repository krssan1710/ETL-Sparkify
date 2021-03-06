# Sparkify Datawarehouse Project

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their  user activity data (Log dataset), and their song master data (Song dataset).

The goal of this project is to create a Postgres database with tables designed to optimize queries on song play analysis.

The data used for this project is a subset of the [Million Song Dataset](http://millionsongdataset.com/)

## Song Dataset

Song master data is stored in multiple files which are present in multiple directories. Each file is in JSON format and contains metadata about a song and the artist of that song. 

This file contributes data to:
- *Songs* dimension table
- *Artists* dimension table

## Log Dataset

The second dataset consists of log files in JSON format generated by user activity on the Sparkify music app. The log files in the dataset are partitioned by year and month.

This file contributes data to:
- *Users* dimension table
- *Time* dimension table
- *Songplays* fact table

## ETL Design

This project uses ***Python (Pandas, NumPy, JSON etc. libraries)*** to process JSON files in the dataset, and load data into a Postgres data warehouse. The overall solution is split into the following .py files.

### sql_queries.py

This file is used to define SQL queries to ***DROP, CREATE, INSERT, TRUNCATE and SELECT*** tables in the target data warehouse. The other files in the project import this python files and execute queries defined in it on the Postgres database.

### create_tables.py

This file creates the database, named ***sparkifydb*** and creates all the target tables. Tables are created in a ***STAR SCHEMA*** in the structure shown below:

![Sparkify-ERD](https://github.com/krssan1710/ETL-Sparkify/blob/master/Sparkify_ERD.png)

This file sets up the target environment. So if the project is being executed for the first time, this file must be the first to be executed.

### etl.py

This file contains the full ETL logic to 1) read all files in the dataset, 2) process the JSON data and convert it into a relational structure, and 3) load it into appropriate target data warehouse tables.

## Running the project for the first time

1) Make sure proper database connection parameters are present in *etl.py* and *create_tables.py*
2) Run *create_tables.py*
3) Make sure the correct data set folder path is specified in *etl.py*
3) Run *etl.py*

## Running the project multiple times

1) Do not run *create_tables.py* if you don't want to change the database table structure
2) Run *etl.py*
3) ETL is set up to ***UPSERT*** records in USERS table
4) Duplicate SONGS and ARTISTS records are ignored during load to avoid duplication in the master dimension tables

## Other files

### etl.ipynb

This notebook was only used to build the ETL logic on one file. The logic was copied over to etl.py to process the full dataset. 

### test.ipynb

This notebook was only used to test if data was loaded via SELECT statements.

    
    