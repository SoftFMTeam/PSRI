@echo off
set virtualenv_path="venv"
call %virtualenv_path%\Scripts\activate.bat

echo run process
set python_script="src/main.py"
set parameters=%*

python %python_script% %parameters%
echo Success!
pause
