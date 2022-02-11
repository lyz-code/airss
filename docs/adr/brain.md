# Brain

* Python program to extract information from the database through data analysis.
* Python program to generate an updated scored list of content to download.
* Python program to generate an updated scored list of content to browse by the
    user.
* Python program to suggest new browsing content.

## Requirements

* Global
	* It must store the information generated for easy retrieval by the other
        programs.
	* It must periodically check metadata changes in the database so as to
        modify the information.
	* It must have a temporal algorithm to update the social information.
	* It must be constantly learning and act accordingly.
	* It must assign a score to each content/playlist/collection based on the
        data analysis.
	* It must be modular for each scrapper module.
	* It must have a master module to manage the different scrapper modules.
	* It must save the calculated scores in fields of the table.

* Scheduler
	* Generate a score ordered list of content to download.
	* The list must be generated based on the information generated from the
        data.
	* It must continually check the changes on the database so as to modify the
        queues in real time.

* Ui
	* Generate a score ordered list of content to browse.
	* It must continually check the changes on the database so as to modify the
        queues in real time.

* Hivemind
	* Obtain the information of the other hivemind daemons.
	* Obtain information from the queries made between daemons.
	* Be able to answer the queries made from other daemons.

## Workflow

The brain is a daemon that launches several processes.

Daemons:

* Generate download list: At the start of the daemon it launches this process to
    generate the initial download list. It also must be reading the actions of
    the user so as to update the list if needed. If there is no event that
    changes the download list, it generates a new one periodically.
* Generate browse list: At the start of the daemon it launches this process to
    generate the initial browse list. It also must be reading the actions of the
    user so as to update the list if needed. If there is no event that changes
    the download list, it generates a new one periodically.
* Hivemind daemon: The daemon waits for the hivemind program to ask queries and
    answers them.

Cronjobs:

* Predict unscored content: This is a cronjob executed daily or twice daily to
    update the predicted scores of content. Once it finishes it launches the
    download and browse generators.
* Cleaning content: This is a cronjob executed daily to clean the low scored
    content if the content is obsolete or space is needed (maybe a new program).
* Discover process: This is a cronjob executed Xly. If there is new content to
    be added it adds it to the download list and if it needs it makes the
    calculus to get the new content.

## Interfaces

* Get:
	* Metadata from the database

* Put:
	* Score ordered download list
	* Score ordered browse list
	* Information to the database
	* Launches the event trigger to the scheduler

## Content score algorithm

* There must exist a predicted score of the content so as to calculate the
    browse and download scores, later we can do machine learning with this
    information as it is a labeled database.
* The predicted content score must be normalized.
* The predicted score will be the result of a lineal polinomial with variable
    weights (multiple regression) deduced by machine learning for each content.
    `predicted_score=sum(weight_i*score_i) ; sum(weight_i)=1 ; score_i = [0,5]
    -> predicted_score=[0,5]`.
* We'll have a generic formula for all the content types, and if the field is
    not applicable, the weight of that field = 0, but as `sum(weight_i)=1` the
    others will get more importance.
* The user will give his score of the content so as we can do further data
    analysis of our predictions.
* We'll save in the ddbb: the weights vector, the predicted score, the user
    score.
* The information of the fields has a low update frequency and as the ddbb grows
    the frequency decreases even more. Therefore we can update the prediction
    scores periodically, it doesn't have to be real time scores.
* Normalization of fields will go as follow: `normalized=scale_factor*
    variable_value/variable_max_value ; scale_factor=5` (if the score goes from
    0 to 5).
* Weight calculation algorithm:
	* We'll start by some initial weight vector. This could be predefined by
        content type or a standard for all content.
	* Once we have enough feedback from the user, we'll have a labeled ddbb.
	* We can apply then a least squares model with stochastic gradient descent
        to obtain the weight vector.
	* if one field has a null value the weight of the field = 0.
* Fields of the multiple regression:
	* Artist: score of the artist that made the content = sum(user
        score)/num_content.
	* Online View count: It's the view count scraped from the webpage
        normalized(view_count).
	* User view count: It's the view count of te user inside airss (number of
        times it reproduced the selected content) normalized().
	* Repost count: normalized(repost_count).
	* Comments count: normalized(recount_count).
	* Downloads count: normalized(download_count).
	* Likes/View count ratio: normalized(likes_count_ratio).
	* Genre score: Average sum of the genre scores = sum(user score of content
        with genre)/num_scored_content_with_genre.
	* Tag score: Average sum of the tag scores = sum(user score of content with
        tags)/num_scored_content_with_tags.
	* Natural language processing score: apply NLP to articles, song titles,
        descriptions... (described later).
	* View, repost, comments, downloads, likes/views, genre, tag score
        evolution????: as we have the evolution of this scores we can predict
        it's value in the future, interesting?
	* Average content score: for playlists/collections/user calculate the
        average user/predicted score of it's children items
        = sum(children_score)/num_children (if user score doesn't exist use
        predicted score).
	* site score: average score of the site. For example to priorize the
        microsiervos articles over the hipertextual's ones.

