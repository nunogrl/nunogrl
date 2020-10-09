#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nuno Leitao'
SITENAME = u'nunogrl.com'
SITEURL = 'https://www.nunogrl.com'
PATH = 'content'
DEBUG = True

# DEFAULT_CATEGORY = 'personal'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

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
FEED_ALL_ATOM = 'atom.xml'
TAG_FEED_ATOM = 'categories/{slug}/atom.xml'
CATEGORY_FEED_ATOM = "category/{slug}/atom.xml"
TRANSLATION_FEED_ATOM = None
DISPLAY_FEEDS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = False

RELATED_POSTS_MAX = 10

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.do']}

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = CATEGORY_URL + 'index.html'

TAG_URL = 'categories/{slug}/'
TAG_SAVE_AS = TAG_URL + 'index.html'

ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = ARCHIVES_URL + 'index.html'

AUTHOR_URL = 'authors/{slug}/'
AUTHOR_SAVE_AS = AUTHOR_URL + 'index.html'

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ['related_posts', 'series', 'sitemap', 'tag_cloud', 'assets', 'share_post']

SITEMAP = {
    'format': 'xml',
}

DEFAULT_DATE_FORMAT = '%d/%m/%Y'

SOCIAL = (
    ('Twitter', 'https://twitter.com/nunogrl'),
    ('GitHub', 'https://github.com/nunogrl'),
)

DEFAULT_PAGINATION = 9
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

STATIC_PATHS = [
    'images',
    'code',
    'notebooks',
    'files',
    'extra/CNAME',
    'extra/robots.txt'
]
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

TWITTER_USERNAME = 'nunogrl'

THEME = "themes/editorial"

FAVICON = 'images/global/favicon.jpg'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'permalink': True
        },
        'mdx_video': {},
    },
    'output_format': 'html5',
}

QUOTES = [
    {
        'quote': "Roads? Where we're going, we don't need... roads.",
        'source': 'Back to the Future, 1985'
    },
]


# THEME = "themes/bricks"
# THEME = "themes/blue-penguin"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
