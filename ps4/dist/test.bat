@echo off
set count=1
:loop
if %count%==5 goto end
set my_filename=my.%count%.png
set tas_filename=tas.%count%.png
python E:\study\6.006\6.006\ps4\dist\dnaseq.py E:\study\6.006\6.006\ps4\dist\data\0.fa E:\study\6.006\6.006\ps4\dist\data\%count%.fa %my_filename%
python E:\study\6.006\6.006\ps4\dist\dnaseq-sol.py E:\study\6.006\6.006\ps4\dist\data\0.fa E:\study\6.006\6.006\ps4\dist\data\%count%.fa %tas_filename%
set /a count+=1
goto loop
:end