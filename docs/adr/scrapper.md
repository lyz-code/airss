# Scrapper

Python program to obtain the metadata and content from the sites populating the
database.

# Contents

This are the sites from which we take the content/metadata.

* Audio
	* [] Soundcloud.
	* [] Youtube.
	* [] Bandcamp.
	* [] last.fm.
	* [] discogs.
	* [] album reminder.
	* [] songkick.

* Video
	* [] Youtube.
	* [] Vimeo.

* Pictures
	* [] Deviantart.
	* [] Tumblr.
	* [] 9gag.

* Articles
	* [] Generic rss.

* Movies
	* [] bagmovies.com.
	* [] anime-planet.com.
.
* Books
	* [] gen.lib.rus.ec.

* Torrents
	* [] thepiratebay.se.
	* [] kat.cr.
	* [] nyaa.se.

* Games
	* [] humblebundle.com.
	* [] store.steampowered.com.

## Anonymity

We will use all the necessary tools if they guarantee the anonymity of the user.
* It must do distributed scrapping with multiple tor circuits.
	* Mustn't reveal the user IP address.
	* Must be encrypted.
* Must avoid as much as it's possible to log in the sites or use APIs that
    require tokens.

## [WIP] Generic scrapper module

* Generic web page layout: The most generic social web page has the following
    fields (though it may lack some of them).
* General user web page:
	* Data:
		* User name.
		* Description.
		* Following.
		* Followers.
		* ...
XXXXX
* Gallery web page: lists of collections, playlists and/or content made/compiled
    by the user.
	* Data.
		* collections url.
		* playlists url.
		* content url.
* Favourites web page: lists of collections, playlists and/or content liked by
    the user.
	* Data
		* collections url.
		* playlists url.
		* content url.
* Collection web page:
	* Data
		* Collection name.
		* playlists url.
* Playlist web page:
	* Data
		* Playlist name.
		* number of reproductions.
		* number of likes.
		* users who liked the playlist.
		* number of items.
		* genres.
		* tags.
XXXXX


## API analysis

Not usable is marked when API registration is needed, further analysis can be
done if the registration is trivial and we can register several keys.

* Audio
	* ~~8tracks~~
		* Auth: Api Key, Basic Auth (Baaah).
		* [Api Homepage](8tracks.com/developers).
		  Note: As of February 2015, we are no longer issuing new API keys..
		* Scrapper: Lyz's outdated written in bash.
		* Conclusion: API not usable, we'll have to rewrite the bash script in
            python and update it.

	* **Soundcloud**
		* Auth: OAuth2,OAuth1 OPTIONAL.
		* [Doc](https://developers.soundcloud.com/).
		* [Python wrapper](https://github.com/soundcloud/soundcloud*python).
		* [Programmableweb](http://www.programmableweb.com/api/soundcloud).
		* Conclusion: API USABLE.

	* ~~Bandcamp~~
		* Auth: Api Key.
		* [Homepage](http://bandcamptech.wordpress.com/2010/05/15/bandcamp-api/).
			Note: Sorry, the API is no longer supported and we're not granting
            any new developer keys..
		* [Wrapper 1](https://github.com/GIider/bandcamp).
		*	[Wrapper 2](https://github.com/eloe/Bandcamp-API).
		* [Scrapper](https://github.com/masterT/bandcamp-scraper).
		* Conclusion: API not usable, We can use masterT scraper or translate it
        to python3.

	* **Youtube**
		* Auth: OAuth 2, OPTIONAL.
		* [Homepage](https://developers.google.com/youtube/).
		* [Wrapper](https://pypi.python.org/pypi/youtube-api-wrapper/0.2).
		* Conclusion: API USABLE.

	* ~~last.fm~~
		* Auth: Api Key.
		* [Homepage](http://www.last.fm/api).
		* [Wrapper](http://code.google.com/p/python-lastfm/).
		* Scrapper: None found.
		* Conclusion: API not usable, not available scrapers, write one.

	* **discogs**
		* Auth: OAuth, OPTIONAL.
		* [Homepage](http://www.discogs.com/developers/)..
		* [Wrapper](https://github.com/discogs/discogs_client).
		* Conclusion: API USABLE.

* Video
	* **Youtube**.
		* API Usable.
	* ~~Vimeo~~.
		* Auth: not optional.
		* [Homepage](https://developer.vimeo.com/api).
		* [Wrapper](https://github.com/nirmalalmara/python-vimeo).
		* [Scrapper](https://github.com/svanderbleek/vimeo_scrape).
		* Conclusion: API not usable, scraper might work, else youtube-dl.

* Pictures
	* ~~Deviantart~~.
		* Auth: OAuth 2.
		* [Homepage](https://www.deviantart.com/developers/authentication).
		* Wrapper:None.
		* Scrapper: None.
		* Conclusion: Not sure if it requires auth or it doesnt, anyway there
            are no good scrapers or wrappers so, one has to be written.

	* ~~Tumblr~~
		* Auth: OAuth2.
		* [Homepage](https://www.tumblr.com/docs/en/api/v2).
		* [Wrapper](https://github.com/tumblr/pytumblr).
		* [Scrapper 1](https://github.com/xcthulhu/TumblrScraper).
		* [Scrapper 2](https://github.com/rranshous/tumblr_scraper).
		* Conclusion: API not usable, scrappers don't seem to be enough, maybe
        we can use part of the code.

	* ~~9gag~~
		* Doesnt exist.
		* [Scrapper 1](https://github.com/amferraz/9gag-scraper).
		* [Scrapper 2](https://github.com/sjs7007/9gag).
		* Conclusion: One of them is based on scrapy and the other seems to be
        very simple, maybe we can use part of the code.

* Articles
	* Generic rss.
		* Use feedparser python module.

## Resources

* Anonymity.
	* [Distributed scrapping with multiple tor
        circuits](blog.databigbang.com/distributed-scraping-with-multiple-tor-circuits).

* API.
	* http://pythonapi.com/.
	* http://www.programmableweb.com/.
