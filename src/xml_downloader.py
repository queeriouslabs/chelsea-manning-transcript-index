import cursor
import sys
import os
import getpass
import requests

from print_progress_bar import print_progress_bar

def main(working_dir):


    print()
    print('\033[38;5;205m\033[1mDownloading XML Transcript\033[0m')


    xml_dir = working_dir + '/xml'

    try:
      os.mkdir(xml_dir)
    except FileExistsError:
      pass

    djvu_url = 'https://archive.org/download/usvmanning%d/usvmanning%d_djvu.xml'
    dl_path = xml_dir + '/usvmanning%d_djvu.xml'

    def are_documents_private():
      r = requests.get(djvu_url % (1,1))
      return r.status_code == 403

    with requests.Session() as s:
        if are_documents_private():
            print()
            print('  Accessing these documents currently requires a login. Please enter archive.org credentials.')
            print()
            cursor.show()
            username = input('  Username: ')
            password = getpass.getpass('  Password: ')
            cursor.hide()
            s.cookies['test-cookie']="1"
            login_res = s.post("https://archive.org/account/login", data={
              "username": username,
              "password": password
            })

            if 200 != login_res.status_code:
                print()
                print("  \033[38;5;205m\033[1mERROR\033[0m Invalid credentials.")
                sys.exit(1)

        total = 111
        current = 0

        #print("Downloading documents")

        print()

        for n in range(1, 111+1):
            print_progress_bar('  Downloading XML volumes...', current, total)
            current += 1

            retry = True

            while retry:
                try:
                    with s.get(djvu_url % (n, n), stream=True) as r:
                        if 200 == r.status_code:
                            retry = False
                            with open(dl_path % n, "wb") as f:
                                for chunk in r.iter_content(chunk_size=4096):
                                    if chunk:
                                        f.write(chunk)
                except Exception: pass

        print_progress_bar('  Downloading XML volumes...', current, total)

        print()
