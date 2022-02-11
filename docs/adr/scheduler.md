# Scheduler

Python program to generate an ordered list of content to download and call the
scrapper.

## To read
https://www.fullstackpython.com/celery.html
https://tests4geeks.com/blog/python-celery-rabbitmq-tutorial/
https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html


## Requirements

* Fetch content reducing the browsing fingerprint.
* Change in real time the content to download.

## Workflow

* When the daemon starts it reads the scored ordered download list by the brain
    and launches the schedule download list generator.
* It sleeps till the date of the first item of the list.
* If some event changes the download list and places an item before the next
    scheduled item, the brain triggers the scheduler to wake up and relaunch the
    download list generator.
* Once the daemon wakes it checks the pending downloads of the current slot time
    and launches the scrapper on the selected jobs.

## Interfaces

* Get
	* Metadata from the database.
	* Score ordered download list.
	* Called by the brain if download list changes.

* Put
	* Calls scrapper to perform its actions.

## Schedule download list generator

The scored download list given by the brain will give:

* the item id.
* a vector of relative time curl queries (for example if a playlists has to
    download 5 songs plus 3 queries to get the information needed we'll have
    [ 0 0 0 0 300 357 ...] being the last digits the length to wait between
    downloads) .
* the latest download date of the item. .
* The scrapper module of the url.
* The type of download: metadata, content or metadata+content.

With this information we'll generate a gaussian browsing profile to hide the
user browsing fingerprint.

* Get the content download list ordered by score for a specified time (6h).
* Calculate the number of curl queries that are needed for that period of time.
* Generate a gaussian noise signal, take only the positive part of the function,
    with resolution of 10s.
* Do the integral of the signal to know the overall queries.
* Adjust the amplitude of the gaussian noise so as the overall integral matches
    the calculated number of curl queries. Saving it in a vector called
    queries_vector.
* Asign a download date for each content.

	```
	calculate for all items the latest_download_start_date = latest download date - sum(relative_time_curl_queries)
	for i in $(ordered list of items by latest_download_start_date, earlier first)
		check the first nonzero slot in the queries_vector

		if the last download date < (the slot time + sum(relative_time_curl_queries))
			select a random start date from first slot to the latest_download_start_date slot
		else
			Assign that slot's date to the item's download date
			substract the relative_time_curl_queries vector ot the queries_vector
			if it produces any negative value, recursively substract those values to the closest non zero slot till no negative values exist
		fi
	end
    ```
