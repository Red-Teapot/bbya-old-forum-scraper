# Old BByaWorld forum scraper

This is a scraper built to collect user info, forums, topics and posts from http://mc.bbcity.ru

Here is a list of what is collected:

Users:
 - ID
 - Nickname
 - Registration date
 - Avatar URL
 - Avatar image (the file itself as a blob)

Sections (forum groups on the main page):
 - ID
 - Title

Forums:
 - ID
 - Title
 - Corresponding section ID

Topics:
 - ID
 - Title
 - Corresponding forum ID

Posts:
 - ID
 - Publication date
 - Author ID
 - Corresponding topic ID
 - Message (HTML as is)
 - Post number in the topic

## Setup

Just install dependencies from `requirements.txt`, e.g. with `pip install -r requirements.txt`

## How to run

The project contains two spiders: `users` spider and `forums` spider. Users spider has to be run first.

So, if you want to run it manually, you should first run `scrapy crawl users`, then `scrapy run forums`
