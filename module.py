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