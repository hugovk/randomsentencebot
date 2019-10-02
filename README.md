# randomsentencebot

[![Build Status](https://travis-ci.org/hugovk/randomsentencebot.svg?branch=master)](https://travis-ci.org/hugovk/randomsentencebot)
[![Python: 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg?logo=python&logoColor=FFE873)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)

Tweet a random line from a text file. Use this to make your own Twitter bots.

For example, 
**[![](https://abs.twimg.com/favicons/favicon.ico)Six-Worder Bot](https://twitter.com/sixworderbot)** is tweeting six-word stories picked at random from a text file of six-word sentences taken from the [Project Gutenberg August 2003 CD](http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project). Think along the lines of "For Sale, Baby Shoes, Never Worn" ([probably not by Ernest Hemingway](http://quoteinvestigator.com/2013/01/28/baby-shoes/)). See the [archive](https://hugovk.github.io/randomsentencebot/).

In [@sixworderbot](https://twitter.com/sixworderbot)'s case, the text file was generated using [gutengrep](https://github.com/hugovk/gutengrep) something like this:

```bash
gutengrep.py "^\W*([a-zA-ZåäöÅÄÖàéÉÈíšŠ]+['[a-zA-Z]+]?[- :;,.¿?\!]+){6}\W*$" --correct --cache > /tmp/1.txt

# Remove blanks and duplicates:
sort /tmp/1.txt | uniq > six-word-sentences.txt  # 
```
