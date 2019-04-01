# SitsiTeX
## What is SitsiTeX?
Having developed this for my personal use in order to easily generate good-looking songbooks for Sitsits, I decided to share this with other songmasters in order to simplify the songbook creation process and make the result more elegant using the power of LaTeX. This comes with the added benefit of being able to share a common song library for all users, further spreading the love for one of our favorite activities.

## Packages needed
SitsiTeX relies on a specific package, [`songs.sty`](http://songs.sourceforge.net/), for most of the formatting. Please use the installed version.

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
* Song data structure improvements
  * Raw text instead of LaTeX format
  * Song reference glossary
  * Song variations
  * Per-verse selection
  * Separation from the repo
* Page layout improvements
  * Optimize song order with constraints
* Script
  * Ability to pass parameters for quietness and others
  * Ability to wipe all generated files

## Versions
### 0.2 (current)
* Added `booklet.tex`, which generates the booklet
* Added `src` folder, with subfolders:
  * `aux_files` for LaTeX auxiliary files
  * `images` for images with a cover template
  * `outputs` for compiled PDFs
* Added `tools` folder for various helper tools
  * `songbook_cover.psd`, a Photoshop file correctly sized to design covers
* Added lots of songs to `songbook.dat`
* Script for generating an arranged long-edge songbook for printing
  * Generates songbook in sequential and arranged versions
  * Keeps files organised
* Fixed table-of-content anchors not pointing to the beginning of songs

### 0.1
* Initial commit
* Works but is not convenient to use nor customizable, and is thus not ready for public use. 
* Includes :
  * 1 `.tex` file for the PDF structure
  * 1 `.sty` file for formatting functions
  * 1 `.dat` file for song data