## Discover new content algorithm

The discover content algorithm only downloads metadata to try to make those
elements go high in score so as to show them to the user. Flag those contents as
comming from the discover algorithm to filter it later in the searchs.

This algorithm is divided in fetching data and processing data. The fetching
part will be added to the download list as another job.

The algorithm will check the unreviewed discover content and if it sees that
there is a lack of content in any one of the next paths it will execute the
algorithm again. It will also be executed if the last time the algorithm was
executed was X time ago.

This are the paths of discovering new content:

### Frequent not subscribed elements

Through the analysis of the browsing history we can deduce identities, tags,
genres, artists...  from which we liked their content but are not yet subscribed
to them. Once this happens suggest the user to follow those elements.

### Nearest neighbours

Do a knn algorithm to suggest new identities similar to the user to follow them
although they dont generate content. For example an 8tracker that has the same
music taste as the user.

### Network analysis

Only dive to one (or two)? levels into the social hierarchy (fetch following and
followers of who liked the user/collection/playlist/content).

Then apply concepts as ** Eigenvector centrality ** for large networks,
Betweenness Centrality,	Algorithm breadth-first search, Closeness centrality to
deduce important members of the community of those sites and suggest them.

### Hivemind

Ask the hivemind for content based on some query.

### Scrap suggestion web pages

Add information from sites like last.fm or bagmovies.com to the database.

## Download playlist generator algorithm

It will generate a score ordered list of content to download. The scored
download list given by the brain will give the item id, a vector of relative
time curl queries (for example if a playlists has to download 5 songs plus
3 queries to get the information needed we'll have [ 0 0 0 0 300 357 ...] being
the last digits the length to wait between downloads) and the latest download
date of the item. With this information we'll generate a gaussian browsing
profile to hide the user browsing fingerprint.

Depending on the type of subscription of a site, collection...  New content will
be flagged as waiting or pending. Waiting will be very useful when we are
analyzing the social enviroment of a user to discover new content.

To deduce the relative time curl queries vector we'll use:
- A prediction made by the scrapper programmer per
    content/playlist/collection/user.
- The history of previous fetchs.

To deduce the lastest download date of an item we'll use different paths:

### Urgent download

This content will be generated when the user tries to browse something that it's
not in the local cache. The brain will add it's entry with latest download date
== current and launch trigger event on the scheduler.

We expect that this case will not happen often, which will mean that airss is
doing it's job correctly.

### Subscription new content download

This are content that we'll expect to download based on the history of the
sources and the user.

Known source update frequency. We'll only download metadata in this case.

**[NEXT ALGORITHM IS REALLY SIMPLE AND MUST BE IMPROVED, taking into account different periodic trends daily, weekly, montly, each X days, in the morning, in the afternoon...]**

How to treat with outliers:
	* Q1 == 25th percentile
	* Q3 == 75th percentile
	* IQR=Q3-Q1
	* Outlier if:
		* is located 1.5*IQR below Q1
		* is located 1.5*IQR above Q3

### Deduce when the next content might be generated

```
predicted_next_entry_date=minimum squares(last n (published_date_i - published_date_i-1)

if predicted_next_entry_date - last_downloaded_item_date < max_download_frequency
	next_download_date=max_download_frequency
else
	next_download_date=predicted_next_entry_date
fi
```

Note: we'll keep a log of if there is new content, the next download date... to
do debugging.

If the content score is high compared with the cached one of a particular
genre/tag/site download the content else only maintain the metadata.

### User consumption download

The Brain must have the daily expected material consumption saved in the cache
of airss. Till it knows the user better, use a factor of 2 times the day's
expected viewed content, later we can decrease this factor.

For this purpose we can use the algorithm of the last section to predict the
date when the user is going to browse the next content of a subscription or
a search term. Once we have the value, we can extrapolate for 24h and we'll have
the content the user might browse, both the subscription it comes from and the
amount of content. With that information we can deduce the date of content
download of each of the subscriptions or when to update the content of a special
search.

Once an element has been selected to download content, we must first check the
last metadata update of the element against the frequency update to deduce if we
need to update the metadata before choosing what content to download.

We can also set a minimum update frequency so that we are always updated in
a particular subscription although we don't visit it in a regular way.

###	Probable user new search content

Based on the history of the user, both browse and search history we can make
a knn algorithm to predict which are going to be the most probable new searches
and cache them.

### Discover download

The discover algorithm might introduce new content to download to the list.

### Fake traffic ( interesting??? )

We can generate fake traffic, downloads that go to /dev/null so as to hide even
further the user fingerprint in case our architecture of multiple circuits of
tor is compromised...

### Social update algorithm

It may be interesting to download the social metadata of the most liked sources
more than one time so as to add new likely users to connect with (who liked
a playlist or commented).

## Browse playlist generator algorithm

It will generate a list of content to show depending on the browsing mode:

Select the matched content:

* First select the type of content to see/search (article, music, video,
    picture).
