trap "kill 0" EXIT
git pull origin
python -m SimpleHTTPServer 8000 &
python update.py

