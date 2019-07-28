# Chelsea Manning Trial Transcript Index Generator

This project generates an index for the [Chelsea Manning Trial Transcript](https://archive.org/details/chelsea_manning_transcript). The canonical version of the generated index can be found on the Internet Archive [here](https://archive.org/details/usvmanning-index).

## How to Use

1. Download this repository into a directory of your choice. We shall refer to this directory as `$DIR` for the rest of this explanation.
2. Create a directort `$DIR/dictionaries`, and put the following dictionaries into them:
    - Oxford Dictionary of Computer Science; ebook; 2016 ISBN 978-0-19-100288-5 (can be found in various places, both legally and illegally).
    - DOD Dictionary of Military and Associated Terms; pdf; May 2019; [https://www.jcs.mil/Portals/36/Documents/Doctrine/pubs/dictionary.pdf?ver=2019-05-29-162249-290](https://www.jcs.mil/Portals/36/Documents/Doctrine/pubs/dictionary.pdf?ver=2019-05-29-162249-290)
    - The Jargon File Glossary; webpage; [http://catb.org/jargon/html/go01.html](http://catb.org/jargon/html/go01.html)
    - NIST Glossary of Key Information Security Terms; pdf; May 2013; [https://csrc.nist.gov/publications/detail/nistir/7298/rev-2/final](https://csrc.nist.gov/publications/detail/nistir/7298/rev-2/final)
3. Convert the PDFs to TXTs in the same directory, using Adobe Acrobat Pro using the following methods. If you don't have Acrobat Pro, this process can't be recreated with any guarantee, sorry.
    - DOD Dictionary of Military and Associated Terms: Save as Accessible Text
    - NIST Glossary of Key Information Security Terms: Save as Plain Text (HTML/ASCII Encoding)
4. Connect to the internet.
5. From within `$DIR` the extractor script: `python3 src/run.py`. Follow the prompts. To recreate the content on archive.org, pick your base url to be `https://archive.org/download/`

The output of this whole process can be found in `$DIR/output`, and will have the following sort of structure:

```
output
├── usvmanning-index
│   ├── a_certificate.html
│   ├── a_life.html
│   ├── acceptability.html
│   ...
│   ├── term_list.html
│   ...
├── usvmanning1
│   ├── page_0000.html
│   ├── page_0001.html
│   ...
├── usvmanning10
├── usvmanning100
├── usvmanning101
...
```

The various directories named `usvmanningNNN` are the browsable HTML versions of the PDFs on archive.org, while `usvmanning-index` contains the generated index pages. The most important one being `term_list.html`, which contains the list of terms that are in the index, and links to the individual pages for those terms, which then link to the HTML versions of the PDFs.

## Contact

If you have any questions or need assistance with any of this, 
        <p>
          This index and the software for it was created by volunteers at
          <a href="https://queeriouslabs.com">Queerious Labs</a> in San Francisco.
          All inquiries about the project should be directed to Beka Valentine,
          who can be contacted via email at <a href="mailto:beka@queeriouslabs.com">beka@queeriouslabs.com</a>
          or via Twitter at <a href="https://twitter.com/beka_valentine">@beka_valentine</a>.
        </p>
