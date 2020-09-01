# Trophy Manager Journal
[tmjournal.tk](https://tmjournal.tk)

[TrophyManager.com](http://trophymanager.com/?c=4322018)

## Extract:

**insert_data.py**

I extract game data basically through web scraping.<br />
Before season start I collect all the links of all fixtures of the season.<br />
Basically I store all data in two databases (well, my bad architecture).<br />
I managed to separate in lists which countries have their games earlier so I can run the collection as soon as the games are finishing.


## Automate screenshots:

### Take screenshots on html elements

**screenshots.py**

In fact I need help in some points:

1 - If is possible determine window size of a headless browser. I can't run a headless browser in full screen mode.<br />
2 - Well, if I could take a screenshot of full page even without full screen mode setting the property full of method screenshot().<br />
Didn't work for me: *screenshot_path = browser.screenshot('absolute_path/your_screenshot.png', full=True)*<br />
3 - Get the size and coordinates of a element easier than this: *table_location = table.\__dict__\['_element'].location*<br />
Didn't work: *element.location* and *element.size*.

See this script in action:
[Automate screenshots](https://www.youtube.com/watch?v=R-EeywMeXvI)


