#!/bin/bash

usage(){
cat << EOF
Usage: $0 [OPTION...] [content] 

Examples:
  $0 -a "This is a new Article" -t "music, lifestyle" -c "personal"  

Switches:

  -a                         Article title (MANDATORY)
  -c                         Category
  -t                         Tags
  -h                         Shows this help
EOF
}

if [ $# -lt 1 ]; then
    usage
    exit 1
fi

while getopts 'a:t:c:h' OPTION
do
  case $OPTION in
    a) article_title="${OPTARG}"
       ;;
    c) category="${OPTARG}";;
    t) tags="${OPTARG}";;
    h) usage
       exit 0
       ;;
    *) usage
       exit 2
       ;;
  esac
done


if [ -z "${article_title:-}" ] ; then
    usage
    exit 0
fi

article_slug=$(echo "${article_title}" | sed 's/ /-/g' | tr "[:upper:]" "[:lower:]" )
article_file="content/${article_slug}.rst"

if [ -f "${article_file}" ] ; then
    echo "⛔ Article ${article_file} already exists"
    echo "Giving up"
    exit 1
fi

titlehr=""
while IFS= read -r _; do
    titlehr="${titlehr}#"
done < <(seq 1 ${#article_title})

cat << EOF > "${article_file}"
${article_title}
${titlehr}

:Date: $(date +"%Y-%m-%d %H:00:00 +0100")
:Category: ${category:-}
:Tags: ${tags:-}
:Authors: Nuno Leitao
:Slug: ${article_slug}
:Summary: ${article_slug}
EOF

if [ -f "${article_file}" ] ; then
    echo "🙌 Created ${article_file}"
else
    echo "⚠️  Failed to create ${article_file}"
fi
