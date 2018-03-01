from pub_atx.app import db
from pub_atx import data_engineering 


db.drop_all()
db.create_all()
data_engineering.gather_cmpny_data()
data_engineering.load_tables_cmpny_data()