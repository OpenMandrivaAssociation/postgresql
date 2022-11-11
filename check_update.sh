#!/bin/sh
git ls-remote --tags https://git.postgresql.org/git/postgresql.git |sed -e 's,.*refs/tags/,,' |grep ^REL_ |grep -vE '(ALPHA|BETA|RC)' |sed -e 's,^REL_,,;s,_,.,g' |sort -V |tail -n1
