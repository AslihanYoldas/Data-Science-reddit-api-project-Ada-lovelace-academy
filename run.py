from module import get_popular_reddit_posts_with_whole_text
from config import api_key


data=get_popular_reddit_posts_with_whole_text(api_key.RAPID_API_KEY)
print(data.head())
data.to_csv("popular_reddit_posts_with_whole_text.csv",index=False)
