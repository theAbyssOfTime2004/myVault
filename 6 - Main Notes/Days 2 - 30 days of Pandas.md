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


# References
