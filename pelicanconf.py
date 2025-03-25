#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nuno Leitao'
SITENAME = u'nunogrl.com'
SITEURL = 'https://www.nunogrl.com'
PATH = 'content'
DEBUG = True

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'
ARTICLE_TRANSLATION_ID = 'slug'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'atom.xml'
TAG_FEED_ATOM = 'categories/{slug}/atom.xml'
CATEGORY_FEED_ATOM = "category/{slug}/atom.xml"
TRANSLATION_FEED_ATOM = None
DISPLAY_FEEDS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = False

RELATED_POSTS_MAX = 10

# JINJA_ENVIRONMENT = {
#        'extensions': ['jinja2.ext.with_', 'jinja2.ext.do']}

ARTICLE_URL = 'articles/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = CATEGORY_URL + 'index.html'

TAG_URL = 'categories/{slug}/'
TAG_SAVE_AS = TAG_URL + 'index.html'

ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = ARCHIVES_URL + 'index.html'

AUTHOR_URL = 'authors/{slug}/'
AUTHOR_SAVE_AS = AUTHOR_URL + 'index.html'

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = [
     'related_posts',
     'series',
     'sitemap',
     'tag_cloud',
     'assets',
     'share_post',
     'search',
     'code_include',
     'mermaid-include'
]

SEARCH_MODE = "output"
SEARCH_HTML_SELECTOR = "main"

SITEMAP = {
    'format': 'xml',
}

DEFAULT_DATE_FORMAT = '%d/%m/%Y'

# The default metadata you want to use for all articles and pages.
DEFAULT_METADATA = {
  'status': 'draft',
  'opengraph_image': 'githorrorstory/githorrorstory.jpg'
}


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
    'extra/robots.txt',
    'extra/headers'
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/headers': {'path': '_headers'},
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

# EXTRACOPYRIGHT = ''

#CATEGORIES = [
#    {
#        'title': "Electronics",
#        'href': "/category/electronics/",
#        'icon': "icon fa-microchip",
#        'description': "Articles on DIY projects on electronics"
#
#        },
#    {
#        'title': "DevOps",
#        'href': "/category/devops/",
#        'icon': "icon fa-robot",
#        'description': "Articles on articles on DevOps"
#
#        },
#    {
#        'title': "hiking",
#        'href': "/category/hiking/",
#        'icon': "icon fa-walking",
#        'description': "Articles and maps on hiking"
#        },
#    ]
#TOPSERIES = [
#     {
#         'title': "GPG usages",
#         'href': "/blog/2019/08/30/the-perfect-gpg-key/",
#         'image': "/images/gpg-series.png",
#         'alt': "GPG",
#         'description':
#             "A series of posts with examples on GPG creation and usage, for"
#             " simple password maintaining, password sharing, authentication"
#             " and signing."
#         },
#     {
#         'href': "/blog/2017/05/09/a-game-of-tokens-write-an-interpreter-in-python-with-tdd-part-1/",
#         'image': "/images/a-game-of-tokens-1.jpg",
#         'alt': "A Game of Tokens",
#         'title': "A game of tokens",
#         'description': "Python, Ruby, Javascript, C, Erlang, how many different"
#             " languages. But how does a compiler work? How si the source code"
#             " converted into something that works? Let's write a simple language"
#             " interpreter using TDD!"
#         },
#     {
#         'title': "Exploring the Amiga",
#         'href': "/blog/2018/05/28/exploring-the-amiga-1/",
#         'image': "/images/exploring-the-amiga-1.jpg",
#         'alt': "Exploring the Amiga",
#         'description': "Is it worth unearthing old architectures? Is it"
#             " worth understanding how a computer system from the 80s worked?"
#             " I believe old architectures can teach us a lot, so let's explore"
#             " \"the computer that wouldn’t die\"!"
#         },
#]
# 
# MYVIDEOS = [
#     {
#         'href': "https://www.youtube.com/playlist?list=PLWtCrYLGt7T2REIrEcpGY6nT2t7Wcoj-m",
#         'image': "/images/video-tdd-in-python-with-pytest.jpg",
#         'alt': "TDD in Python with pytest (playlist)",
#         'title': "TDD in Python with pytest (playlist)",
#         'description': "I recorded my successful workshop \"TDD in Python with"
#             " pytest\" and produced my first series of videos, for a grand total"
#             " of 2 hours of hands-on tutorial on Test-Driven Development in Python."
#     },
#     {
#         'href': "https://www.youtube.com/playlist?list=PLWtCrYLGt7T3DUFPYdqrdEqzt-OCfBQ5O",
#         'image': "/images/video-object-oriented-programming-in-python.jpg",
#         'alt': "Object-oriented programming in Python (playlist)",
#         'title': "Object-oriented programming in Python (playlist)",
#         'description': "A journey into the Python implementation of the Object-oriented"
#             " paradigm, specifically tailored for beginner programmers."
#     },
# ]

QUOTES = [
    {
        'quote': "If I have seen further it is by standing on the shoulders of"
            " Giants",
        'source': "Isaac Newton"
    },
    {
        'quote': "We are like dwarfs on the shoulders of giants, so that we can"
            " see more than they, and things at a greater distance, not by"
            " virtue of any sharpness of sight on our part, or any physical"
            " distinction, but because we are carried high and raised up by"
            " their giant size.",
        'source': "Bernard De Chartres"
    },
]
