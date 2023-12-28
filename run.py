from module import get_popular_reddit_posts, get_ds_reddit_posts, df_turn_datatype_to_numeric, find_outliers,plot_outliers, plot_outliers_with_id, plot_hist

from config import api_key

import pandas as pd

# Getting the data
#popular_posts_df = get_popular_reddit_posts(api_key=api_key.RAPID_API_KEY)
#ds_posts_df =get_ds_reddit_posts(api_key=api_key.RAPID_API_KEY)
popular_posts_df = pd.read_csv("popular_posts.csv")
ds_posts_df = pd.read_csv("data_science_posts.csv")

# Popular Reddit Posts Analyze and Viz
# Printing first five rows
print(f"Popular reddit posts:\n{popular_posts_df.head()}")

#Printing info for to get more information about data
print(popular_posts_df.info())

#Turning numerical data to numeric data type
df_turn_datatype_to_numeric(popular_posts_df, ['score','numComments', 'goldCount'])

#Detecting Outliers
# Plotting outliers
plot_outliers(popular_posts_df['id'], popular_posts_df['score'],'Popular Posts Score', xlabel='Posts', ylabel='Score')
plot_outliers_with_id(popular_posts_df,'id','score', 'id', 'Popular Posts Score', xlabel='Posts', ylabel='Score', min_value=5000, max_value=300000)

# Dropping outliers from the plot and reseting index after dropping
popular_posts_df = popular_posts_df.drop(popular_posts_df.query('score < 5000').index).reset_index(drop=True)

#Plotting popular posts score without outliers
plot_outliers(popular_posts_df['id'], popular_posts_df['score'],'Popular Posts Score Without Outliers', xlabel='Posts', ylabel='Score')

#Plotting histogram of comment numbers of popular posts
plot_hist(popular_posts_df,'Popular Posts Number of Comments', 'Number of Comments', 'numComments', 5, True )

# Plotting gold count outliers
plot_outliers_with_id(popular_posts_df,'id','goldCount', 'id', 'Popular Posts Gold Count', xlabel='Posts', ylabel='Gold Count', min_value=0, max_value=300)
#Printing the outlier row to find out the index
print(find_outliers(popular_posts_df, 'goldCount'))
# Dropping the outlier and reseting the index
popular_posts_df = popular_posts_df.drop(find_outliers(popular_posts_df, 'goldCount').index).reset_index(drop=True)

print(popular_posts_df.head())











#print(f"Data-science reddit posts with whole text:\n{ds_posts_df.head()}")



