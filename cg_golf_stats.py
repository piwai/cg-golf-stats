import csv
import collections
import sys

import requests

STATS_URL = "https://www.codingame.com/services/CodinGamer/getMyConsoleInformation"
OUTFILE = "codegolf.csv"

def get_top_values(scores_by_lang, limit=5):
    return dict(collections.Counter(scores_by_lang).most_common(limit))


def main(userid):
    headers = {'Content-Type': 'application/json'}
    stats = requests.post(STATS_URL, data=f"[{userid}]", headers=headers).json()
    
    rows = []
    grand_total = 0
    submitted_languages = set()
    for puzzle in stats['puzzles']:
        if puzzle.get('puzzleType') != 'GOLF':
            continue
        scores = {k:int(v) for (k,v) in puzzle['pointsByLanguage'].items() }
        top5 = get_top_values(scores)
        total = sum(top5.values())
        grand_total += total
        submitted_languages.update(top5.keys())
        rows.append({'Puzzle name': puzzle['labelTitle'].removesuffix('- Code Golf'), 'Total': total, '# Solutions': len(top5), **top5})

    with open(OUTFILE, 'w') as f:
        columns = ['Puzzle name', 'Total', '# Solutions'] + sorted(list(submitted_languages))
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
        writer.writerow({})
        writer.writerow({'Puzzle name': 'Grand total', 'Total': grand_total})


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('Usage: cg_golf_stats.py <userid>', file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])