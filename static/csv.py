import pandas as pd
from textblob import TextBlob

# Read the CSV file into a DataFrame

df = pd.read_csv('F://Data_Mining//sentimentaionm.csv')

# Assuming your CSV file has a 'text' column that contains the text data to analyze
# You can adjust the column name accordingly
text_column = 'text'

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(text):
    if isinstance(text, float):
        # Handle cases where 'text' is a float
        text = str(text)
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    print(sentiment)

# Apply sentiment analysis to the 'text' column and create a new 'sentiment' column
df['sentiment'] = df['text'].apply(analyze_sentiment)

# Print the DataFrame with sentiment analysis results
print(df)

