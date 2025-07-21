2025-07-21 23:38


Tags: [[30 Days of Pandas - Leetcode]]

# Days 2 - 30 days of Pandas

### 1683. Invalid Tweets
```python
import pandas as pd

def invalid_tweets(tweets: pd.Dataframe)
-> pd.Dataframe
	return tweets[tweets["content"].str.len() > 15][["tweets_id"]]
```

- faster approach:
```python
df.loc[df["content"].str.len() > 15, "tweet_id"]
```
- It avoids creating a temporary full df like `[["tweets_id]]` 
- `df.loc[<conditions>, <columns>]`, in this case `df["contents"].str.len() > 15` is a boolean mask which will return `1` or `0` according to the condition, and willl return the corresponding `tweet_id`

# References
