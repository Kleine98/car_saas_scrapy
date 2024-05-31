# settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_NAME = 'myproject'

SPIDER_MODULES = ['car_saas.spiders']
NEWSPIDER_MODULE = 'car_saas.spiders'

ROBOTSTXT_OBEY = True

#ITEM_PIPELINES = {
#    'myproject.pipelines.MongoDBPipeline': 300,
#}

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

LOG_LEVEL = 'DEBUG'
