This is the example file for creating your own song banks. We use Markdown as it allows us to have a clean visualization of our song banks while keeping our data easily compilable for the songbooks.  

Here is the standard format for a song:  

    ## Title
    #### Subtitle
    ###### codeofthesong

        Comments (just preceed with 4 spaces)
        More comments

    > Special line  
    Verse 1 Verse 1 Verse 1 Verse 1  
    Verse 1 Verse 1 Verse 1 Verse 1  
    Verse 1 Verse 1 **Important Words**  
    Verse 1 Verse 1 **Important Words**  

    _(Special bit)_ Verse 2 Verse 2 Verse 2 Verse 2  
    _(Special bit)_ Verse 2 Verse 2 Verse 2 Verse 2  
    Verse 2 Verse 2 Verse 2 Verse 2  
    Verse 2 Verse 2 Verse 2 Verse 2  

    :;: Repeat Repeat Repeat :;:  
    Repeat More Repeat More (x3)

Absence of a **_title_** and a **_code_** will prevent your song from being used!

- The **title**, which must be preceeded by `##` (2 times).

- The **subtitle**, which must be preceeded by `####` (4 times). The typical use case is:
        
        #### To the tune of "Other Song Name"

- The **code**, which must be preceeded by `######` (6 times). **This code is very important**, as it will allow you to select the song for use in the songbook. Using the following syntax will allow you to pretty print it in the registry :

        SongCode_VersionName_VersionNumber

 Thus when you write :  

        ## Title
        ###### mysong_fun_3

 in file `xy.md`, this will appear in the registry:

        <Song Title> - Fun Version 3
        Code: xy_mysong_fun_3  

- **Comments**, where each line must be preceeded by 4 spaces. Warning: this feature is not well supported currently and will be lost when running the script. Comments will **NOT** appear on the songbook.
  
- **Special lines**, which indicate instructions for the songs. They are surrounded by `_` which make them appear in italic. Parentheses should be used within. The typical use cases are:

        > Songmaster solo:
        > Everyone:

- **Special bits**, when a small instruction applies to just one line. Same format as above, but within a line. Here we wrote `___(Special bit)___`. The typical use cases are:

        ___(Solo:)___
        ___(All:)___

- **Repeat segments**, when a section of the song must be repeated. If it is just one repetition, `:;:` must be put before and after the section. This can cover multiple lines. If more repetitions are needed, simply add `(x3)`, `(x4)`, etc at the end of the line. Use a **Special line** instead if a whole paragraph needs to be sung more than twice.

- Any text can be made _ITALIC_, **BOLD** or even **_BOTH AT ONCE_** by wrapping it in 1, 2 or 3 asterisks (`*`) respectively. Underscores (`_`) can also be used instead. Use this sparingly, though.  Here are all possibilities: 

    - `*ITALIC*` or `_ITALIC_`
    - `**BOLD**` or `__BOLD__`
    - `***BOTH AT ONCE***` or `___BOTH AT ONCE___`

- **Double spaces are needed** at the end of each line. Some markdown viewers will not break those lines otherwise. The compilation script is a nice fellow and will fix your song bank where double spaces are missing. When in doubt, just run it once!  