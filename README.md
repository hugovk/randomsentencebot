# randomsentencebot

Tweet a random line from a text file. Use this to make your own Twitter bots.

For example, 
**[![](https://abs.twimg.com/favicons/favicon.ico)Six-Worder Bot](https://twitter.com/sixworderbot)** is tweeting six-word stories picked at random from a text file of six-word sentences taken from the [Project Gutenberg August 2003 CD](http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project). Think along the lines of "For Sale, Baby Shoes, Never Worn" ([probably not by Ernest Hemingway](http://quoteinvestigator.com/2013/01/28/baby-shoes/)).

In [@sixworderbot](https://twitter.com/sixworderbot)'s case, the text file was generated using [gutengrep](https://github.com/hugovk/gutengrep) something like this:

```bash
gutengrep.py "^\W*([a-zA-ZåäöÅÄÖàéÉÈíšŠ]+['[a-zA-Z]+]?[- :;,.¿?\!]+){6}\W*$" --correct --cache > /tmp/1.txt

# Remove blanks and duplicates:
sort /tmp/1.txt | uniq > six-word-sentences.txt  # 
```
