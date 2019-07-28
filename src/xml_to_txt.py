import os
import re
import xml.etree.ElementTree as ET
from print_progress_bar import print_progress_bar

def process_volume(working_dir, vol_number):
  vol_number = str(vol_number)
  doc_root = ET.parse(working_dir + '/xml/usvmanning' + vol_number + '_djvu.xml').getroot()
  pages = []

  for node in doc_root.find('BODY'):
    if 'OBJECT' == node.tag:
      pages += [process_page(node)]

  vol_path = os.path.join(working_dir, 'txt', vol_number)
  vol_pages = []

  if not os.path.isdir(vol_path): os.makedirs(vol_path)
  for page in pages:
    page_text = page_to_text(page)
    with open(os.path.join(vol_path, page['page_number'] + '.txt'), 'w') as f:
      f.write(page_text)
    vol_pages += [page_text]

  with open(os.path.join(vol_path, 'all.txt'), 'w') as f:
    f.write(' '.join(vol_pages))

def process_page(page_node):
  page_number = get_page_number(page_node)
  paragraphs = process_hiddentext(page_node.find('HIDDENTEXT'))
  return { 'page_number': page_number, 'paragraphs': paragraphs }

def get_page_number(page_node):
  for params in page_node.findall('PARAM'):
    if params.attrib['name'] and params.attrib['name'] == 'PAGE':
      return re.match('.*_(\d+)\.djvu', params.attrib['value'])[1]
  raise Exception

def process_hiddentext(hiddentext_node):
  return sum([ process_pagecolumn(pc) for pc in hiddentext_node.findall('PAGECOLUMN') ], [])

def process_pagecolumn(pagecolumn_node):
  return sum([ process_region(r) for r in pagecolumn_node.findall('REGION') ], [])

def process_region(region_node):
  return [ process_paragraph(p) for p in region_node.findall('PARAGRAPH') ]

def process_paragraph(paragraph_node):
  return { 'content': ' '.join([ process_line(l) for l in paragraph_node.findall('LINE') ]) }

def process_line(line_node):
  return ' '.join([ w.text for w in line_node.findall('WORD') ])

def page_to_text(page):
  return ' '.join([ par['content'] for par in page['paragraphs'] ])





def main(working_dir):

    print()
    print('\033[38;5;205m\033[1mConverting XML Transcript to TXT Transcript\033[0m')

    current = 0
    total = 111

    for i in range(1,112):
      print_progress_bar('  Processing volumes...', current, total)
      current += 1

      try:
          process_volume(working_dir, i)
      except FileNotFoundError:
          pass

    print_progress_bar('  Processing volumes...', current, total)
    print()
