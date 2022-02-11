---
title: Downloader
date: 20200410
author: Lyz
---

Python program to obtain the metadata and content from the sites populating the
database.

The idea is to have a centralized scheduler that triggers celery jobs to be
consumed by worker processes. We'd have different worker processes for
each data source, so it should be easy to support new sites.

# Requirements

* It must download the metadata and content to the [database|filesystem].
* All the user information must remain local.
* It must preserve the anonymity of the user as much as possible.
* It must store all the metadata needed by the other programs in the database.

# Extractors

Extractors are programs that transform the source data into SQLAlchemy
objects defined in the [models]() schema.

They must have at least these principal methods:

* *create_source*: Parse url content to add the source information in the database.
* *extract*: Parse the url content to add the source content in the database.

## Article extraction

We could use one of the following libraries:

* [news-please](https://github.com/fhamborg/news-please)
* [newspaper](https://github.com/codelucas/newspaper)
* [python-readability](https://github.com/buriy/python-readability)

# API endpoints

| Method | Endpoint      | Auth? | Returns                                |
| ---    | ---           | ---   | ---                                    |
| POST    | /api/metadata | no    | If the job has been added to the queue |
| POST    | /api/content  | no    | If the job has been added to the queue |
| GET    | /metrics      | no    | microservice metrics                   |
