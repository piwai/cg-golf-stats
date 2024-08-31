import csv
import collections
import sys

import requests

STATS_URL = "https://www.codingame.com/services/CodinGamer/getMyConsoleInformation"
OUTFILE = "codegolf.csv"
SCORE_MAX = 200

def get_highest_values(scores_by_lang, limit=5):
    return dict(collections.Counter(scores_by_lang).most_common(limit))


def main(args):
    userid = args[1]
    only_top1 = True if "--only-top1" in args else False
    headers = {'Content-Type': 'application/json'}
    stats = requests.post(STATS_URL, data=f"[{userid}]", headers=headers).json()
    
    rows = []
    grand_total = 0
    submitted_languages = set()
    for puzzle in stats['puzzles']:
        if puzzle.get('puzzleType') != 'GOLF':
            continue
        scores = {k:int(v) for (k,v) in puzzle['pointsByLanguage'].items()}
        if only_top1:
            top1 = {k:k for (k,v) in scores.items() if v == SCORE_MAX}
            rows.append({'Puzzle name': puzzle['labelTitle'].removesuffix('- Code Golf'), '# Solutions': len(top1), **top1})
            submitted_languages.update(top1.keys())
        else:
            highest5 = get_highest_values(scores)
            total = sum(highest5.values())
            grand_total += total
            submitted_languages.update(highest5.keys())
            rows.append({'Puzzle name': puzzle['labelTitle'].removesuffix('- Code Golf'), 'Total': total, '# Solutions': len(highest5), **highest5})

    sort_column = '# Solutions' if only_top1 else 'Total'
    rows.sort(key=lambda d: (-d[sort_column],d['Puzzle name']))

    with open(OUTFILE, 'w', newline='') as f:
        columns = ['Puzzle name', 'Total', '# Solutions'] + sorted(list(submitted_languages))
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
        if not only_top1:
            writer.writerow({})
            writer.writerow({'Puzzle name': 'Grand total', 'Total': grand_total})


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('Usage: cg_golf_stats.py <userid> [--only-top1]', file=sys.stderr)
        sys.exit(1)
    main(sys.argv)
