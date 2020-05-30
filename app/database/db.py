import databases
import os

db_user = os.getenv('DB_USER', 'postgres')
db_host = os.getenv('DB_HOST', '127.0.0.1')
db_port = os.getenv('DB_PORT', '12100')
db_name = os.getenv('DB_NAME', 'mvp_metric')
db_password = os.getenv('DB_PASSWORD', 'postgres')

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

database = databases.Database(DATABASE_URL)