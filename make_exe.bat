REM *** Used to create a Python exe 

REM ***** get rid of all the old files in the build folder
rd /S /Q build

REM ***** create the exe
python -OO setup.py py2exe

REM **** pause so we can see the exit codes
pause "done...hit a key to exit"