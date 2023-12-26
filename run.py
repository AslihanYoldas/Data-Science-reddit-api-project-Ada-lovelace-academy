from module import get_popular_reddit_posts, get_ds_reddit_posts
from config import api_key

popular_posts_df = get_popular_reddit_posts(api_key=api_key.RAPID_API_KEY)
ds_posts_df =get_ds_reddit_posts(api_key=api_key.RAPID_API_KEY)


print(f"Popular reddit posts:\n{popular_posts_df.head()}")
print(f"Data-science reddit posts with whole text:\n{ds_posts_df.head()}")

