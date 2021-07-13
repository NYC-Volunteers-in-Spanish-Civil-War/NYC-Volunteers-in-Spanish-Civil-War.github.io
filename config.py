# ckeditor configuration
CKEDITOR_PKG_TYPE = 'standard'
CKEDITOR_HEIGHT = 500

# Freezer configurations
FREEZER_BLACKLIST = ['*ckeditor*', 'ckeditor.static']
FREEZER_DESTINATION_IGNORE = ['.git*', 'env*', 'scraping*', 'templates', 'update.py', '*.json', 'images*', 'js*', 'favicon.ico', 'css*', 'robots.txt', 'CNAME', '*.md', 'run.sh', '.emacs*', 'requirements.txt']
FREEZER_IGNORE_MIMETYPE_WARNINGS = True
FREEZER_IGNORE_404_NOT_FOUND = True
FREEZER_DESTINATION = ''
FREEZER_REMOVE_EXTRA_FILES = False


