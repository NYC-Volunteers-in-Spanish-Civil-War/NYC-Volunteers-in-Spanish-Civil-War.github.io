# TODO (Vaguely Increasing Priority)
- [ ] Spruce up backend form inputs.
- [ ] Look into adding a license.
- [ ] Subscribe link, we mail them when we add new features or lots of new updates to our archives.
- [ ] Add URL option to image upload.
- [ ] Add social media sharing on site 
- [ ] Add printing option to volunteer biographies
- [ ] Look into OCR libraries for COMINTERN archives
- [ ] Improve document/tag pages UI, add scrolling to necessary sections.
- [ ] Add cite option to document/tag pages
- [ ] Add tag manager and descriptions of each tag, add way to view descriptions
- [ ] Move to using published instead of class of
- [ ] Detect if password valid before commiting in upload modal
- [ ] Update volunteer searcher to navigate to a new page with the search string passed as a get request, like documents
- [ ] Leftpad document urls with 0s
- [ ] Convert sources to a bibtext or similar jsony format and integrate a plugin to work with them
- [ ] Accesibility review and updates

# DEVLOG

## December 27, 2022
- Added dividers to archive page to mark letter sections
- Renamed "archives" link to "biographies" (less confusion)
- Added ability to search by tag on biographies page, click tag listed under name to search

## June 5, 2022
- Optimized cache. Cache now has 4 hour expiry time.
- Removed google analytics from site when running locally.
- Added tag searching functionality to archive page. 
- Added rudimentary tag management system to editor page.
- Added biography count to archive page

## June 4, 2022
- Added suggested tags feature to editor page, tags similar to biography text are automatically suggested.

## July 13, 2021
- Fixed bug caused by porting, Editor option is no longer saved statically.
- Cleaned up codebase a little more
- Updated archive page to create then cache a serialized index for searching if it doesn't exist, updated master archive json to include the biography text.
- Updated title across site

## July 12, 2021
- Refactored codebase, split project into more files to keep it manageable

## Jun 2, 2021
- Updated title across site

## May 25, 2021
- Added search to volunteer editor

## May 22, 2021
- Added search functionality to volunteer page.
- Updated document and tag pag design.

## May 21, 2021
- More improvements to home page design.

## May 20, 2021
- Updated home page design.
- Added trigger for building the misc. non-content pages

## May 19, 2021
- Fixed bugs in editor caused by porting to Python 3

## May 2, 2021
- Added better descriptions and titles to the document and tag pages, as well as the index.

## May 1, 2021
- Improved COMINTERN document data representation
- Finished the site templates, all files are now correctly rendered
- Updated index so that background image takes up less space and the site directory is now immediately visible
- Updated sitemap to include the new files and use unicode encoding
- Updated sitewide document search to sort the rendered items

## Apr 25, 2021
- Added templates for navigating the COMINTERN archives by tags and by hierarchical index.
- Created a helper js class that deals with lunr.js search for the tags and the documents, both local and sitewide
	- The datasets are cached locally so they don't have to be pulled from the server unless absolutely necessary
- Updated local instance of flask frozen to include a blacklist. Will later make a pull request for it.

## Apr 21, 2021
- Added SovDoc Scraper that connects to the google translate API
- Added an Interbrigades Scraper that uses the google translate API and nifty cacheing
- Added file to process the data into a useful format

## Apr 9, 2021
- Updated site to generate all files from base and extended templates
- Added requirements.txt
- Made editor page a page on the site derived from the base that only shows up on a local/debuggin server

## Mar 19, 2021
- Added static page generation for each volunteer for SEO purposes. Updated home, map, and archive pages to direct there.
- Added sitemap/sitemap generation and a robots.txt.

## July 27, 2020
- Fixed map page title
- Updated map so you can't zoom out farther than an overview of the whole map
- Updated map configuration to be more accessible. Larger font and text-wrapping.
- Added a site directory to the home page.

## July 26, 2020
- Added a map page, displays tags as a network.

## July 25, 2020
- Added tags to all volunteer biographies.
- Updated README images of backend to incorporate the new tags.
- Added tags to the archive page.

## July 22, 2020
- Added a tag system to the uploading page and backend. 
- Gave all data files tag fields.

## July 20, 2020
- Made link to volunteer biography cause the page to automatically scroll into view.
- Added a favicon, the emblem of the international brigades.

