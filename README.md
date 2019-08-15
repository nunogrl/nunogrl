# Website with Pelican

## Organization

    .
    ├── buildsite.sh
    ├── content
    │   └── (...)
    ├── develop_server.sh
    ├── output
    │   └── (...)
    ├── pelicanconf.py
    ├── pelicanconf.pyc
    └── publishconf.py



## Pre-flight

    mkdir pelican
    virtualenv  pelican
    source pelican/bin/activate
    pip install pelican
    pip install Markdown
    
## Build the site

    pelican -s pelicanconf.py -o output content

or:

    sh buildsite.sh


## Test the site

    cd output/
    python -m SimpleHTTPServer

Go to [http://localhost:8000](http://localhost:8000)

## Deploy

scp -r output root@oxygene.barbearclassico.com:/srv/.

# Site planning

    .
    ├── about - footprints.jpg
    │   ├── about.md
    │   ├── bio.md
    │   └── cv.md
    ├── projects - planning
    │   ├── cgit.md
    │   ├── bookmarks.md
    │   ├── ansible.md    
    │   └── cicd.md
    ├── devops - itil
    │   ├── ansible.md
    │   ├── aws.md
    │   ├── barbearclassico.md
    │   ├── devops.md
    │   ├── gpg.md
    │   ├── nci.md
    │   ├── pelican.md
    │   └── runit.md
    ├── interests - 
    │   ├── hiking
    │   ├── raspberry
    │   ├── wetshaving
    │   ├── hiking
    │   ├── hiking
    │   └── music
    └── README.md

