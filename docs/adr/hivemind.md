# Hivemind

Python daemon to give/fetch information to/from other Airss hivemind daemons.

The idea is to create a cloud of airss daemons sharing information so as to
improve the browsing experience of the users through discovering new
content/playlists/collections applying data analysis.

## Requirements
* It must preserve the anonymity of the user.
	* Mustn't reveal the clients IP address.
	* Must be distributed/federated.
	* Must be encrypted.
	* Must not depend on any kind of tracker. All the user information must
        remain local. There won't exist a tracker with the information of every
        daemon. The daemon asks to another daemon p2p or asks in a general chat
        room, and then those daemons choose based on their configuration and
        relative social status to answer or not through an private p2p encrypted
        chat.
* The user must decide what to share and with whom.
* The daemon must keep memory of its interactions with the other daemons.
* Once a daemon shares content with our daemon, it must be an option to give
    feedback to that daemon so as to improve future responses, depending on the
    privacy relation between those daemons.
* The interaction with the daemon must be transparent to the user.

## Workflow

The daemon is started when the server is started, joins the jabber chatrooms and
waits to be asked by the user or the other daemons. Once this happens it does
the selected action, updates the ddbb and waits for next action.

## Interfaces

* Get
	* Information from the database.
	* Queries from the user through UI.
	* Queries from other hivemind daemons.
* Put
	* Information to the hivemind based on those queries.
	* Information of the queries results to the database.

## Communication protocol design

Use jabber clients

* Mustn't reveal the clients IP address: each daemon contacts to its jabber
    server so it doesn't show its IP to the other daemons.
* Must be distributed/federated: jabber is federated.
* Must be encrypted: It is known that the conversations in the chat rooms are
    not encrypted but the p2p communication should be under OTR.
* Must not depend on any kind of tracker: The daemons join a common predefined
    chat room, whoever is there benefits from the hivemind. A daemon asks in the
    chat room and the daemons that want to answer him do it through an OTR p2p
    encrypted chat.
* Must be robust: Each daemon should have two or three jabber accounts in
    different servers, there should exist several predefined chat rooms, and
    there should exist predefined pad urls where to share newly created chat
    rooms in case everything goes wrong, if that also goes wrong, well just wait
    till the apocalypse is over..

## Social protocol

Daemon Database

* There must exist predefined groups of users, such as: friends (share some
    information), very close friends (share more information), soul mates (share
    all!), unknown people (share only content).
* The daemon could have a presentation card, such as, daemon name, number of
    queries, number of suggestions, number of good suggestions (based on the
    feedback).
* There must exist an entry of daemons inside the database, with the following
    data.
	* Daemon name.
	* User name associated to the daemon.
	* Daemon relation between hims/hers daemon and ours.
	* Log all of the daemon interactions (see brain for more details). Both the
        answers to our daemon questions and the questions it proposes to our
        daemon. Also store the feedback given by their daemon to our
        suggestions.

## User interaction with the daemon

* The user through UI (search people, manage contacts, manage groups) chooses
    whom to follow and manage groups.
* The user through configuration file (that can be modified through UI) chooses
    what to share (only content, content with some metadata, content with lot of
    metadata).
* The user should have the choice once it makes a search query through the UI to
    ask only the local database, the local database + close friends daemons, the
    local database + close friends + friends, the local database + close friends
    + friends + unknown.
