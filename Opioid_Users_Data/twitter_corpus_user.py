#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import sys
import time


#Twitter API credentials
consumer_key = "5MOIEv04mahHH3iruYSBi6acU"
consumer_secret = "zrj11pHlZ5RkND8oX2b34voCmNFWHV3tj2eLXtmOASn6c3WcSj"
access_key = "2207078118-5DojdYuM0wvLmvO6YdTRrwsfe15KLnuqBLk2U0c"
access_secret = "0boDaUkIANRYmUIOISoNohbREykTg7Ad11vkn7pz0J357"


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)
    cnt = 1
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while cnt < 5:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
        cnt = cnt+1
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))
       
    #write tweet objects to JSON
    
    fname = screen_name.strip()+".txt"
    fname = fname[1:]
    
    file = open(fname, 'a')
    print "Writing tweet objects to JSON please wait..."
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True)
	file.write('\n')
    
    #close the file
    print "Done"
    file.close()

if __name__ == '__main__':
    #pass in the username of the account you want to download
    
    fin = open('screen_names.txt','r')
    all_lines = fin.readlines()
    n = 0
    
    fout = open('error_users.txt','a') 
          
    tot_len = len(all_lines)
    
    while n<tot_len:
      try:
          screen_name = '@'+all_lines[n]
          print screen_name
          print n
          get_all_tweets(screen_name)
          n = n+1
          if n==5000:
             break
      except tweepy.RateLimitError:
          print 'Rate Limit Exceeded. Retrying....'
          time.sleep(60*5)
      except tweepy.TweepError as err:
          n = n+1
          print 'Error code:'+str(err.api_code)
          fout.write(screen_name)
      except:
          n = n+1 
          fout.write(screen_name)
    
    fout.close()
