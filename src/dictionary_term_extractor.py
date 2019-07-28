import re
from ebooklib import epub
import ebooklib
from requests_html import HTML
from lxml import html

from indexer_cleaned_text import *
from print_progress_bar import print_progress_bar





def extract_jargon_file(working_dir):
    dictionary_filename = working_dir + '/dictionaries/Jargon File Glossary.html'
    with open(dictionary_filename, 'r') as f:
        content = f.read()

    dom = HTML(html = content)

    terms = []
    dds = dom.find('dd')

    current = 0
    total = len(dds)

    for el in dds:
        print_progress_bar('  Extracting Jargon File...', current, total)
        current += 1

        dd = el.lxml[0]
        dl = dd[0]
        for dt in dl:
            a = dt[0]
            terms += [a.text.strip()]

    jargon_file_terms_filename = working_dir + '/dictionaries/jargon_file_terms.txt'
    with open(jargon_file_terms_filename, 'w') as f:
        f.write('\n'.join(terms))
    #  f.write('\n'.join([ el.text_content().strip() for el in toc_tree.find_class('toc2') ]))

    print_progress_bar('  Extracting Jargon File...', current, total)
    print()



def extract_dod(working_dir):
    # this is the output of Acrobat -> Save as Accessible Text

    dictionary_filename = working_dir + '/dictionaries/DOD Dictionary of Military and Associated Terms.txt'

    with open(dictionary_filename, 'r', encoding='mac_roman') as f:
      lines = f.readlines()

    current = 0
    total = len(lines)

    separator = '—'
    terms = []
    parens_pattern = re.compile('^([^()]+)\(([^()]+)\)')
    for line in lines:
      print_progress_bar('  Extracting DOD dictionary...', current, total)
      current += 1

      loc = line.find(separator)
      if -1 != loc:
        term = line[:loc].strip().replace('&rsquo;','\'')
        m = parens_pattern.match(term)
        if m:
          terms += [m[1].strip(), m[2].strip()]
        else:
          terms += [term]

    dod_terms_filename = working_dir + '/dictionaries/dod_terms.txt'
    with open(dod_terms_filename, 'w') as f:
      f.write('\n'.join(terms))

    print_progress_bar('  Extracting DOD dictionary...', current, total)
    print()



def extract_nist(working_dir):
    # this is the output of Acrobat -> Save as Plain Text (HTML/ASCII Encoding)

    dictionary_filename = working_dir + '/dictionaries/NIST Infosec Dictionary.txt'

    with open(dictionary_filename, 'r') as f:
      lines = f.readlines()

    current = 0
    total = len(lines)

    separator = '&ndash;'
    terms = []
    parens_pattern = re.compile('^([^()]+)\(([^()]+)\)')
    for line in lines:
      print_progress_bar('  Extracing NIST dictionary...', current, total)
      current += 1

      loc = line.find(separator)
      if -1 != loc:
        term = line[:loc].strip().replace('&rsquo;','\'')
        if len(term) > 100: continue
        m = parens_pattern.match(term)
        if m:
          terms += [m[1].strip(), m[2].strip()]
        else:
          terms += [term]

    nist_terms_filename = working_dir + '/dictionaries/nist_terms.txt'

    terms_end_index = 1684
    with open(nist_terms_filename, 'w') as f:
      f.write('\n'.join(terms[:terms_end_index]))

    print_progress_bar('  Extracing NIST dictionary...', current, total)
    print()



def extract_docs(working_dir):
    input_path = working_dir + '/dictionaries/A Dictionary of Computer Science.epub'
    book = epub.read_epub(input_path)
    toc_content = None

    for doc in book.get_items():
      if 'Text/part0001.xhtml' == doc.get_name():
        toc_content = doc.get_content()
        break

    toc_tree = html.fromstring(toc_content)

    terms = []
    toc2s = toc_tree.find_class('toc2')

    current = 0
    total = len(toc2s)

    for el in toc2s:
        print_progress_bar('  Extracing Oxford CS dictionary...', current, total)
        current += 1
        terms += el.text_content().strip()

    docs_terms_filename = working_dir + '/dictionaries/docs_terms.txt'
    with open(docs_terms_filename, 'w') as f:
      f.write('\n'.join(terms))

    print_progress_bar('  Extracing Oxford CS dictionary...', current, total)
    print()



def combine_terms(working_dir):
    with open(working_dir + '/dictionaries/jargon_file_terms.txt', 'r') as f:
      jargon_file_terms = re.split('\n+',f.read())

    with open(working_dir + '/dictionaries/dod_terms.txt', 'r') as f:
      dod_terms = re.split('\n+',f.read())

    with open(working_dir + '/dictionaries/nist_terms.txt', 'r') as f:
      nist_terms = re.split('\n+',f.read())

    with open(working_dir + '/dictionaries/docs_terms.txt', 'r') as f:
      docs_terms = re.split('\n+',f.read())




    current = 0
    total = 7

    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms = jargon_file_terms + dod_terms + nist_terms + docs_terms
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms_with_case = [ term for term in list(set(combined_terms)) if term.strip() ]
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms = [ indexer_cleaned_text(tm) for tm in combined_terms if ',' not in tm ]
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms = list(set(combined_terms))
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms = [ tm.strip() for tm in combined_terms
                       if not re.match('^(\d+|.|\s+)$', tm) and not tm == '' ]
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1

    combined_terms.sort()
    print_progress_bar('  Combining dictionaries...', current, total)
    current += 1



    with open(working_dir + '/dictionaries/combined_terms_with_case.txt', 'w') as f:
      f.write('\n'.join(combined_terms_with_case))

    with open(working_dir + '/dictionaries/combined_terms.txt', 'w') as f:
      f.write('\n'.join(combined_terms))

    print_progress_bar('  Combining dictionaries...', current, total)
    print()



def main(working_dir):

    print()
    print('\033[38;5;205m\033[1mExtracting Terms from Dictionaries\033[0m')

    extract_jargon_file(working_dir)

    extract_dod(working_dir)

    extract_nist(working_dir)

    extract_docs(working_dir)

    combine_terms(working_dir)
