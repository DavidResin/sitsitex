## Title
#### Subtitle
###### Code
  
    Comments that won't appear in the songbook (4 spaces of indent)  
  
> Textual notes  
Verse 1 Verse 1 Verse 1 Verse 1  
Verse 1 Verse 1 Verse 1 Verse 1  
Verse 1 Verse 1 **Important Words**  
Verse 1 Verse 1 **Important Words**  
  
_(Special bit)_ Verse 2 Verse 2  
_(Special bit)_ Verse 2 Verse 2  
Verse 2 Verse 2 Verse 2 Verse 2  
Verse 2 Verse 2 Verse 2 Verse 2  
  
:;: Repeat Repeat Repeat :;:  
Repeat More Repeat More (x3)  

song = {
	"title": title,
	"subtitle": subtitle,
	"verses": [
		{
			# Lines
			"lines": [
				{
					"type": <meta/text>,
					"segments": [
						{
							"style": <b/i/bi>,
							"text": text
						}
						...
					]
				}
				...
			]
		}
		...
	]
}