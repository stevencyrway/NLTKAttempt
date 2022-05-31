import nltk as nlp
import psycopg2 as db
import pandas as pd
import pandas.io.sql as sqlio
import os

connection = db.connect(database='quasar_prod_warehouse', user='scyrway', password=os.environ['SQLPASS'], host=os.environ['HOST'], port='5432')

data = sqlio.read_sql_query("Select posts.campaign_id, text from posts left outer join campaign_info on posts.campaign_id = cast(campaign_info.campaign_id as varchar) where created_at >= '2022-03-01' and text is not null group by posts.campaign_id, text",connection)

print(data.info())



