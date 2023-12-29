import requests
from config import constants
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nlp_rake
from wordcloud import WordCloud

def make_api_call(api_key, api_host, querystring, url):
    """
    Make a API call to Rapid Api with given api key and api host. Returns the API response.

    :param api_key: str -unique key given from rapid api for authorization
    :param api_host: str -api service url that provides data (for reddit api:reddit34.p.rapidapi.com)
    :querystring : dict -required or optional parameters that API wants for the data
    :url: str -url adress for the api call with the endpoint 
    :return:dict -API response
    
    """ 
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def get_popular_reddit_posts(api_key):
    """
    Make a API call to Reddit Api Popular Posts endpoint via Rapid Api with given api key. 
    Returns the popular posts as a dataframe

    :param api_key: str -unique key given from rapid api for authorization
  
    :return popular_posts_df:dataframe -Returns some data from popular posts as a dataframe
    
    """ 
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
    """
    Turns structured post text data to a string.

    :param post_text: dict -structured post text data in the API response
  
    :return post_string:string -Returns the post text data as string
    
    """ 
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
    """
    Make a API call to Reddit Api Subreddit Posts endpoint via Rapid Api with given api key. 
    Returns the that subreddit's posts as a dataframe

    :param api_key: str -unique key given from rapid api for authorization
  
    :return ds_posts_df:dataframe -Returns the that subreddit's posts as a dataframe
    
    """ 
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
    """
    In a dataframe turns the given columns' data types to numeric.

    :param df: dataframe 
    :param column_names: list- column names 
  
    :return df:dataframe -Returns the dataframe after changing data types to numerical for given column names
    """
    for column_name in column_names:
        df[column_name] = pd.to_numeric(df[column_name])
    return df 

def find_outliers(df,column_name):
    """
    Find outliers for given dataframe's column via z-score

    :param df: dataframe 
    :param column_name: list  
  
    :return :dataframe -Returns the outliers data as dataframe
    
    """ 
    
    threshold = 3
    outliers = []
    for index, data in enumerate(df[column_name]):
        z_score = (data - df[column_name].mean()) / df[column_name].std()
        if abs(z_score) > threshold:
            outliers.append(index)
    return df.iloc[outliers]

def plot_outliers(x, y, title, xlabel, ylabel, color='indigo'):
    """
    Plot x and y data as a point. That way we can detect outliers.

    :param x: series - x axis data
    :param y: series - y axis data
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param ylabel: str - Label of the y-axis
    :param color: str - Color of the plot

    :return : shows the plot
    
    """ 
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tick_params(axis='both', which='both', labelbottom=False, bottom=False)
    x = x
    y = y
    plt.plot(x, y, "o", color=color)
        
    plt.show()

def plot_outliers_with_id(df, column_name_x,column_name_y, column_name_id, title, xlabel, ylabel, max_value, min_value, color='indigo'):
    """
    Plots dataframe's columns as a point. For given min and max values detect outliers and show the id of that outliers.

    :param df: dataframe
    :param column_name_x: str - x axis data's column name
    :param column_name_y: str - y axis data's column name
    :param column_name_id: str - id data column name
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param ylabel: str - Label of the y-axis
    :param max_value: int - max value for the data
    :param min_value: int - min value for the data
    :param color: str - Color of the plot

    :return : shows the plot"""
    
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
    """
    Plots histogram for the given dataframe's column.

    :param df: dataframe
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param column_name: str - x axis data's column name
    :param bin-num: int - Number of the bins
    :param kde: bool - Drawing the line 

    :return : shows the plot"""
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    sns.histplot(data = df, x = column_name, bins = bin_num,  kde = kde, color = color )
    plt.show()

def plot_scatter(df, colmn_name_x, colmn_name_y, title, xlabel, ylabel):
    """
    Scatter plot for the given dataframe's columns.

    :param df: dataframe
    :param column_name_x: str - x axis data's column name
    :param column_name_y: str - y axis data's column name
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param ylabel: str - Label of the y-axis

    :return : shows the plot
    """
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.scatterplot(data=df,
                x=colmn_name_x,
                y=colmn_name_y,
                )
    plt.show()

def corr_heatmap(df, column_names):
    """
    Calculates correllation between given dataframe's columns and shows it as a heatmap

    :param df: dataframe 
    :param column_names: list -column names 
  
    :return :shows the plot
    """
    
    matrix = df[column_names].corr()
    sns.heatmap(matrix, 
            xticklabels=matrix.columns.values,
            yticklabels=matrix.columns.values,
            vmin=-1)
    plt.show()

def extract_words(text):
    """
    Extracts most frequent words from the text

    :param text: str
    :return res : list - most frequent words and their frequency as tuples
    """

    extractor = nlp_rake.Rake(max_words=3,min_freq=3,min_chars=4)
    res = extractor.apply(text)
    return res

def plot_frequent_words(text,title):
    """
    Extracts most frequent words from the text and show in a plot.

    :param text: string
    :param title: str - Title of the plot

    :return : shows plot
    """
    res = extract_words(text)
    pair_list = res[:20]
    k,v = zip(*pair_list)
    plt.title(title)
    plt.bar(range(len(k)),v)
    plt.xticks(range(len(k)),k,rotation='vertical')
    plt.show()

def plot_word_cloud_generate_from_freq(text,title):
    """
    Extracts most frequent words from the text and generate word cloud from frequent words.

    :param text: str
    :param title: str - Title of the plot

    :return : shows word cloud
    """
    res = extract_words(text)
    wc = WordCloud(background_color='white',width=800,height=600)
    plt.imshow(wc.generate_from_frequencies({ k:v for k,v in res[:20] }))
    plt.title(title)
    plt.show()

def plot_word_cloud_generate_from_text(text,title):
    """
    Generate word cloud from a text and show it.

    :param text: str
    :param title: str - Title of the plot

    :return : shows word cloud
    """
    wc = WordCloud(background_color='white',width=800,height=600)
    plt.imshow(wc.generate(text))
    plt.title(title)
    plt.show()
    