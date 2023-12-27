import requests
from config import constants
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_api_call(api_key, api_host, querystring, url):
 
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def get_popular_reddit_posts(api_key):
    querystring = {"time":"year"}# required parameter
    data_popular = make_api_call(api_key, constants.RAPID_API_HOST, querystring, constants.BASE_URL+constants.POPULAR_POST_ENDPOINT)
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
    data_science_posts = make_api_call(api_key, constants.RAPID_API_HOST, querystring, constants.BASE_URL+constants.SUBREDDIT_POSTS_ENDPOINT)
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

def df_turn_datatype_to_numeric(df,column_names):
    for column_name in column_names:
        df[column_name] = pd.to_numeric(df[column_name])
    return df 

def plot_outliers(x, y, title, xlabel, ylabel, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tick_params(axis='both', which='both', labelbottom=False, bottom=False)
    x = x
    y = y
    plt.plot(x, y, "o", color=color)
        
    plt.show()

def plot_outliers_with_id(x, y, id, title, xlabel, ylabel, max_value, min_value, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tick_params(axis='both', which='both', labelbottom=False, bottom=False)
    for i in range(len(x)):
        try:
            x = x[i]
            y = y[i]
            plt.plot(x, y, "o", color=color)
            if y[i] > max_value or y[i]<min_value :
                plt.text(x, y * (1 - 0.05), id[i], fontsize=10)
        except:
            continue
    plt.show()

def plot_hist(df, title, xlabel, column_name, bin_num, kde, color='maroon'):
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    sns.histplot(data = df, x = column_name, bins = bin_num,  kde = kde, color = color )
    plt.show()

def plot_scatter(df, colmn_name_x, colmn_name_y, id, title, xlabel, ylabel, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.scatterplot(data=df,
                x=colmn_name_x,
                y=colmn_name_y,
                )
    plt.show()

def corr_heatmap(df, column_names):
    matrix = df[[column_names]].corr()
    sns.heatmap(matrix, 
            xticklabels=matrix.columns.values,
            yticklabels=matrix.columns.values)

