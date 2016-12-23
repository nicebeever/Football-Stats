#!/bin/bash

cd ./football/lib/Source

echo Updating football data
echo Updating results from BBC web page
python3 reports.py

echo Updating results
python3 resultUpdate.py
echo Updating football tables
python3 tableUpdate.py
echo Update player details
python3 updatePlayers.py

echo Finished
