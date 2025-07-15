#!/bin/bash
source venv/bin/activate
nohup python receiver.py all > "$HOME/output_receiver.log" 2>&1 &
