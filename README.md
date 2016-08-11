# cowrieStatTweet
Python scripts to tweet interesting stats from Cowrie SSH Honeypot data stored in ElasticSearch.

### cowrieTweet.py
---

### Description

A basic script to pull the top 10 source countries trying to attack the given Cowrie sensor over the last 24 hours and tweet the results via the twitter API.

### Usage

Usage: cowrieTweet.py [-h] [--test] sensorName sensorLocation

*Positional arguments:*

sensorName      Cowrie Sensor Name - for ES query

sensorLocation  Cowrie Sensor Geographic Location - for tweet formatting

*Optional arguments:*

-h, --help      show this help message and exit
--test          Don't tweet, just print output to console and exit

Example - cowrieTweet.py "SKOREA" "South Korea"

### Instructions

This script is hardcoded to query an elasticsearch indice with the name format "cowrie-YYYY.MM.DD". If your's is different, you will need to change the esIndice value in the script.

We are also assuming that you have enriched the cowrie output using logstash or similar to include standard GeoIP fields.

To use the twitter output - you will need to include your Twitter API keys and tokens. A great tutorial for setting up your own Twitter API can be found here: https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04
  
### Dependencies

tweepy, elasticsearch 