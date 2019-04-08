# SitsiTeX
## What is SitsiTeX?
Tired of reinventing the wheel many times over, I started developing this for my personal use in order to easily generate good-looking songbooks for Sitsits. Later, I then decided I would share it with other songmasters in order to simplify the process and make the result more elegant using the power of LaTeX. This comes with the added benefit of being able to share a common song library for all users, further spreading the love for one of our favorite activities.

## Information for contributors
Please make all your pull requests to `dev`, not `master`. I will apply changes to `master` from `dev` myself once I have made a changelog and tested everything sticks together nicely.

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
  * Multiple song files?
* Page layout improvements
  * Optimize song order with constraints
* Script
  * Ability to pass parameters for quietness and others
  * Ability to wipe all generated files
* GPL-3.0 license
