# SitsiTeX
## What is SitsiTeX?
Having developed this for my personal use in order to easily generate good-looking songbooks for Sitsits, I decided to share this with other songmasters in order to simplify the songbook creation process and make the result more elegant using the power of LaTeX. This comes with the added benefit of being able to share a common song library for all users, further spreading the love for one of our favorite activities.
## Packages needed
SitsiTeX relies on a specific package, [`songs.sty`](http://songs.sourceforge.net/), for most of the formatting. The package is provided in this repo, but can also be directly installed on your computer. Using the file version of the package causes 2 errors to appear when compiling, but these should be ignored as they do not affect the end result. A fix for this is being worked on.
## To be implemented
- Booklet generation
- Tutorial
  - Library installation
  - Functionalities
  - Example songbooks
- Packages
  - Refactoring of the packages used
- More customization
  - Inter-song content
- Song data structure improvements
  - Raw text instead of LaTeX format
  - Song reference glossary
  - Song variations
  - Per-verse selection
  - Separation from the repo
- Page layout improvements
  - Optimize song order with constraints
- Bugfixes
  - Table-of-contents page number anchors at end of songs
## Versions
### 0.1
- Initial commit
- Works but is not convenient to use nor customizable, and is thus not ready for public use. 
- Includes :
  - 1 `.tex` file for the PDF structure
  - 1 `.sty` file for formatting functions
  - 1 `.dat` file for song data
