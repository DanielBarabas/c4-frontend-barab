import psycopg2
from config import load_config
import pandas as pd
import psycopg2.extras
import random

config = load_config(filename="backend/database.ini")


def query_series(criteria_list=["Sex & Nudity", "Severe", "Profanity", "Moderate"]):
    # All the input strings should have ' instead of " because of some funny sql syntax

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

    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(rows) > 0:
        return random.choice(rows)[1]
    else:
        return "There are no series that satisfy your needs. Try pornhub instead"
    
def query_plot(criteria_list=["Sex & Nudity", "Severe"]):
    sql = """ 
    select s.t, s.title, s.rate
    from series s
    join parentalguides pg on s.t = pg.t
    where cat = '{}' and level = '{}'
    group by s.title, s.rate
    having count(distinct cat) = 2
    """.format(
        *criteria_list
    )

    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(rows) > 0:
        return random.choice(rows)[1]
    else:
        return "There are no series that satisfy your needs. Try pornhub instead"
