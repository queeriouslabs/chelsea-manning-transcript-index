import math
import os
import re
import json
from jinja2 import Template

from print_progress_bar import print_progress_bar
from term_for_urls import *

def loc_to_url(vol, loc, term):
  return 'usvmanning%s/page_%s.html?highlight=%s'%(vol, page_for_url(loc), term_for_urls(term))

def page_for_url(page):
  return (4 - len(str(page)))*'0' + str(page)

def url_for_term(term):
  return 'usvmanning-index/%s.html' % term_for_urls(term)





def main(working_dir, base_url):

    print()
    print('\033[38;5;205m\033[1mBuilding Index Pages\033[0m')

    # load index

    index = {}
    with open(working_dir + '/indexes/dictionary_index.json', 'r') as f:
        index = json.loads(f.read())




    # load terms with case

    term_expansions = {}

    with open(working_dir + '/dictionaries/combined_terms_with_case.txt', 'r') as f:
      lines = f.readlines()

    current = 0
    total = len(lines)
    for line in lines:
      print_progress_bar('  Loading terms with case...', current, total)
      current += 1
      term = line.strip()
      if term not in term_expansions:
        term_expansions[indexer_cleaned_text(term)] = term
      else:
        term_expansions[indexer_cleaned_text(term)] += ' / ' + term

    print_progress_bar('  Loading terms with case...', current, total)
    print()







    # Generate Term List

    alphabetical_index = {}

    current = 0
    total = len(index)

    for term in index:
      print_progress_bar('  Generating term list...', current, total)
      current += 1

      c = term[0]
      if c not in alphabetical_index:
        alphabetical_index[c] = []
      alphabetical_index[c] += [{
        'url': url_for_term(term),
        'link_text': term_expansions[indexer_cleaned_text(term)]
      }]

    for term, entries in alphabetical_index.items():
      if len(entries) <= 10:
          alphabetical_index[term] = [entries]
      elif len(entries) <= 20:
          alphabetical_index[term] = [entries[0:10], entries[10:]]
      elif len(entries) <= 30:
          alphabetical_index[term] = [entries[0:10], entries[10:20], entries[20:]]
      else:
          col_height = math.ceil(len(entries) / 4)
          alphabetical_index[term] = [entries[0:col_height],
                                      entries[col_height:2*col_height],
                                      entries[2*col_height:3*col_height],
                                      entries[3*col_height:]]

    with open(working_dir + '/src/index_page_template.html', 'r') as index_template_file, \
         open(working_dir + '/output/usvmanning-index/term_list.html', 'w') as index_page_file:

      index_page_file.write(Template(index_template_file.read()).render({
          'base_url': base_url,
          'alphabetical_index': alphabetical_index
      }))

    print_progress_bar('  Generating term list...', current, total)
    print()












    # Generate Term Pages

    #print('Generating term pages...')

    with open(working_dir + '/src/term_page_template.html', 'r') as f:
        term_template = Template(f.read())

    current = 0
    total = len(index)

    for term, info in index.items():
      current += 1
      print_progress_bar('  Generating term pages...', current, total)

      term_index_html = term_template.render({
        'term': term,
        'base_url': base_url,
        'info': sorted([ (vol, [{ 'url': loc_to_url(vol, loc, term), 'link_text': loc }
                                 for loc in sorted(locs, key = lambda loc: int(loc)) ]) for vol, locs in info.items() ],\
                       key = lambda vol_loc: int(vol_loc[0]))
      })

      with open(working_dir + '/output/usvmanning-index/%s.html' % term_for_urls(term), 'w') as f:
        f.write(term_index_html)

    print_progress_bar('  Generating term pages...', current, total)
    print()