## July 19, 2020
- Looked at the google analytics reports, realized that newcomers are lost on the archives page. Added "click to expand" hints to the volunteer names that dissapear on first click, and are then replaced by tooltips.

## July 18, 2020
- Changed volunteer carousel to horizontal swiping on mobile. 

## July 17, 2020
- Added a context/further reading page that gives a brief overview of the war and the volunteer brigades.
- Removed site navigation code left over from the previous version.
- Restructured navbar to be more intuitive. Moved contact to end and changed about to home.
- Fixed bug, volunteer biography wouldn't open in chrome.

## July 16, 2020
- Fixed school image sizing bug
- Made archive page automatically open volunteer biography if the key was provided in the url.
- Added volunteer carousel on the home page. Displays images of and links to random volunteers.

## July 14, 2020
- Removed contact section from main page.
- Added a contact page that uses a google form.
- Added active setting to navbar sections. Now displays current page in case the user forgets.

## July 13, 2020
- Added metadata to the site's pages: description, keywords, title, author. Also added a noindex to the backend site page.
- Added google analytics tracking.
- Added new image to readme display of backend. They now contain the sources section.
- Changed front page brigade image to a jpeg to drastically reduce loading time.
- Got rid of junk scss and font files.

## July 12, 2020
- Added a source section to the uploading page as well as the archive page (each biography has its own sources section).
- Updated the archive to use these, as well as fixed broken links researchers had provided.
- Added a source page that pulls the links from sources and presents them so people can do further research should they so choose.
- Fixed the indentation on the html files.
- Refactored the site to use Bootstrap to a larger extent. 

## July 11, 2020
- Changed header to a bootstrap navbar, now works on all screen sizes.
- Added a standard footer to the sites pages with a copyright notice.
- Ported site to the latest versions of bootstrap and jquery, with better integrity checking.
- Removed junk JS files.
- Fixed uploading bug, username and password weren't being properly passed to the push command.

## July 6, 2020
- Added a README to the site. Gives a breakdown of the code base.

## July 3, 2020
- Added checkboxes to upload modal that allow the user to choose which changes to push live.
- Improved commit message on data upload the lists the volunteers affected and how.

## July 2, 2020
- Refactored backend UI using bootstrap grid system.
- After saving the selector will now display the correct status instead of simply assuming it to be modified.
- Added a bootstrap login modal for pushing code to live site. Handles all cases and tweaks accordingly: no changes, wrong login information, and success. Even better, it does it in style.

## July 1, 2020
- Refactored the backend code to use the new modularized system.
- Implemented more efficient status checking using checksums.
- Refactored the volunteer information page to use the new system, just in time instead of bulk data download.
- Added original webscraping code to the repository.

## June 30, 2020
- Created a script to port the existing data over to a more modularized format.
- Added checksums to help detect changes between the local and remote branch.

## May 26, 2020
- Fixed a tag overflowing biography section on mobile. Minor improvements to site UI.

## May 25, 2020
- Added mobile support for archive page. Refactored biographies to use flexboxes, so images come after the text on small screens.

## May 24, 2020
- Added status field to data, and a display for it. You can now easily tell if something is PUBLISHED, MODIFIED, or UNMODIFIED.
- Improved backend styling considerably. 
- Stopped overlow in and generally improved image uploader interface.

## May 23, 2020
- The archive page now displays images pertaining to the volunteer side by side with the text.
- Updated run.sh to have better behavior.
- Minor improvements to landing page and fixed a typo.
- Better error handling for upload function.
- Restructured upload form, image upload now next to editor, preview section is underneath.
- Added the ability to add captions for images.
- Added image caption display.
- The data file is now pretty printed as its saved. Format is now human readable.

## May 22, 2020
- Added two(Volunteer Images and School Crests) buttons with which to upload pictures.
- Under each button is a list of pictures, and a button to delete them.

## May 20, 2020
- Removed contact section on landing page.
- Shrunk the black bottom margin section.

## May 17, 2020
- Added button to push changes to live site.
- Completed upload form's basic functionality.
- Added basic .sh script to run the uploading program correctly.
- Made the archive page load and display volunteer data.
- Added preview to upload form.
- Added ability to delete volunteer information.
- Fixed form sanitation bugs. Improved from handling / page transfers.
- Created DEVLOG.

## May 16, 2020
- Created basis of uploading form.
