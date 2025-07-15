#!/bin/bash
source venv/bin/activate
nohup python receiver.py > "$HOME/output_receiver.log" 2>&1 &
