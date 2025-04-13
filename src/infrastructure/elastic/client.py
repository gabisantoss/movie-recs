import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

es_host = os.getenv("ELASTICSEARCH_HOST")
es_user = os.getenv("ELASTICSEARCH_USER")
es_pass = os.getenv("ELASTICSEARCH_PASSWORD")

es = Elasticsearch(F"http://{es_host}:9200",
                   http_auth=(es_user, es_pass))
