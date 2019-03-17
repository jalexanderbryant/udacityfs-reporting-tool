# News Website Statistics

## Description
This project is a small reporting engine for a news article website. It sets up an article database using PostgreSQL, and runs queries against it with a python script (app.py) to generate statistics and answer the following questions:
>   * What are the most popular three articles of all time?
>   * Who are the most populare article authors of all time?
>   * On which days did more than 1% of requests lead to errors?

In the interest of modularity and cleanliness, the code within **app.py**  have been wrapped in a single class. Once a report is generated (class is instantiated), there are 4 public functions available to retrieve data:
* **get_most_popular_articles** - Prints the 'x' most popular articles. 'x' defaults to 3 but can be changed in the method call.
* **get_most_popular_authors** - Gets the most popular articles by the number of times their articles have been viewed.
* **get_errors_over_threshold** - Print any days where incoming requests resulted in errors over the specified threshold. Error is any request that did not result in a HTTP Status code of 200. Threshold defaults to 1.0% but can be changed in the method call.
* **terminate** - closes the database connection

## Requirements
* [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_2)
> * There are some known issues that prevent vagrant from working with the latest version of virtualbox thus, you should download version one of the VirtualBox **5.2 builds**. For this project, I used **5.2.26**
> * Follow the link provided and download/install the appropriate package for you operating system.
> * No setup required for Virtualbox besides installation. We'll be using it to run a Vagrant instance.

* [Vagrant](https://www.vagrantup.com/downloads.html) - Download and install the latest version for your operating system.
* [VagrantFile as provided by Udacity](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) - With vagrant installed, download this file and run the following commands to setup:
```
> git clone git@github.com:udacity/fullstack-nanodegree-vm.git virtual_machine
> cd virtual_machine/vagrant
> vagrant up --provision
```

* [Python 3](https://www.python.org/downloads/) - [Installation Instructions](https://realpython.com/installing-python/)
* [PostgreSQL](https://www.postgresql.org/download/) - Run the following commands to install and setup:
```
Linux (Ubuntu, Debian, Mint, etc)
> sudo apt-getinstall postgresql
For MacOS:
> brew install postgresql
```
* [pip](https://pip.pypa.io/en/stable/installing/)
```
> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
> python3 get-pip.py
```
* [psycopg2 Library](http://initd.org/psycopg/docs/install.html)
```
> pip install psycopg2
```

## Setting Up and Running the App
With the above requirements installed, run the following to setup and run the application:
```
# Clone the repo into the shared folder within the virtual machine's directory
> cd virtual_machine/vagrant
> git clone git@github.com:jalexanderbryant/udacityfs-reporting-tool.git reporting
> cd reporting

# Unzip the SQL dump and use it to populate the database
> unzip newsdata.sql
> psql -d news -f newsdata.sql

# Create the Views
> psql -d news -f views.sql

# Start the application:
> python3 app.py
```

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