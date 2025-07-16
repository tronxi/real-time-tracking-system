#!/bin/bash
source venv/bin/activate
nohup python -u receiver.py > ~/output_receiver.log 2>&1 &