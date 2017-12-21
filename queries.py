# Code written by: Memo Khoury
import datetime
import psycopg2
import csv
import sys

"""In this file, we will define the queries,
   and run them one by one. Ideally, we want
   the final product to be displayed on a
   www server hosted as a guest."""


def first_query():
    """In the first query, we want to fetch
       the top 3 rows that contain the article
       names with the greatest views"""

    db_name = "news"
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()

    # Our first query selects the article title
    # and it's number of views after aggregating
    # the database to match the path name LIKE
    # the slug name. The reason why we use LIKE
    # is to concatenate the "/article/" to the
    # article's slug. Doing this successfully
    # matches the article's appended slug with
    # the log path. After receiving those results,
    # fetch only the first 3 rows to get the three
    # juiciest articles of all time!

    first_query = """select art.title, count(*) as views
                     from articles as art, log as l
                     where l.path like concat('/article/', art.slug)
                     group by art.title
                     order by views desc
                     fetch next 3 rows only"""
    print """Executing first query. Please stand by while we
             query the data.\n"""
    c.execute(first_query)
    first_query_results = c.fetchall()
    # Here, the first_query results are stored in
    # a variable by the fetch all command. We print
    # no results if there are no rows. Otherwise
    # we print the results of the query, tuple by
    # tuple.
    if c.rowcount == 0:
        print "Query returned no results!\n"
    else:
        for row in first_query_results:
            print(row)

    print "First query is complete\n"
    db.close()


def second_query():
    """In the second query, we want to fetch the top
       authors of all time. We add on top of the logic of
       our first query by making sure that the author of
       article (id) = the id of the author."""

    db_name = "news"
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()

    # First, we select the author name and number of hits
    # that were aggregated from equating the author ID with
    # the article's author (in ID), AND equating the path of
    # the log with the concatenated slug of the article.
    # Since we want the top authors, and not only three,
    # we don't fetch the first three or n number of tuples.
    second_query = """select auth.name, count(*) as views
                      from articles as art, authors as auth, log as l
                      where art.author = auth.id
                      and l.path like concat('/article/', art.slug)
                      group by auth.name
                      order by views desc"""
    print """Executing second query. Please stand by while we
             query the data.\n"""
    c.execute(second_query)
    second_query_results = c.fetchall()

    if c.rowcount == 0:
        print "Second query returned no results!\n"
    else:
        for row in second_query_results:
            print(row)
    print "Second query is complete\n"
    db.close()


def third_query():
    """In the third query, we want to fetch the day where the
        percentage of users who encountered errors requesting
        to access website is greater than 1%"""

    db_name = "news"
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()

    # To perform this query, it took me a while to code around
    # a subquery. However, as I read the documentation and the
    # similar problems encountered by the community, I realized
    # that I can simply filter the count results by the filter
    # function, thanks to PSQL. In this query, we select the
    # date as day, and the division of the requests that lead to
    # errors by the total number of requests. This will give us
    # the percentage of errors. We aggregate this data in the
    # month of July. Finally, after the data aggregation, we
    # fetch the tuples that gives us the percentage > 1.0% !
    third_query = """select time::date as day,
                     round(count(status) filter
                     (where status = '404 NOT FOUND') * 100::numeric
                     / count(status)::numeric, 2) as error_percent
                     from log
                     where time::date between
                     to_date('2016-07-01', 'yyyy-mm-dd')
                     and to_date('2016-07-31', 'yyyy-mm-dd')
                     group by time::date
                     having round(count(status) filter
                     (where status = '404 NOT FOUND')* 100::numeric
                     /count(status)::numeric, 2) > 1.0"""

    print """ Exeuting third query. Please stand by while we
              query the data.\n"""
    c.execute(third_query)
    third_query_results = c.fetchall()

    if c.rowcount == 0:
        print "Third query returned no results!\n"
    else:
        for row in third_query_results:
            print(row)
    db.close()

def user():
    user_greeting = """Please select the following:
          1) Find the top 3 articles of all time OR
          2) Find the top authors of all time OR
          3) Find the day where more than 1 percent OR
          of the requests lead to errors OR
          0) Exit program \n"""
    user_input = input(user_greeting)
    if user_input == 1:
        first_query()
        user()
    elif user_input == 2:
        second_query()
        user()
    elif user_input == 3:
        third_query()
        user()
    elif user_input == 0:
        print "Exiting program\n"
        sys.exit()
    else:
        print "Invalid input!\n"
        user()

user()
