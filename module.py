import requests
from config import constants
import pandas as pd

def make_api_call(api_key, querystring, url):
 
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": constants.RAPID_API_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def get_popular_reddit_posts(api_key):
    querystring = {"time":"year"}# required parameter
    data_popular = make_api_call(api_key, querystring, constants.BASE_URL+constants.POPULAR_POST_ENDPOINT)
    popular_posts =[]
    for post in data_popular['data']['posts']:
        popular_post= {
            "id":post['id'],
            "title":post['title'],
            "numComments":post['numComments'],
            "score":post['score'],
            "author":post['author'],
            "authorId":post['authorId'],
            "goldCount":post['goldCount'],
            "domain":post['domain']}
        popular_posts.append(popular_post)

    popular_posts_df = pd.DataFrame(popular_posts)
    return popular_posts_df

def get_post_text(post_text):
    post_string=""
    if (len(post_text) == 0):
        return "None"
    for text in post_text: 
        try: 
           for line in text['c']:
               post_string+= line['t']
        except KeyError:
            try:
                for sentence in line['c']:
                    post_string += sentence['c'][0]['t']
            except:
                continue # for the 'e' key that we dont need   
    return post_string

def get_ds_reddit_posts(api_key):
    querystring = {"subreddit":"datascience","sort":"new"}
    data_science_posts = make_api_call(api_key, querystring, constants.BASE_URL+constants.SUBREDDIT_POSTS_ENDPOINT)
    ds_posts =[]
    for post in data_science_posts['data']['posts']:
        post_text = get_post_text(post['media']['richtextContent']['document'])
        ds_post= {
            "id":post['id'],
            "title":post['title'],
            "numComments":post['numComments'],
            "score":post['score'],
            "author":post['author'],
            "authorId":post['authorId'],
            "goldCount":post['goldCount'],
            "domain":post['domain'],
            "post_text":post_text
            }
        ds_posts.append(ds_post)

    ds_posts_df = pd.DataFrame(ds_posts)
    return ds_posts_df


   