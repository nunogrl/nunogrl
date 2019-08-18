#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nuno Leitao'
SITENAME = u'nunogrl.com'
SITEURL = ''
PATH = 'content'
# DEFAULT_CATEGORY = 'personal'

ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'


TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'
#####################

# all defaults to True.
DISPLAY_HEADER = True
DISPLAY_FOOTER = True
DISPLAY_HOME   = True
DISPLAY_MENU   = True


MENU_ITEMS = True
# DISPLAY_PAGES_ON_MENU = True
# DISPLAY_CATEGORIES_ON_MENU = True
USE_FOLDER_AS_CATEGORY = False


DISPLAY_CATEGORIES_ON_MENU = False
# DISPLAY_PAGES_ON_MENU = False

DISPLAY_PAGES_ON_MENU = False
PAGE_PATHS = ['pages']
PAGE_URL = 'pages/{slug}.html'
PAGE_LANG_URL = 'pages/{slug}-{lang}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}.html'

# PATH = 'content'
# ARTICLE_PATHS = ['blog']
# ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
# ARTICLE_URL = '{date:%Y}/{slug}.html'
# SHOW_FULL_ARTICLE = True

MENUITEMS = (
    ('About', '/pages/about.html'),
    ('Devops', '/category/devops.html'),
    ('Electronics', '/category/electronics.html')
    # ('Music', '/category/music.html'),
    # ('Photo', '/category/photo.html')
    # ('Electronics', 'http://www.google.com/recaptcha/mailhide/d?...'),
    # ('Vita', '/pdfs/HouserCV.pdf')
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('My Shaarli', 'http://bookmarks.barbearclassico/'))

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

THEME = "themes/pelican-clean-blog"
# THEME = "themes/bricks"
# THEME = "themes/blue-penguin"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
