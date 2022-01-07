#!/bin/sh

# pelican content --debug 1>/dev/null 2>&1 #| grep -i warning
pelican content --debug  2>&1 | egrep -i "error|warn"

# Verify contents
grep -P "^:[a-zA-Z0-9]+:" content/*.rst
