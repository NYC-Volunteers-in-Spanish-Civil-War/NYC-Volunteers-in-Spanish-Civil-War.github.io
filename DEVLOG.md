# TODO
- [ ] Add seperate buttons to push volunteer data vs all data to site. Possible checklist in push modal/
- [ ] Add context section: giving information about the war and its context
- [ ] Add further information section, linking to other sites and SCW resources
# DEVLOG

## July 2, 2020
- Refactored backend UI using bootstrap grid system.
- After saving the selector will now display the correct status instead of simply assuming it to be modified
- Added a bootstrap login modal for pushing code to live site. Handles all cases and tweaks accordingly: no changes, wrong login information, and success. Even better, it does it in style.

## July 1, 2020
- Refactored the backend code to use the new modularized system
- Implemented more efficient status checking using checksums
- Refactored the volunteer information page to use the new system, just in time instead of bulk data download
- Added original webscraping code to the repository.

## June 30, 2020
- Created a script to port the existing data over to a more modularized format
- Added checksums to help detect changes between the local and remote branch

## May 26, 2020
- Fixed a tag overflowing biography section on mobile. Minor improvements to site UI.

## May 25, 2020
- Added mobile support for archive page. Refactored biographies to use flexboxes, so images come after the text on small screens.

## May 24, 2020
- Added status field to data, and a display for it. You can now easily tell if something is PUBLISHED, MODIFIED, or UNMODIFIED
- Improved backend styling considerably. 
- Stopped overlow in and generally improved image uploader interface.

## May 23, 2020
- The archive page now displays images pertaining to the volunteer side by side with the text.
- Updated run.sh to have better behavior
- Minor improvements to landing page and fixed a typo
- Better error handling for upload function
- Restructured upload form, image upload now next to editor, preview section is underneath
- Added the ability to add captions for images
- Added image caption display
- The data file is now pretty printed as its saved. Format is now human readable.

## May 22, 2020
- Added two(Volunteer Images and School Crests) buttons with which to upload pictures
- Under each button is a list of pictures, and a button to delete them

## May 20, 2020
- Removed contact section on landing page
- Shrunk the black bottom margin section

## May 17, 2020
- Added button to push changes to live site
- Completed upload form's basic functionality.
- Added basic .sh script to run the uploading program correctly
- Made the archive page load and display volunteer data
- Added preview to upload form
- Added ability to delete volunteer information
- Fixed form sanitation bugs. Improved from handling / page transfers.
- Created DEVLOG

## May 16, 2020
- Created basis of uploading form
