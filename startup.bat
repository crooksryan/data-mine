@echo off

echo Running Mass_Gather
python mass_gather.py

echo Running Machine
python scheduler.py

echo Finished