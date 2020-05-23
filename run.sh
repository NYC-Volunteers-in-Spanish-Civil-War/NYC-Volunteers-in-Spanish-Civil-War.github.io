trap "kill 0" EXIT
git pull origin
python update.py &
python -m SimpleHTTPServer 8000


