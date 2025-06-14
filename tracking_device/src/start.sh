#!/bin/bash
source venv/bin/activate
nohup python main.py all > "$HOME/output.log" 2>&1 &
