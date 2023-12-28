import requests
from config import constants
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nlp_rake
from wordcloud import WordCloud


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

def find_outliers(df,column_name):
    threshold = 3
    outliers = []
    for index, data in enumerate(df[column_name]):
        z_score = (data - df[column_name].mean()) / df[column_name].std()
        if abs(z_score) > threshold:
            outliers.append(index)
    return df.iloc[outliers]

def plot_outliers(x, y, title, xlabel, ylabel, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tick_params(axis='both', which='both', labelbottom=False, bottom=False)
    x = x
    y = y
    plt.plot(x, y, "o", color=color)
        
    plt.show()

def plot_outliers_with_id(df, column_name_x,column_name_y, column_name_id, title, xlabel, ylabel, max_value, min_value, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tick_params(axis='both', which='both', labelbottom=False, bottom=False)
    for i in range(len(df)):
        try:
            x = df[column_name_x][i]
            y = df[column_name_y][i]
            plt.plot(x, y, "o", color=color)
            if y > max_value or y < min_value :
                plt.text(x, y * (1 - 0.05), df[column_name_id][i], fontsize=10)
        except:
            continue
    plt.show()

def plot_hist(df, title, xlabel, column_name, bin_num, kde, color='maroon'):
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    sns.histplot(data = df, x = column_name, bins = bin_num,  kde = kde, color = color )
    plt.show()

def plot_scatter(df, colmn_name_x, colmn_name_y, title, xlabel, ylabel, color='indigo'):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.scatterplot(data=df,
                x=colmn_name_x,
                y=colmn_name_y,
                )
    plt.show()

def corr_heatmap(df, column_names):
    matrix = df[column_names].corr()
    sns.heatmap(matrix, 
            xticklabels=matrix.columns.values,
            yticklabels=matrix.columns.values,
            vmin=-1)
    plt.show()

def extract_words(text):
    extractor = nlp_rake.Rake(max_words=3,min_freq=3,min_chars=4)
    res = extractor.apply(text)
    return res

def plot_frequent_words(text,title):
    res = extract_words(text)
    pair_list = res[:20]
    k,v = zip(*pair_list)
    plt.title(title)
    plt.bar(range(len(k)),v)
    plt.xticks(range(len(k)),k,rotation='vertical')
    plt.show()

def plot_word_cloud_generate_from_freq(text,title):
    res = extract_words(text)
    wc = WordCloud(background_color='white',width=800,height=600)
    plt.imshow(wc.generate_from_frequencies({ k:v for k,v in res[:20] }))
    plt.title(title)
    plt.show()

def plot_word_cloud_generate_from_text(text,title):
    wc = WordCloud(background_color='white',width=800,height=600)
    plt.imshow(wc.generate(text))
    plt.title(title)
    plt.show()
    