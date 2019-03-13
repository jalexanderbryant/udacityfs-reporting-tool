# News Website Statistics

## Description
In the interest of modularity and cleanliness, the methods have been wrapped in a single class. Once a report is generated (class is instantiated), there are 4 public functions available to retrieve data:
* get_most_popular_articles - Prints the 'x' most popular articles. 'x' defaults to 3 but can be changed in the method call.
* get_most_popular_authors - Gets the most popular articles by the number of times their articles have been viewed.
* get_errors_over_threshold - Print any days where incoming requests resulted in errors over the specified threshold. Error is any request that did not result in a HTTP Status code of 200. Threshold defaults to 1.0% but can be changed in the method call.
* terminate - closes the database connection

## Requirements
* Virtualbox - https://www.virtualbox.org/wiki/Downloads


    No setup required for Virtualbox besides installation. We'll be using it to run a Vagrant instance. 

* Vagrant - https://www.vagrantup.com/downloads.html


* Python 3 - https://www.python.org/downloads/
* PostgreSQL - https://www.postgresql.org/download/
* psycopg2 Library - http://initd.org/psycopg/docs/install.html

## 

### Example Output:
```
Most Popular Articles:
Candidate Is Jerk, Alleges Rival - 338647
Bears Love Berries, Alleges Bear - 253801
Bad Things Gone, Say Good People - 170098

Most Popular Authors:
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views

Days where over 1% of incoming requests resulted in errors;
July 17, 2016 - 2.26% errors
```

## How to run
0. Run sql dump to setup database
1. Create views.
2. In the command line, CD into 'reporting' directory, then run: `python3 app.py`.


## Views
#### Get a count of each time time an article was visited
```
create view article_views as
SELECT slug as article_slug, count(articles.slug) as count
        FROM articles, log
        WHERE articles.slug = replace(log.path, '/article/', '')
        and log.status LIKE '200%'
        GROUP BY articles.slug;
```

#### Get the number of requests for each day
```
CREATE VIEW requests_by_date as 
SELECT date(time) as day, count(*) as requests
FROM log
GROUP BY day;
```

#### Get the number of requests that resulted in errors for each day
```
CREATE VIEW errors_by_date as
    SELECT date(time) as day, count(*) as errors
    FROM log
    WHERE log.status not like '200%'
    GROUP BY day;
```