import re
from indexer_cleaned_text import *

def term_for_urls(term):
  return re.sub('\\s+', '_',  indexer_cleaned_text(term))
