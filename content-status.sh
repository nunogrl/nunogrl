#!/bin/sh

find content | egrep -i  "md|rst" |\
  while read post ; do
    printf "$post "
    grep -i Status: $post
  done | sort |  awk '{print $1" "$3 }' | column -t

