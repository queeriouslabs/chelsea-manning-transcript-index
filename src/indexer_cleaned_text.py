import re

def indexer_cleaned_text(text):
  return re.sub('\\s+', ' ', re.sub('[^a-zA-Z0-9\\s]', '', text.strip().lower()))
