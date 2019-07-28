import os
import re
import json

from indexer_cleaned_text import *
from print_progress_bar import print_progress_bar

def build_volumes(vol):

  pages = []
  file_names = sorted([ file_name for file_name in os.listdir(os.path.join('txt', vol))
                                  if re.match('^\d+\.txt$', file_name) ])

  for file_name in file_names:
    with open(os.path.join('txt', vol, file_name), 'r', encoding='mac_roman') as f:
      pages += [(int(file_name[:-4]), re.split('\\s+',indexer_cleaned_text(f.read())))]

  return pages





def main(working_dir):

    print()

    print('\033[38;5;205m\033[1mBuilding Index\033[0m')





    current = 0
    total = 111

    volumes = []
    for vol in range(1,112):
      print_progress_bar('  Building volumes...', current, total)
      current += 1
      try:
          volumes += [(vol, build_volumes(str(vol)))]
      except FileNotFoundError:
          pass

    print_progress_bar('  Building volumes...', current, total)
    print()




    with open(working_dir + '/dictionaries/combined_terms.txt', 'r') as f:
      terms = [ line.strip() for line in f.readlines() ]

    terms_map = {}
    MAX_TERM_LENGTH = 0
    for term in terms:
      MAX_TERM_LENGTH = max(MAX_TERM_LENGTH, len(re.split('\\s+',term)))
      terms_map[term] = []

    index = {}
    rows = []



    current = 0
    total = len(volumes)

    for volume, pages in volumes:
      print_progress_bar('  Indexing volumes...', current, total)
      current += 1

      volume = int(volume)
      for page_num, page_words in pages:
        for i in range(0, len(page_words)):
          for n in range(1,MAX_TERM_LENGTH+1):
            ngram = ' '.join(page_words[i:i+n])
            if ngram in terms_map:
              if ngram not in index: index[ngram] = {}
              if volume not in index[ngram]: index[ngram][volume] = []
              if page_num not in index[ngram][volume]:
                index[ngram][volume] += [page_num]
                rows += [(ngram, str(volume), str(page_num))]

    indexes_dir = working_dir + '/indexes'
    if not os.path.exists(indexes_dir):
        os.mkdir(indexes_dir)

    with open(indexes_dir + '/dictionary_index.json', 'w') as f:
      f.write(json.dumps(index, sort_keys = True, indent = 4))

    print_progress_bar('  Indexing volumes...', current, total)
    print()
