trap "kill 0" EXIT
git pull origin
python -m http.server 8000 &
python update.py

