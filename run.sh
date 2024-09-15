#!/bin/bash

CG_ID=${1:-$CODINGAMER_ID}

if [ -z "$CG_ID" ]; then
  echo >&2 "Usage: ./run.sh <codingamer_id>"
  echo >&2 "To run script without argument, you can export your codingamer ID in CODINGAMER_ID environment variable"
  exit 1
fi

if [ ! -d venv ]; then
  python3 -m venv venv
  source venv/bin/activate 
  pip install -r requirements.txt
fi  

source venv/bin/activate
python cg_golf_stats.py ${CG_ID}
