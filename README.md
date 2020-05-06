# ilabs.matchbak

A tool to match back XML elements of the Innodata's inno:dom XML to the source HTML elements.

## Installation

```
pip install ilabs.matchback
```

## Usage

```
matchback -h

usage: matchback [-h] [-v] [-r REQUIRED] input_html input_innodom output_html output_meta

match HTML and InnoDOM XML files, then translate idref from InnoDOM back to the source HTML, and writes HTML and META

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
* meta JSON file - the inno:meta section extracted from the inno:dom XML file, where "idref" atributes now point to the HTML

## Developing
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python -m ilabs.matchback.main -h
```

## Algorithm

1. Take source HTML, and build an index containing all text chunks and their parent XML element
2. Do the same for the target inno:dom XML
3. Use `difflib` to compare source text with teh target text. Pieces that match establish one-to-one mapping between
   source text chunk and target text chunk. From source and target inices we also know the XML elements that correspond
   to the matched chunks.
4. Given an element in the target inno:dom, we can find all text chunks that are "covered" by this element, then
   we check how many of these chunks have match to the source text chunks. This is called "coverage" fraction.
   It is usually in the range of 0.85 and higher. If we can not match at least 0.75 of the target text chunks, we issue
   an error and algorithm fails.
5. Once we have all matched text chunks, we follow them to the source index and collect all XML elements that correspond
   to these chunks. Because of the inline tags like `<i>`, `<b>`, etc., we often end up with more than one element
   in the source tree that corresponds to the given element in the target tree.
6. Given a set of matched candidate elements in the source tree, we find a single common ancestor, and declare this to be a
   match for the element in the target inno:dom.

What is chink? Python built-in `difflib` operates on a lists of objects. Experience shows that if we give it a list of
characters (one object === one character), algorithm runs very slow (its O(N^2) in the length of the list. Therefore, it makes
sence to use more coarse text pieces.