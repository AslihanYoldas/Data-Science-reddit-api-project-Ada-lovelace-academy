from module import * 
import string
from config import api_key

# Getting the data
popular_posts_df = get_popular_reddit_posts(api_key=api_key.RAPID_API_KEY)
ds_posts_df =get_ds_reddit_posts(api_key=api_key.RAPID_API_KEY)

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
print(popular_posts_df)
# Plotting gold count without outlier
plot_outliers_with_id(popular_posts_df,'id','goldCount', 'id', 'Popular Posts Gold Count Without Outlier', xlabel='Posts', ylabel='Gold Count', min_value=0, max_value=300)

# Plotting  number of comment and score as a scatter plot see their relationship
plot_scatter(popular_posts_df,
            'numComments',
            'score', 
            'Popular Posts Number of Comments and Score',
            'numComments' ,
            'score')

# Calculating correlation and showing with heatmap
corr_heatmap(popular_posts_df,['score', 'numComments', 'goldCount'])
#Getting basic statistics values of the data without the outliers
print(popular_posts_df.describe())

## Data science Posts

# Printing first five rows
print(f"Data-science reddit posts with whole text:\n{ds_posts_df.head()}")

#Printing info for to get more information about data
print(ds_posts_df.info())

#Filling null post text with their titles
ds_posts_df['post_text'] = ds_posts_df.post_text.fillna(ds_posts_df.title)

# Detecting Outliiers

# Plotting outliers
plot_outliers(ds_posts_df['id'], ds_posts_df['score'],'Data Science Posts Score', xlabel='Posts', ylabel='Score')

#Finding and dropping outlier
ds_posts_df = ds_posts_df.drop(find_outliers(ds_posts_df, 'score').index).reset_index(drop=True)

# Plotting post scores without outliers
plot_outliers(ds_posts_df['id'], ds_posts_df['score'],'Data Science Posts Score Without Outlier', xlabel='Posts', ylabel='Score')

#Plotting histogram of comment numbers of popular posts
plot_hist(ds_posts_df,'Data Science Posts Number of Comments', 'Number of Comments', 'numComments', 3, True )

# Ploting score and number of comments
plot_scatter(ds_posts_df,
            'numComments',
            'score', 
            'Data Science Posts Number of Comments and Score',
            'numComments' ,
            'score')

# Calculating correlation and showing with heatmap
corr_heatmap(ds_posts_df,['score', 'numComments'])

#Getting basic statistics values of the data without the outliers
print(ds_posts_df.describe())

#Data Science Post Text Analyzing

# Post texts and titles turn into lis
ds_post_text_list =ds_posts_df['post_text'].to_list()
ds_post_title_list=ds_posts_df['title'].to_list()

# We  filled none text value with title because of that we are removing the titles in the post text
for i in range (len(ds_post_text_list)):
    if (ds_post_text_list[i] == ds_post_title_list[i]):
        ds_post_text_list[i] = ""

# Joining list to get a string
data_science_posts_titles  = " ".join(ds_post_title_list)
data_science_posts_text = " ".join(ds_post_text_list)

# Cleaning punctuation
exclude = set(string.punctuation)
data_science_posts_text = ''.join(ch for ch in data_science_posts_text if ch not in exclude)
data_science_posts_titles = ''.join(ch for ch in data_science_posts_titles if ch not in exclude)

# Plotting frequent words in the post texts
plot_frequent_words(data_science_posts_text, 'Post text word frequencies')

# Showing frequent words in the word cloud
plot_word_cloud_generate_from_freq(data_science_posts_text, 'Data Science Post Texts  Word Cloud Generated From Frequinces')

# Generating word cloud with post texts
plot_word_cloud_generate_from_text(data_science_posts_text , 'Data Science Post Texts  Word Cloud Generated From Text')

# Getting titles and post texts in a str
ds_texts = data_science_posts_titles+  data_science_posts_text 

# Getting frequent words in post texts and titles
plot_frequent_words(ds_texts, 'Post text and titles word frequencies')

# Showing frequent words in the word cloud
plot_word_cloud_generate_from_freq(ds_texts, 'Data Science Post Texts and Titles Word Cloud Generated From Frequinces')

# Generating word cloud with post texts and post titles
plot_word_cloud_generate_from_text(ds_texts, 'Data Science Post Texts and Titles Word Cloud Generated From Text')
