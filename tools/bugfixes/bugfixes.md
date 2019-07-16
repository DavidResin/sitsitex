A number of bugs encountered as well as their fixes are listed here:

## LaTeX: Extra else error
Latex might freak out saying there is an extra `\else` at line 44 the `songs.py`. It seems some installations do not like version 3.1 of this package. You should manually replace the package with the one provided here (version 3.0).

## LaTeX: Font expansion error
Some installations of pdfTeX will fail on compilation saying "auto expansion is only possible with scalable fonts". It seems using `\include{lmodern}` fixes this problem. I have done this by default in `songbook.sty`.