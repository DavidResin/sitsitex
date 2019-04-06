# SitsiTeX
## What is SitsiTeX?
Having developed this for my personal use in order to easily generate good-looking songbooks for Sitsits, I decided to share this with other songmasters in order to simplify the songbook creation process and make the result more elegant using the power of LaTeX. This comes with the added benefit of being able to share a common song library for all users, further spreading the love for one of our favorite activities.

## Packages needed
SitsiTeX relies on a specific package, [`songs.sty`](http://songs.sourceforge.net/), for most of the formatting. Please use the installed version.

## Versions
### Coming in 0.3
* References for ToC in PDF
* More checks in `make.sh`
* Song database:
  * Song reference glossary
  * More checks in song_bank.py
  * Partial compilation with error report
  * Auto-fix `.md` file line breaks
  * Reorganize structure and include in `make.sh`

### 0.3 "Song Bank" (current)
* Reforged the song structure. Now all modifications are made through Markdown files which are then compiled into one big data file ready to use. Everything is in the `python` folder with subfolders and files:
  * `format_conversion` for converting from old song data format
    * `songbook.dat`, old song data file
    * `dat-to-md.py`, Python script for conversion
    * `song_bank.md`, output of the script in the new Markdown format
  * `song_bank` for compiling LaTeX data files from song files
    * `song_bank.py`, Python script for compilation
  * `example.md`, a reference for song formatting
* GPL-3.0 license

### 0.2 "Auto Booklets"
* Added `make.sh`, the script that handles all compilations
  * Generates songbook in normal and booklet versions
  * Keeps files organised
* Added `booklet.tex`, which generates the booklet
* Added `src` folder, with subfolders:
  * `aux_files` for LaTeX auxiliary files
  * `images` for images with cover and back-page templates
  * `outputs` for compiled PDFs
* Added `tools` folder for various helper tools
  * `songbook_cover.psd`, a Photoshop file correctly sized to design covers
* Added lots of songs to `songbook.dat`
* Fixed table-of-content anchors not pointing to the beginning of songs

### 0.1 "Utter Mess"
* Initial commit
* Works but is not convenient to use nor customizable, and is thus not ready for public use. 
* Includes :
  * 1 `.tex` file for the PDF structure
  * 1 `.sty` file for formatting functions
  * 1 `.dat` file for song data
  
## To be implemented
* Tutorial
  * Library installation
  * Functionalities
  * Example songbooks
* Packages
  * Refactoring of the packages used
* Documentation improved
  * Comments
  * Package references
* More customization
  * Inter-song content
* Page layout improvements
  * Optimize song order with constraints
* Script
  * Ability to pass parameters for quietness and others
  * Ability to wipe all generated files
* Separation of songs from the repo
