#!/usr/bin/python

import sys
import tweepy
import datetime
import argparse
from elasticsearch import Elasticsearch

client = Elasticsearch()

parser = argparse.ArgumentParser()
parser.add_argument("sensorName", help="Cowrie Sensor Name - for ES query")
parser.add_argument("sensorLocation", help="Cowrie Sensor Geographic Location - for tweet formatting")
parser.add_argument("--test", help="Don't tweet, just print output to console and exit",action="store_true")
args = parser.parse_args()

startTime = datetime.datetime.now()
endTime = startTime - datetime.timedelta(days=1)
esIndice = "cowrie-" + startTime.strftime("%Y.%m.%d")

response = client.search(
    index=esIndice,
    body={
"size": 0,
  "aggs": {
    "geoCode": {
      "terms": {
        "field": "geoip.country_code2",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      }
    }
  },
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "sensor:"+args.sensorName,
          "analyze_wildcard": True
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": int(endTime.strftime('%s')) * 1000,
                  "lte": int(startTime.strftime('%s')) * 1000,
                  "format": "epoch_millis"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
}
}
)


output = args.sensorLocation + " SSH Attackers  - Last 24hr - "

isData = False

for country in response["aggregations"]["geoCode"]["buckets"]:
        output = output + str(country["key"]) + "(" + str(country["doc_count"]) + "),"
        if country["doc_count"] > 1:
                isData = True

# Drop trailing comma
output = output.rstrip(',')

if isData == True:

        if args.test:
                print output

        else:
                print "Tweeting! " + output
                
                cfg = {
                    "consumer_key"        : "KEY",
                    "consumer_secret"     : "SECRET",
                    "access_token"        : "TOKEN",
                    "access_token_secret" : "TOKENSECRET"
                    }

                auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
                auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
                api = tweepy.API(auth)
                status = api.update_status(status=output)
                
else:
        print "ElasticSearch returned no data, check indices. Raw ES response: " + response