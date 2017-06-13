@echo off
python WikiExtractor.py zhwiki-latest-pages-articles.xml.bz2 --output output -b 1000M --links --sections
pause