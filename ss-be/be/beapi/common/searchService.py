from elasticsearch import Elasticsearch
from datetime import datetime
import socket

class SearchService:

    def upload(self, type, id, obj ):
        es = Elasticsearch(self.getElasticUrl())
        es.index(body=obj,index=self.getIndexName(), doc_type=type, id=id )

    def searchTxns(self, cardId, query, start, limit):
        res = []
        try:
            es = Elasticsearch(self.getElasticUrl())
            payload = {
                       "query": {
                          "filtered": {
                                    "query": {
                                        "query_string": {
                                            "query": "*"+query+"*",
                                        }
                                    },
                                    "filter": {
                                        "term": {
                                              "cardId": cardId
                                        }
                                    }
                                }

                            }
                       }
            json =  es.search(index=self.getIndexName(), body=payload)
            hits = json["hits"]["hits"]
            for hit in hits:
                res.append(hit["_source"])
        except Exception as ex:
            print "Exception is "+ex.message

        return res

    def getIndexName(self):
        indexName="ss"
        if(socket.gethostname().lower() == "vipins-macbook-pro-2.local"):
            indexName = "vipins-macbook-pro-2.local"
        return indexName

    def getIndexUrl(self):
        return self.getElasticUrl()+"/"+self.getIndexName()

    def getElasticUrl(self):
        return "https://xqx1cw1zvu:suup3oylzm@ss-9534518376.eu-west-1.bonsai.io"