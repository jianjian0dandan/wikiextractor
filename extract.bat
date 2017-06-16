@echo off
python WikiExtractorV2.py zhwiki-latest-pages-articles.xml.bz2 --output output -b 1M --links --sections --lists --json
pause