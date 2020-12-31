#!/bin/sh

pelican content --debug 1>/dev/null 2>&1 | grep -i warning
