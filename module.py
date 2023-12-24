import requests
from config import constants
import pandas as pd

def get_popular_reddit_posts(api_key):
    querystring = {"time":"year"}# required parameter
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": constants.RAPID_API_HOST
    }
    response = requests.get(constants.BASE_URL + constants.POPULAR_POST_END_POINT, headers=headers, params=querystring)
    data_popular = response.json()
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

def get_post_whole_text(api_key, post_id):

    querystring = {"post_id":post_id}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": constants.RAPID_API_HOST
    }

    response = requests.get(constants.BASE_URL+ constants.POST_DETAILS_END_POINT, headers=headers, params=querystring)

    post_detail = response.json()
    post_text=post_detail['data']['media']['richtextContent']['document']
    post_string=""
    for line in post_text:
        try:
            post_string+=line['c'][0]['t']
        except KeyError:
            for nested_line in line['c'][0]['c']:
                try:
                    post_string+= nested_line['t']
                except KeyError:
                    post_string+=nested_line['c'][0]['t']
                    continue
            continue
    return post_string

def get_popular_reddit_posts_with_whole_text(api_key):
    popular_posts = get_popular_reddit_posts(api_key)
    post_texts = [get_post_whole_text(api_key=api_key, post_id=id) for id in popular_posts['id']]
    popular_posts['post_text'] =post_texts
    return popular_posts

   