# TidyFilm

Renames movie folders and files, deletes unwanted files, and moves to a new directory

Can be compiled to .exe with Pyinstaller: https://github.com/pyinstaller/pyinstaller a GUI for Pyinstaller can be found: https://github.com/vsantiago113/PyInstallerGUI

TidyFilm was made to solve a number of problems common with video files that are downloaded from the internet. Common problems include:

1. Movie file names often contain hyphens, underscores, and periods. They often include codec names, resolution, or uploader information and
lack dates and proper capitalization.

2. Movie files may not be contained within a folder or may be contained within multiple levels of folders.

3. Folders containing movies may also contain unwanted files such as .txt files, .nfo files, README files, and image files.

4. Subtitle files if present may suffer from the same problems as movie files as described in 1.

TidyFilm addresses the above problems in the following manner:

1. A source directory containing the movie files to be cleaned and a destination directory for the clean files to be moved to is specified.

2. Any video files not in a folder are put into a folder with the same name as the video file.

3. Video files that are contained within subfolders are moved to the top level.

4. The name of each folder is cleaned up by removing common unwanted characters such as periods and curly braces.

5. The googlesearch module with BeautifulSoup parsing is used to get the correct name and date of the movie by scraping IMDB.

6. The name and date scraped from IMDB is used to rename the folder, movie, and subtitle files.

7. Unwanted file types such as .txt, .nfo, .jpeg, etc. are deleted.

8. Files are moved from source directory to destination directory.
