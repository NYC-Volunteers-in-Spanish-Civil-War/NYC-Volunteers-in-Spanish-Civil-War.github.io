trap "kill 0" EXIT
git pull origin
py -2.7 update.py &
py -2.7 -m SimpleHTTPServer 8000


