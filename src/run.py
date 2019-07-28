import time
import cursor
import os
from shutil import copyfile
import requests
import sys
import json

import xml_downloader
import dictionary_term_extractor
import xml_to_txt
import dictionary_indexer
import index_page_generator
import xml_to_html



def preamble():

    print('''

┌──────────────────────── \033[38;5;205m\033[1mChelsea Manning Trial Transcript Index Generator\033[0m ────────────────────────┐
│                                                                                                  │
│  The source code for this can be found at                                                        │
│                                                                                                  │
│    github.com/QueeriousLabs/ChelseaManningTrialTranscriptIndexGenerator                          │
│                                                                                                  │
│  The Internet Archive page for this project, including the browsable output of this project,     │
│  can be found at                                                                                 │
│                                                                                                  │
│    archive.org/details/chelsea_manning_transcript                                                │
│                                                                                                  │
│  Processing will begin shortly.                                                                  │
│                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
''')



class MissingPrerequisite(Exception):
    pass

def guard_prerequisites(working_dir):

    has_error = False

    print()
    print()
    print('Checking prerequisites...')
    print()


    # check internet connection
    time.sleep(0.25)
    try:
        requests.get('https://example.org/')
        print('  \033[38;5;155m\033[1mOK\033[0m Internet connection works.')

    except requests.exceptions.ConnectionError:
        has_error = True
        print('  \033[38;5;205m\033[1mERROR\033[0m No internet connection. Please connect to the internet and try again.')



    # check dictionaries
    time.sleep(0.25)
    if os.path.exists(working_dir + '/dictionaries/A Dictionary of Computer Science.epub'):
        print('  \033[38;5;155m\033[1mOK\033[0m Dictionary of Computer Science found.')
    else:
        has_error = True
        print('  \033[38;5;205m\033[1mERROR\033[0m Missing dictionary: "A Dictionary of Computer Science.epub"')

    time.sleep(0.25)
    if os.path.exists(working_dir + '/dictionaries/DOD Dictionary of Military and Associated Terms.txt'):
        print('  \033[38;5;155m\033[1mOK\033[0m DOD Dictionary of Military and Associated Terms found.')
    else:
        has_error = True
        print('  \033[38;5;205m\033[1mERROR\033[0m Missing dictionary: "DOD Dictionary of Military and Associated Terms.txt"')

    time.sleep(0.25)
    if os.path.exists(working_dir + '/dictionaries/Jargon File Glossary.html'):
        print('  \033[38;5;155m\033[1mOK\033[0m Jargon File Glossary found.')
    else:
        has_error = True
        print('  \033[38;5;205m\033[1mERROR\033[0m Missing dictionary: "Jargon File Glossary.html"')

    time.sleep(0.25)
    if os.path.exists(working_dir + '/dictionaries/NIST Infosec Dictionary.txt'):
        print('  \033[38;5;155m\033[1mOK\033[0m NIST Infosec Dictionary found.')
    else:
        has_error = True
        print('  \033[38;5;205m\033[1mERROR\033[0m Missing dictionary: "NIST Infosec Dictionary.txt"')


    if has_error:
        raise MissingPrerequisite()
    else:
        return True



def setup_output_dir(working_dir):
    output_dir = working_dir + '/output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


    if not os.path.exists(working_dir + '/output/usvmanning-index'):
        os.mkdir(working_dir + '/output/usvmanning-index')

    if not os.path.exists(working_dir + '/output/usvmanning-index'):
        os.mkdir(working_dir + '/output/usvmanning-index')

    for vol in range(1,112):
        if not os.path.exists(working_dir + '/output/usvmanning%i' % vol):
            os.mkdir(working_dir + '/output/usvmanning%i' % vol)


def run_scripts(working_dir, base_url):

    xml_downloader.main(working_dir)

    dictionary_term_extractor.main(working_dir)

    xml_to_txt.main(working_dir)

    dictionary_indexer.main(working_dir)

    setup_output_dir(working_dir)

    index_page_generator.main(working_dir, base_url)

    xml_to_html.main(working_dir, base_url)



def main():
    cursor.hide()

    try:

        preamble()

        time.sleep(0.5)

        working_dir = os.getcwd()

        print()
        print('This program will use the following directory as the working directory:')
        print()
        print('  ' + working_dir)

        guard_prerequisites(working_dir)

        time.sleep(0.5)
        print()
        cursor.show()
        base_url = input('Enter a base url for URLs, or leave blank to use the output directory:\n\n  ')
        cursor.hide()
        print()

        if '' == base_url: base_url = 'file://' + working_dir + '/output/'

        run_scripts(working_dir, base_url)

        time.sleep(0.5)

        print()
        print()
        print('\033[1mThe index has been generated.')
        time.sleep(0.5)
        print()
        print('Thank you for using this program.')
        time.sleep(0.5)
        print()
        print('\033[38;5;155mGood bye!\033[0m')
        time.sleep(1)

    except KeyboardInterrupt:
        print()
        print()
        print('Quitting via keyboard interrupt.')
        print()
        time.sleep(1)

    except MissingPrerequisite:
        print()
        print()
        print('Quitting due to failed prerequisites.')
        print()
        time.sleep(1)

    cursor.show()

main()
