import psycopg2

class Report(object):
    def __init__(self, connection='news'):
        self._conn = psycopg2.connect("dbname=%s" %(connection))
        self._cursor = self._conn.cursor()

    def _run_query(self,query, params=()):
        """ Runs a query and returns the unprocessed results """
        self._cursor.execute(query, params)
        return self._cursor.fetchall()

    def get_most_popular_articles(self, x_most_popular=3):
        """ Get the 'x' most popular articles. Print as a formatted list """
        query = """ SELECT articles.title, subq.count as page_views
                        FROM articles,
                            (SELECT * from article_views) as subq
                        WHERE articles.slug = subq.article_slug
                        ORDER BY page_views desc
                        LIMIT %s;
                """
        result = self._run_query(query, (x_most_popular,) )
        print("\n{} Most Popular Articles:".format(x_most_popular))
        for item in result:
            print("{} - {}".format(item[0].title(), item[1]))
        print("\n")

    def get_most_popular_authors(self):
        """ Get the most popular authors """
        query = """ SELECT authors.name, author_by_page_views.total_views as count
                    FROM authors 
                    JOIN (SELECT articles.author, SUM(subq.count) as total_views
                    FROM articles, authors, (SELECT * from article_views) as subq
                    WHERE authors.id = articles.author
                        and articles.slug = subq.article_slug
                    GROUP BY articles.author) as author_by_page_views
                        on authors.id = author_by_page_views.author
                    ORDER BY count desc;
            """
        result = self._run_query(query)
        print("\nMost Popular Authors:")
        for item in result:
            print("{} - {} views".format(item[0], str(item[1])))
        print("\n")


    def get_errors_over_threshold(self, threshold=1.0):
        """ Get any days where incoming requests resulted in errors over the 
            specified threshold. In this case, 1.0% 
        """
        query = """ SELECT to_char(r.day, 'FMMonth DD, YYYY'), r.requests as reqs, e.errors as errs,
                   to_char(round(100*(e.errors::decimal/r.requests), 2), 'FM9D99') as percent_errors 
                   FROM requests_by_date as r, errors_by_date as e
                    WHERE r.day = e.day
                    and round(100*(e.errors::decimal/r.requests), 2) > %s;
                """
        result = self._run_query(query, (threshold,))
        print("{} - {}% errors".format(result[0][0], result[0][3]))
        print("\n")


def main():
    """ App entry point """
    report = Report()
    report.get_most_popular_articles(3)
    report.get_most_popular_authors()
    report.get_errors_over_threshold(1.0)

main()
