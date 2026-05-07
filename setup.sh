#!/bin/bash
# setup.sh — run once after cloning
pip install -r requirements.txt
cd website && npm install && npm run build