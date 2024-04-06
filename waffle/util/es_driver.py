# -*- coding: utf-8 -*-

import sys

import requests
import json
from waffle.config.database import ElasticSearch


class ESdriver(object):
    """
       Legacy Class
    """
    def __init__(self, es_base_url, es_index, es_type):
        self.url = "%s/%s/%s" % (str(es_base_url),
                                 str(es_index),
                                 str(es_type))

    def post_to_es(self, es_data):
        r = requests.post(self.url,
                          data=json.dumps(es_data, ensure_ascii=False))
        response = r.text
        return response


class ES(object):
    def __init__(self,
                 es_search_url=ElasticSearch.es_search_url,
                 es_index_url=ElasticSearch.es_index_url):
        """
        Define ES connection urls
        :param url:
        :return:
        """
        self.es_search_url = es_search_url
        self.es_index_url = es_index_url

    def insert(self, es_index, es_type, doc):
        """
        Post A json doc into ES server (indexing)
        :param es_index:
        :param es_type:
        :param doc:
        :return:
        """
        index_url = "%s/%s/%s" % (str(self.es_index_url),
                                  str(es_index),
                                  str(es_type)
                                  )
        r = requests.post(self.es_index_url,
                          data=json.dumps(doc, ensure_ascii=False))
        response = r.text
        return response

    def search(self, query):
        """
        Proceed am elastic search based on the search query string
        :param query:
        :return:
        """
        r = requests.post(self.es_search_url,
                          data=json.dumps(query, ensure_ascii=False))
        response = r.text
        return response


if __name__ == "__main__":
    query = {"query":{"bool":{"must":[{"query_string":{"default_field":"_id","query":"b0f020a51b2c929ad296ad6b5f7a0f52"}}],"must_not":[],"should":[]}},"from":0,"size":3,"sort":[],"facets":{}}
    my_es = ES()
    res = my_es.search(query)
    print(res)
