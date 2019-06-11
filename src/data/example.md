This is the example file for creating your own song banks. We use Markdown as it allows us to have a clean visualization of our song banks while keeping our data easily compilable for the songbooks.  

Here is the standard format for a song:  

## Title
##### codeofthesong
- Subtitle

> Comments
> More comments

_(Special line)_  
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

Absence of a *title* and a *code* will prevent your song to be used!

- The **title**, which must be preceeded by `##`. Here we wrote `## Title`.
- The **code**, which must be preceeded by `#####` (5 times). Here we wrote `##### Code: codeofthesong`. **This code is very important**, as it will allow you to select the song for use in the songbook.
- The **subtitle**, which must be preceeded by `-`. Here we wrote `- Subtitle`. The usual case is:
    - To the tune of "Other Song Name"
- **Comments**, where each line must be preceeded by `>`. Here we wrote `> Comments` followed by `> More comments` on the next line. Comments will **NOT** appear on the songbook.
- **Special lines**, which indicate instructions for the songs. They are surrounded by `_` which make them appear in italic. Parentheses should be used within. Here we wrote `_(Special line)_`. The usual cases are:
    - _(Songmaster solo:)_
    - _(Everyone:)_
- **Special bits**, when a small instruction applies to just one line. Same format as above, but within a line. Here we wrote `_(Special bit)_`. The usual cases are:
    - _(Solo:)_
    - _(All:)_
- **Repeat segments**, when a section of the song must be repeated. If it is just one repetition, `:;:` must be put before and after the section. Here we wrote `:;: Repeat Repeat Repeat :;:`. This can cover multiple lines. If more repetitions are needed, simply add `(x3)`, `(x4)`, etc at the end of the line. Use a **Special line** instead if a whole paragraph needs to be sung more than twice.
- Any text can be made *ITALIC*, **BOLD** or even ***BOTH AT ONCE*** by wrapping it in 1, 2 or 3 asterisks (`*`) respectively. Underscores (`_`) can also be used instead. Use this sparingly, though. Here we wrote:
    - `*ITALIC*` or `_ITALIC_`
    - `**BOLD**` or `__BOLD__`
    - `***BOTH AT ONCE***` or `___BOTH AT ONCE___`

**Double spaces are needed** at the end of each line. Some markdown viewers will not break those lines otherwise. The compilation script is a nice fellow and will fix your song bank where double spaces are missing. When in doubt, just run it once!  