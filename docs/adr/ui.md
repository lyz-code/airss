# UI

* Program to show the content to the user.
* Program to fetch metadata from the user.

## Unclassified thoughts

Discover

Categorias: news, articles, images, videos, music, games, books

Being able to define a session, 10 mins news, 20 articles, 15 images,. ... with a slider that shows progress

All items are auto suggested, you should not select categories by default, although the possibility should be there.

Suggestions based on hour of the day

Present one item at the time, don't scroll

Have a system to visualize your ratings

Start by gather data:
webapp of news to gather data

Do clustering and introduce content outside the bubble

In news have different providers, rss reddit,. ..

For each source, have rating and certainty or confidence

Tap un 3, swipe izq un 2, tap abajo izq 1 swipe der 4, tap abajo der e5.

Swipe arriba al todo.

Foto modo galeria

Página estadísticas

Entee in vi mode to underline (hiher priority when text search) and mark important words, relevant for rating

Read on recpmrndation sysremd

* [ ] Interaction must be keyboard based
* [ ] It should be able to send articles to wallabag
* [ ] It should have an intuitive interface to mark as read

--- Optional

* [ ] Should have filtering methods
  * with a keyboard key you trigger a textbox to introduce the filter
  * items are marked as red for a while, and then hidden

## Requirements

* It must be multi platform, therefore it's best to have it as a web page (or
  a tkinter python program)
  * Flask web app would require to learn: flask and probably some javascript
  + css
  * Tkinter app would require to learn tkinter and
* It must be *really easy* to populate the database with new content
  * Populate it with external sources, wallabag, polar, mediarss, rss
* The interaction with the user requires the program to have:
* A search field
* A method to obtain the rating of the user of the current content
* UI to interact with hivemind
* Manage the social relationships between daemons
* Share content with other daemons
* All queries triggered by the UI to the database, must be documented as actions so as to be easy to make scripts with it or build the API
* Must have an optional "terminal" to enter commands such as mcabber
* The user must be able to manage all the program configuration through the UI and from editing local files
* It must not waste space, use all the space to show the content (tiling window manager or uzbl philosophy)

## Interfaces

* Get
	* Called by the user
	* Content and metadata from database
	* Score ordered browse list from database

* Put
	* Browsing user metadata to the database
	* User search queries to the database and hivemind (if selected)

## Command line API

Code language: python
* add: add url to the database (it can be an content/playlist/collection url)
* search: perform a search in the information of the database
	* Make the search intelligent, using bangs such as g! yt! of duckduckgo or ext: inurl:....
	* Create a bang system to ask only to the own daemon or to the own daemon + daemon group
* share: share the current content with:
	* hivemind daemon/group of daemons
	* email
	* gnusocial
* rooster: manage the daemon social system
	* useradd: add a daemon
	* groupadd group: create group
		* name
		* group permissions
	* mv daemon: add daemon to group
	* mv group: change group name
	* rm: delete daemon or group
	* info: get the daemon info
	* chmod group: change group permissions
* content: perform actions related with contents
	* download: add it to the download queue
	* download now: download the content *now* avoiding the scheduler algorithm
	* rate: log the rate of the current content
		* it is possible that several contents are displayed (a song and an article), the method must be clear to what content is being rated
	* info: get the contents information available in the database
* set: change the value of a configuration variable
* dump: dump the loaded configuration
* reload: reload the configuration
* web page: interact with the web page
	* hide sidebar
	* hide lowbar

## Web page

* There must be possible to interact with several contents (read an article while listening to a song)
* search field: so the user can type the query, then process the output and present it to the user in the main page
* share: a button somewhere near the content
* main page: Where the user is going to spend most of it's time
	* composition:
		* Tabs in the upper part of the page
			* Welcome/Discover: Homepage, when the user enters she gets this information
				* User stats:
					* View stats:
						* Number of new contents:
						* Number of good new contents:
XXXX
			* Article/Video/Picture page:
XXXX
			* Audio page:
XXXX
* configuration: there must be a configuration button where you can enter the "preferences" page, with the following tabs
	* configuration
		* display the configurations of the program in a user friendly way and make it easy to modify them
		* reset values to original -.-
		* it must contain the following tabs:
			*
XXXX
	* rooster
		* There the user must see:
			* Add field: to add new daemons/groups
			* The different daemon groups (interface like xabber,mcabber)
		* The user can interact
			* right click over the daemons/groups and get a menu or have buttons beside it with the following options
				* mv to group
				* delete
				* info
				* chmod
* sidebar:
	* There must exist the posibility to hide it
	* It must show the information like an rss sidebar with the following structure
XXXX

* lowbar:
	* score the content

* Discover page
	* Periodical report of:
		* internet users with a high affinity score
		* If I have several contents of the same author, suggest to follow him, get his discography, blog...
		* Forgotten content. Suggest content that in the past had been
			very popular for me but lately I've forgotten it (genres,
			contents, tags...)
		* Interesting stats
			* trending contents of the last X
			* Used space
			* Time saved xD
* Add interface: there must be an easy way to add new content while browsing the internet
	* For firefox: build a plugin

## Search algorithm

## Research

- How do we process the html in blogs, how do we show the articles in the ui, plaintext or html, and if the rss does it itself or we have to process it
