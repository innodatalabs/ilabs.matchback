# ilabs.matchbak
[![Build Status](https://travis-ci.com/innodatalabs/ilabs.matchback.svg?branch=master)](https://travis-ci.com/innodatalabs/ilabs.matchback)
[![PyPI version](https://badge.fury.io/py/ilabs.matchback.svg)](https://badge.fury.io/py/ilabs.matchback)


A tool to match back XML elements of the Innodata's inno:dom XML to the source HTML elements.

## Installation

```
pip install ilabs.matchback
```

## Usage

```
matchback -h

usage: main.py [-h] [-v] [-r REQUIRED]
               input_html input_innodom output_html output_meta

match HTML and InnoDOM XML files. Version 0.1.3.

positional arguments:
  input_html            HTML input file
  input_innodom         InnoDOM XML input file
  output_html           Output HTML - copy of the input HTML with ids added
  output_meta           Output META in JSON format

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity level
  -r REQUIRED, --required REQUIRED
                        Required coverage threshold, default is 0.75
```

You need to provide two input files:
* Original HTML file
* Processed inno:dom XML file

Tool will generate two output files:
* Instrumented HTML - this is the input HTML file with added id attributes (where needed), to be referenced by meta datapoint via idref
* meta JSON file - the inno:meta section extracted from the inno:dom XML file, where "idref" atributes now point to the HTML. Additionally,
  each datapoint there receives an `xpath` attribute, pointing to the support element in the source HTML.

## Algorithm

1. Take source HTML, and build an index containing all words and their parent XML element
2. Do the same for the target inno:dom XML
3. Use `difflib` to compare source text with the target text. Pieces that match establish one-to-one mapping between
   source word and target word. From source and target indices we also know the XML elements that correspond
   to the matched words.
4. Given an element in the target inno:dom, we can find all words that are "covered" by this element, then
   we check how many of these words have match to the source. This is called "coverage" fraction.
   It is usually in the range of 0.85 and higher. If we can not match back at least 0.75 of the target words, we issue
   an error and algorithm fails (you can adjust the threshold with the `required` CLI option).
5. Once we have matched words, we follow them to the source and from source index we collect all XML elements that correspond
   to these chunks. Because of the inline tags like `<i>`, `<b>`, etc., we often end up with more than one element
   in the source tree that corresponds to the given element in the target tree.
6. Given a set of matched candidate elements in the source tree, we find a single common ancestor, and declare this to be a
   match for the element in the target inno:dom.
7. Steps 4-6 are repeated for every element in the inno:dom that needs to be matched back to the source HTML.

## Developing
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python -m ilabs.matchback.main -h
```

## Building
TravisCI is configured to automatically build this project.

To publish new version to the PyPI, just tag the master branch and push the tags out:
```
git tag 0.1.3
git push --tags
```
