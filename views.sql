create view article_views as
SELECT slug as article_slug, count(articles.slug) as count
        FROM articles, log
        WHERE log.path = CONCAT('/article/', articles.slug)
        and log.status LIKE '200%'
        GROUP BY articles.slug;

CREATE VIEW requests_by_date as 
SELECT date(time) as day, count(*) as requests
FROM log
GROUP BY day;

CREATE VIEW errors_by_date as
    SELECT date(time) as day, count(*) as errors
    FROM log
    WHERE log.status not like '200%'
    GROUP BY day;
