import os
import re
import json
import xml.etree.ElementTree as ET
from jinja2 import Template

from term_for_urls import *
from indexer_cleaned_text import *
from print_progress_bar import print_progress_bar





def process_volume(working_dir, base_url, dictionary_index, vol_number):
  vol_number = str(vol_number)
  doc_root = ET.parse(working_dir + '/xml/usvmanning' + vol_number + '_djvu.xml').getroot()
  pages = []

  for node in doc_root.find('BODY'):
    if 'OBJECT' == node.tag:
      pages += [process_page(dictionary_index, node)]

  vol_path = os.path.join(working_dir, 'output', 'usvmanning%s' % vol_number)

  if not os.path.isdir(vol_path):
      os.makedirs(vol_path)

  for i, page in enumerate(pages):
    with open(os.path.join(vol_path, 'page_' + page['page_number'] + '.html'), 'w') as f:
      f.write(page_to_html(base_url, vol_number, page, i == 0, i+1 == len(pages)))



def process_page(dictionary_index, page_node):
  page_number = get_page_number(page_node)
  paragraphs = process_hiddentext(dictionary_index, [], page_node.find('HIDDENTEXT'))
  return { 'page_number': page_number, 'paragraphs': paragraphs }

def get_page_number(page_node):
  for params in page_node.findall('PARAM'):
    if params.attrib['name'] and params.attrib['name'] == 'PAGE':
      return re.match('.*_(\d+)\.djvu', params.attrib['value'])[1]
  raise Exception

def process_hiddentext(dictionary_index, last_five_words, hiddentext_node):
  return sum([ process_pagecolumn(dictionary_index, last_five_words, pc) for pc in hiddentext_node.findall('PAGECOLUMN') ], [])

def process_pagecolumn(dictionary_index, last_five_words, pagecolumn_node):
  return sum([ process_region(dictionary_index, last_five_words, r) for r in pagecolumn_node.findall('REGION') ], [])

def process_region(dictionary_index, last_five_words,region_node):
  return [ process_paragraph(dictionary_index, last_five_words, p) for p in region_node.findall('PARAGRAPH') ]

def process_paragraph(dictionary_index, last_five_words, paragraph_node):
  return { 'content': sum([ process_line(dictionary_index, last_five_words, l) for l in paragraph_node.findall('LINE') ], []) }

def process_line(dictionary_index, last_five_words, line_node):
  return [ process_word(dictionary_index, last_five_words, w) for w in line_node.findall('WORD') ]

def get_classes(dictionary_index, last_five_words):
  classes = []
  for i in range(0,5):
    term_to_find = indexer_cleaned_text(' '.join([ word_tuple[1] for word_tuple in last_five_words[i:] ]))
    if term_to_find in dictionary_index:
      classes += [[i,term_for_urls(term_to_find)]]
  return classes

def process_word(dictionary_index, last_five_words,word):
  word_tuple = [[], word.text]
  last_five_words += [word_tuple]
  while len(last_five_words) > 5:
    last_five_words.pop(0)
  classes = get_classes(dictionary_index, last_five_words)
  if classes:
    for class_info in classes:
      last_n = class_info[0]
      klass = class_info[1]
      for word_tuple_2 in last_five_words[last_n:]:
        word_tuple_2[0] += [klass]
  return word_tuple #'<span class="word">%s</span>' % word.text

def page_to_html(base_url, vol_number, page, is_first, is_last):

  pn = page['page_number']

  prev_page = None
  if not is_first:
      pn_prev = str(int(pn) - 1)
      pn_prev = (4 - len(pn_prev))*'0' + pn_prev
      prev_page = { 'url': page_number_to_url(vol_number, pn_prev), 'text': str(int(pn_prev)) }

  next_page = None
  if not is_last:
      pn_next = str(int(pn) + 1)
      pn_next = (4 - len(pn_next))*'0' + pn_next
      next_page = { 'url': page_number_to_url(vol_number, pn_next), 'text': str(int(pn_next)) }

  #print(prev_page)
    # variables: base_url,
    #            volume_url, volume_number, paragraphs
    #            prev_page_url, prev_page_link_text,
    #            current_page_text,
    #            next_page_url, next_page_link_text
  with open('src/volume_page_template.html', 'r') as f:
    volume_page_template = Template(f.read())

  return volume_page_template.render({
    'base_url': base_url,
    'volume_url': volume_number_to_url(vol_number),
    'volume_number': vol_number,
    'paragraphs': [ par['content'] for par in page['paragraphs'] ],
    'prev_page': prev_page,
    'current_page': str(int(pn)),
    'next_page': next_page
  })

def volume_number_to_url(vol_num):
  return 'https://archive.org/details/usvmanning' + str(int(vol_num))

def page_number_to_url(vol_number, page_number):
  return 'usvmanning%s/page_%s.html' % (vol_number, page_number)


def main(working_dir, base_url):
    print()
    print('\033[38;5;205m\033[1mConverting XML Transcript to HTML Transcript\033[0m')
    print()

    with open(working_dir + '/indexes/dictionary_index.json', 'r') as f:
      dictionary_index = json.loads(f.read())

    current = 0
    total = 111
    for i in range(1,112):
      print_progress_bar('  Processing volumes...', current, total)
      current += 1

      try:
          process_volume(working_dir, base_url, dictionary_index, i)
      except FileNotFoundError:
          pass

    print_progress_bar('  Processing volumes...', current, total)
    print()
