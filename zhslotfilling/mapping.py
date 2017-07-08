# -*-coding:utf-8-*-

from elasticsearch import Elasticsearch

es = Elasticsearch("localhost:9200", timeout=600)

def create_mapping(index_name):
    index_info = {
        'settings':{
            'number_of_replicas': 0,
            'number_of_shards': 5
        },
        'mappings':{
            'zhinfo':{
                'properties':{
                    "content_analyzedzh":{
                        "type": "string",
                        #"store": "no",
                        #"term_vector": "with_positions_offsets",
                        "analyzer": "mmseg_maxword",
                        #"include_in_all": "true",
                        #"boost": 8
                    },
                    "content":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "path":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "source":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            },
            'eninfo':{
                'properties':{
                    "content_analyzeden":{
                        "type": "string",
                        "analyzer": "english"
                    },
                    "content":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "path":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    },
                    "source":{
                        'type': 'string',
                        'index': 'not_analyzed'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)


if __name__=='__main__':
    create_mapping("db")
