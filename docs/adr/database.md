# Database

## Requeriments

* Should allow several users.
* We should have a policy that respects the privacy of those users.
	* Have one ddbb with several logical users, and the admin fixes the use of
        that database.
	* For example each X months all the ddbb of the user Y is deleted therefore
        forcing them to have their own server.

The content in the database will have three states:
* Downloaded: The content has already been downloaded.
* Pending: The content is waiting to be downloaded.
* Waiting: The content is not downloaded and it's not in the queue to download,
    we'll just save the metadata.

## Initial database design

This database is my first attempt to design it, it must be used as an initial
list of elements that seem important. The structure can be thrown to /dev/null.

Notation: This is the initial design of the database I made, I posted it here
just to show what data was available, the * field was the primary key, each
indentation is a new table either data or subset.

* content
	* Type: Data
	* Description: The most generic kind of file
	* Subsets:
		* content_fetchs
			* Type: Subset
			* Description: Registers the metadata of the fetchs of contents
			* Field list:
				* content_fetch_id
				* content_id
				* content_fetch_date
				* content_fetch_status (downloaded, pending_download, started)
		* songs
			* Type: Subset
			* Description: Special fields of the songs
			* Field list:
				* content_id
				* song_length
				* song_coverart_location
					(In the server)

			* Subsets
				* lyrics
					* Type: Subset
					* Description: Save the lyrics of the songs (use picard? )
					* Field list:
						* content_id
						* song_lyrics

				* soundcloud_songs
					* Type: Subset
					* Description: Special fields of soundcloud songs
					* Field list:
						* content_id
						* soundcloud_song_description

				* soundcloud_song_updates
					* Type: Subset
					* Description: Saves the statistical evolution of the
						metadata of the soundcloud song ( this could also be inferred through a history log?)
					* Field list:
						* soundcloud_update_id
						* content_id
						* soundcloud_update_date
						* soundcloud_song_reproduction_count
						* soundcloud_song_likes_count
						* soundcloud_song_reposts_count
						* soundcloud_song_comments_count

				* youtube_songs
					* Type: Subset
					* Description: Special fields of youtube songs
					* Field list:
						* content_id
						* youtube_song_description

				* youtube_song_updates
					* Type: Subset
					* Description: Saves the statistical evolution of the
						metadata of the youtube song
					* Field list:
						* youtube_song_update_id
						* youtube_song_update_date
						* content_id
						* youtube_song_reproduction_count
						* youtube_song_likes_count

		* videos
			* Type: Subset
			* Description: Special fields of videos
			* Field list:
				* content_id
				* video_length
				* video_description

			* Subsets
				* video_updates
					* Type: Subset
					* Description: Saves the statistical evolution of the
						metadata  of the youtube video ( this could also be inferred through a history log?)
					* Field list:
						* video_update_id
						* video_update_date
						* content_id
						* video_reproduction_count
						* video_likes_count
		* pictures
			(No extra fields)
			* Subsets
				* 9gag_pictures
					* Type: Subset
					* Description: Special fields of 9gag pictures
						(we don't want to follow the evolution of 9gag)
						pictures... it's a waste of time, net, cputime...
					* Field list:
						* content_id
						* 9gag_title
						* 9gag_comment_counter
						* 9gag_points counter

				* deviantart_pictures
					* Type: Subset
					* Description: Special fields of deviantart pictures
					* Field list:
						* content_id
						* deviantart_title
						* deviantart_picture_description
						* deviantart_camera_make
						* deviantart_camera_model
						* deviantart_camera_shutter_speed
						* deviantart_camera_aperture
						* deviantart_camera_focal_length
						* deviantart_camera_iso
						* deviantart_camera_software

				* deviantart_picture_updates
					* Type: Subset
					* Description: Statistical metadata  of deviantart picture
					* Field list:
						* deviantart_picture_update_id
						* deviantart_picture_update_date
						* content_id
						* deviantart_picture_daily_deviation
						* deviantart_picture_views_counter
						* deviantart_picture_favourites_counter
						* deviantart_picture_comment_counter
						* deviantart_picture_download_counter

* playlists
	* Type: Data
	* Description: Generic metadata of playlists (group of contents)
	* Field list:
		* playlist_id
		* playlist_name
		* playlist_url
		* playlist_arrival_to_queue_date

	* Subsets
		* playlist_fetchs
			* Type: Subset
			* Description: Registers the metadata  of the fetchs of playlists
			* Field list:
				* playlist_fetch_id
				* playlist_id
				* playlist_fetch_date
				* playlist_fetch_status (downloaded, pending_download, started)

		* playlist_updates
			* Type: Subset
			* Description: Statistical metadata  of playlists
			* Field list:
				* playlist_update_id
				* playlist_id
				* playlist_update_date
				* playlist_update_status (started, finished)

		* song_playlists
			* Type: Subset
			* Description: Special fields of song playlists
			* Field list:
				* content_collection_id
				* song_playlist_publication_date
				* song_playlist_coverart_location
					(on server)
				* song_playlist_description
			* Subsets
				* soundcloud_playlist_updates
					* Type: Subset
					* Description: Special fields of soundcloud song playlists
					* Field list:
						* playlist_update_id
						* soundcloud_playlist_likes_counter
						* soundcloud_playlist_reposts_counter
				* 8tracks_playlist_update
					* Description: Special fields of 8tracks song playlists
					* Field list:
						* playlist_update_id
						* 8tracks_playlist_likes_counter
						* 8tracks_playlist_replays_counter
						* 8tracks_playlist_comments_counter

		* article_playlists
			* Type: Subset
			* Description: Special fields of articles playlists (blogs)
			* Field list:
				* playlist_id
				* article_playlist_following_status (not known, following, dont want to follow)
				* rss_feed_url
				* article_playlist_coverart_location
					(icon of the blog)

* playlist_collections
	* Type: Data
	* Description: Registers the metadata  of the collections (groups of playlists)
	* Field list:
		* playlist_collection_id
		* playlist_collection_name
		* playlist_collection_url
		* playlist_collection_arrival_to_queue_date
		* playlist_collection_following_status (not known, following, dont want to follow)

	* Subsets
		* playlist_collections_updates
			* Type: Subset
			* Description: Registers the metadata  of updates of the collections
			* Field list:
				* playlist_collections_update_id
				* playlist_collections_id
				* playlist_collections_update_date
				* playlist_collections_update_status (started, finished)

* sites
	* Type: Data
	* Description: Registers the metadata of the sites, playlists and collections (for example 8tracks.com/8cvetko or soundcloud.com/ahrix)
	* Field list:
		* site_id
		* site_webpage_type (8tracks, youtube, vimeo, deviantart, tumblr)
		* site_coverart_location
			(Image of the webpage)
		* site_url
			(8tracks.com/8cvetko)
		* site_following_status (0,1,*1)
			(1 following, 0 not following, *1 i don't want to follow this
            person)
		* site_description
		* site_arrival_to_queue_date

* authors
	* Type: Data
	* Description: Stores the metadata of the authors of content, playlists,
		collections and sites
		(It must follow other structure, for example if a guy has an)
		8tracks profile, a soundcloud and a youtube profile I want all of
		them linked together
		(This also works for songs authors, for example, last.fm,)
		discogs, official webpage of metallica,.....
	* Field list:
		* author_id
		* author_name
		* author_description
		* author_url

* genres
	* Type: Data
	* Description: Stores metadata  of genres (all kind of genres,
		songs, videos, articles, pictures...)
	* Field list:
		* genre_id
		* genre_name
		* genre_type

* tags
	* Type: Data
	* Description: Stores metadata  of tags (all kind of genres,
		songs, videos, articles, pictures...)
	* Field list:
		* tag_id
		* tag_name

* browsing_history
	* Type: Data
	* Description: Stores the metadata of the reproductions and actions of the real user
	* Field list:
		* browsing_reproduction_id
		* content_id
		* browsing_reproduction_date
		* browsing_reproduction_user_action
		* browsing_reproduction_user_score (0,1,2,3,4,5)

* real_users
	* Type: Data
	* Description: Stores the metadata  of the different users of the program hosted on the same server
	* Field list:
		* real_user_name
		* real_user_joined_date
