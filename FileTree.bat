@echo off
rem 
pushd "%~dp0"
python main.py %*
rem 
popd