* Period of time: Specify the maximum age of the content to be displaied: day,
    week, month, year, 5years, alltime.
* All, seen or unseen: Display only the unseen content (useful for articles), or
    also display the already seen content (useful for music playlists), or
    display only the seen content.
* Source: Select content from one or more of the following sources: subscription
    content, discover content, hivemind content, internet (not processed)
    content.
* Search string: search content based on a string, tag, genre, artist, site,
    site.genre(to group blogs into genres, for example 9gag, xkcd in comedy) or
    all the content.
* Length: The user specifies the amount of time he wants to browse the current
    query.
	* Reviewing the browsing history we can deduce the average amount of time of
        browsing some type of content. Obviously the videos and songs have
        a fixed length, but for the pictures we can have an average browsing
        time for a user, or collection... and predict future ones. For articles,
        number of words, average time of other articles of the same
        author/site...
	* This mode could be used to limit the playlist time, so once the time is
        over, don't show more content, therefore avoiding the internet
        absortion.
	* In case of video or song playlists, the algorithm can priorize videos or
        playlists of the selected length over others.
	* For that each content must have the following field in the database:
        Length: An estimation of length required to view the content (song
        length, article_length/reading_speed).

Order the content: Again with a multiple regression.

This time we wont save the weights or do machine learning on them. The fields are:

* Old/New: Priorize old content before new or the other way around.
* Shuffle: Once the playlist is generated shuffle the content or not.
* Type: There are different normal browsing modes:
	* Popular: Priorize content that is already seen and we know it's good,
        order by `(score of user_view_count*user_score)`.
	* Score: Just take into account the content_score (predicted or user), order
        by content_predicted_score.
	* Forgotten: Priorize content that is good but it's forgotten `(score of
        user_score*(current_date - last_reproduced_date))`.
	* Routine: Take into account the routine browsing profile of the user, and
        we priorize the content of the selected interval, we'll use an algorithm
        like the one described in [User consumption download](### User
        consumption download) only that we use this information to generate an
        order of elements to show and when to show it. Comparing those dates
        with the current time we can know what content to show the user..

## Cleaner algorithm

To clean the old unviewed content and free space. Select a maximum amount of
items or space spent by a subscription. It can be predefined with a default for
each kind of internet source and then run a cron daemon to clean up based on
content score from low to high. Suggesting to increase the maximum amount if
content with high score gets deleted.

## Hivemind algorithm

* Analyze which daemon shared what information.
* If a daemon gives X amount of information that matches the user desires
    propose it to the user through the UI to make him follow it.
* Design the AI to correctly answer the queries of other daemons based on the
    local database and the history of feedback from that daemon and the history
    of already passed contents so as not to repeat.
* It must store the social relationship maintained between the daemons (friends,
    close friends... hivemind groups).
* Calculate deduced scores from data:
	* number of suggestions given to the daemon.
	* number of liked suggestions given to the daemon.
	* number of queries given to that daemon.
	* number of suggestions received from the daemon.
	* number of liked suggestions received from the daemon.
	* Automatic responsive score: if the daemon use to answer us, is online when
        we want to ask it.
	* Automatic similarity score of the daemon.

## Python modules for Data Science

src: Data Science from Scratch: First Principles with Python _-_ Joel Grus

* Statistics: scipy, pandas and statsmodels.
* Probability: scipy.stats contains pdf and cdf functions for most of the
    popular probability distributions.
* Gradient Descend: scikit-learn has a stochastic gradient descent module.
* Working with data: scikit-learn has a wide variety of matrix decomposition
    functions including PCA.
* K-Nearest neighbors: scikit-learn.
* Naive Bayes: scikit-learn BernoulliNB (and others).
* Multiple regression: scikit-learn: LinearRegression, Ridge, Lasso, and others.
* Logistic Regression: scikit-learn for both Logistic regression and support
    vector machines.
* Decision trees: scikit-learn has many it also has an ensemble module that
    includes a RandomForestClassifier as well as other ensemble methods.
* Neural networks (we don't seem to need it): PyBrain (simple), Pylearn2 (more
    advanced and harder).
* Clustering: scikit-learn sklearn.cluster module includes KMeans and Ward
    hierarchical clustering algorithm, scipy has two clustering methods
    scipy.cluster.vq (k-means) and scipy.cluster.hierarchy (variety of
    hierarchical).
* Natural Language processing: Natural Language Toolkit www.nltk.org.
* Stemmers: The names of contents, tags, genres is probable that is similar but
    not identical, therefore we'll have separated information for songs tagged
    as celtic and Celtic. [Homepage](http://snowball.tartarus.org).
* Network Analysis: networkX and Gephi.

## Research

* Extract topic from article: Latent Dirichlet allocation
	Python: gensim
	www.radimrehurek.com/gensim

* Recommender systems
	Python: Crab, Graphlab
	- What's popular
	- User-based collaborative filtering
	- Item-based collaborative filtering

* MapReduce
	Python: mrjob python package for interfacing with Hadoop
	Tools: Hadoop, Spark and Storm

