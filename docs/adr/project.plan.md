# Airss Project Plan

## Project objectives and philosophy

Provide a program to allow people to:

* Control all their browsing metadata.
* Share only what they want with whom they want.
* Benefit from the data mining of their metadata to get a better browsing
    experience.
* Reduce the user browsing fingerprint.
* Adjust the configuration of the program to their needs easily.

## Project layout

![project layout](/doc/assets/airss_diagram_small.png)

* Downloader: Python programs to obtain the metadata and content from the sites
    populating the database.
* Scheduler: Python program to generate an ordered list of content to download
    and call the downloader.
* Brain: Python program to apply data analysis to the database:
	* Extract information from the database through data analysis.
	* Generate an updated scored list of content to download.
	* Generate an updated scored list of content to browse by the user.
	* Suggest new browsing content.
* UI: Program to show/fetch content/metadata to/from the user.
* Hivemind: Program to give/fetch information to/from other Airss.hivemind
    daemons.
