import psycopg2
from config import load_config, load_config_iam
import pandas as pd
import psycopg2.extras
import random

"""
config_local = load_config(filename="database.ini",section="postgresql")
config_aws_master = load_config(filename="database.ini",section="aws")

"""

config_aws_iam = load_config_iam(
    filename="database_shareable.ini", section="aws-database-1"
)


def execute_query(sql, config):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows


def query_plot_one_criterum(
    criteria_list=["Sex & Nudity", "Severe"], config=config_aws_iam
):
    sql = """ 
    select s.title, pg.rate
    from series s 
    join parentalguides pg on s.t = pg.t
    where cat = '{}' and level = '{}'
    order by pg.rate DESC
    LIMIT 5
    """.format(
        *criteria_list
    )
    rows = execute_query(sql=sql, config=config)
    if len(rows) > 0:
        return_df = pd.DataFrame(rows)
        return_df.columns = ["series", "rate"]
        return return_df
    else:
        return "There are no series that satisfy your needs. Try pornhub instead"


def query_series(
    criteria_list=["Sex & Nudity", "Severe", "Profanity", "Moderate"],
    config=config_aws_iam,
):
    sql = """ 
    select s.t, s.title
    from series s
    join parentalguides pg on s.t = pg.t
    where (cat = '{}' and level = '{}')
    or (cat = '{}' and level = '{}')
    group by s.t, s.title
    having count(distinct cat) = 2
    """.format(
        *criteria_list
    )
    rows = execute_query(sql=sql, config=config)
    if len(rows) > 0:
        return random.choice(rows)[1]
    else:
        return "There are no series that satisfy your needs. Try pornhub instead"


def query_plot_two_criteria(
    criteria_list=["Sex & Nudity", "Severe", "Profanity", "Moderate"],
    config=config_aws_iam,
):
    sql = """ 
    WITH SeriesRates AS (
    SELECT s.title, p.cat, p.rate,
           SUM(p.rate) OVER (PARTITION BY s.title) AS total_rate
    FROM series s
    JOIN parentalguides p ON s.t = p.t
    WHERE (p.cat = '{}' AND p.level = '{}')
       OR (p.cat = '{}' AND p.level = '{}')
    )
    SELECT title, cat, rate
    FROM SeriesRates
    WHERE total_rate IN (
        SELECT DISTINCT total_rate
        FROM SeriesRates
        ORDER BY total_rate DESC
        LIMIT 5
    )
    ORDER BY total_rate DESC, title, rate DESC;
    """.format(
        *criteria_list
    )
    rows = execute_query(sql=sql, config=config)
    if len(rows) > 0:
        return_df = pd.DataFrame(rows)
        return_df.columns = ["series", "category", "rate"]
        return return_df
    else:
        return "There are no series that satisfy your needs. Try pornhub instead"
