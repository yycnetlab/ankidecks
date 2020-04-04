#!/bin/bash
# This is a sample add script for when you are adding a whole bunch of cards.

NOTE=$1

cd /Users/kelvintran/GithubRepos/yycnetlabs-anki/tools
BASEPATH="/Users/kelvintran/GithubRepos/yycnetlabs-anki/CCNP-Ent_v8"
DECK="CCNP-ENCOR_v8.json"

MISSINGFIELDS=$(/usr/bin/grep -c -e '\"\"' ${BASEPATH}/${NOTE})

if [ ${MISSINGFIELDS} -ne 0 ]; then
  echo "ERROR: ${BASEPATH}/${NOTE} is missing these non-optional fields:"
  /usr/bin/grep -e '\"\"' ${BASEPATH}/${NOTE}
  exit 1
fi

ruby add_note.rb -f ${BASEPATH}/${DECK} -n ${BASEPATH}/${NOTE}

if [ "$?" -eq 0 ]; then
  /usr/bin/sed -i -e 's/\(\(front\|back\).*":"\)[^"]*\("\)/\1\3/' ${BASEPATH}/${NOTE}
fi

