#!/bin/sh

# Fix pip for GAE.
# http://stackoverflow.com/questions/24257803/distutilsoptionerror-must-supply-either-home-or-prefix-exec-prefix-not-both
echo '[install]\nprefix=' >  ~/.pydistutils.cfg

sudo pip install -t lib --upgrade -r requirements.txt
