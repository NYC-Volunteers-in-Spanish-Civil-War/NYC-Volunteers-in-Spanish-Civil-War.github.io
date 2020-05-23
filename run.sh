trap "kill 0" EXIT
python -m SimpleHTTPServer 8000 &
python update.py

