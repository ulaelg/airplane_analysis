from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import nltk
import pandas as pd
import os

# Download NLTK data
nltk.download('stopwords', quiet=True)

# Create assets directory
os.makedirs("assets", exist_ok=True)

# Load your data
airplane_data_clean = pd.read_csv("Data/cleaned_airplane_crashes.csv")
text = " ".join(airplane_data_clean['Summary'].dropna().astype(str))

# Enhanced stopwords based on your frequency analysis
custom_stopwords = set(STOPWORDS).union(set(stopwords.words("english")))
custom_stopwords.update([
    "aircraft", "plane", "pilot", "flight", "crashed", "crash", "airplane",
    "airport", "landing", "takeoff", "feet", "altitude", "passengers",
    "crew", "runway", "air", "ground", "approach", "departure", 
    "minutes", "hours", "time", "reported", "taking", "conditions",
    # Add more based on your top words if they're not meaningful
    "engine", "weather", "mountain", "land", "failure"  # Remove these if you want them visible
])

# Generate word cloud - this should work after Pillow upgrade
wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="#0E1117",
    stopwords=custom_stopwords,
    colormap="Reds",
    max_words=100,
    relative_scaling=0.5,
    min_font_size=10,
    prefer_horizontal=0.7,
    collocations=False
).generate(text)

# Save the word cloud
output_path = "assets/wordcloud_summary.png"
wordcloud.to_file(output_path)
print(f"✓ Word cloud saved to: {output_path}")

# Display word frequencies
word_freq = wordcloud.words_
print("\nTop 15 words in your word cloud:")
for i, (word, freq) in enumerate(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10], 1):
    print(f"{i:2d}. {word}: {freq:.4f}")