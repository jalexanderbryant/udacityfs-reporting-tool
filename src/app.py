"""
TODO:
- organize into reusable code
- # class InternalReport(object):
"""
import psycopg2

# Connect to 'news' database
conn = psycopg2.connect("dbname=news")
cur = conn.cursor()

# # Question 1
# q1 = """ SELECT title, count(articles.title) as count
# 			FROM articles, log
# 			WHERE articles.slug = replace(log.path, '/article/', '')
# 			and log.status LIKE '200%'
# 			GROUP BY articles.title
# 			ORDER BY count desc
# 			limit 3;
# 	"""

q1v2 =	""" SELECT articles.title, subq.count as page_views
				FROM articles,
					(SELECT * from article_views) as subq
				WHERE articles.slug = subq.article_slug
				ORDER BY page_views desc
				limit 3;
		"""
# # cur.execute(q1v2);

# # Result of Q1
# print("3 most popular articles")
# for item in cur.fetchall():
# 	print("{} - {}".format(item[0].title(), item[1]))

# # # Question 2
# q2 = """ SELECT articles.slug, articles.author, authors.name, subq.count as page_views
# 			FROM articles, authors, (SELECT * from article_views) as subq
# 			WHERE authors.id = articles.author
# 			and articles.slug = subq.article_slug;
# 	"""

q2 = """ SELECT authors.name, author_by_page_views.total_views as count
			FROM authors 
			join (SELECT articles.author, SUM(subq.count) as total_views
					FROM articles, authors, (SELECT * from article_views) as subq
					WHERE authors.id = articles.author
					and articles.slug = subq.article_slug
					GROUP BY articles.author) as author_by_page_views
			on authors.id = author_by_page_views.author
			ORDER BY count desc;
	"""


q3 = 	"""	SELECT to_char(r.day, 'FMMonth DD, YYYY'), r.requests as reqs, e.errors as errs,
				to_char(round(100*(e.errors::decimal/r.requests), 2), 'FM9D99') as percent_errors 
			FROM requests_by_date as r, errors_by_date as e
			WHERE r.day = e.day
				and round(100*(e.errors::decimal/r.requests), 2) > 2;
		"""
cur.execute(q3)
# print(cur.fetchall())
for item in cur.fetchall():
	print(item[0], item[3])
