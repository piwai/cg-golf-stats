# cg-golf-stats
A tool to get a csv extract of codegolf contests on codingame.com platform


# How to use

First, you'll need to get your codingame user id. Then:


```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python cg_golf_stats.py <your_codingame_userid>
```

This will produce a codegolf.csv file with your code golf stats per puzzle, which you can then import to Excel/Libreoffice for easier analysis.
