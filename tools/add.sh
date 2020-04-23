#!/bin/bash
# This is a sample add script for when you are adding a whole bunch of cards.

NOTE=$1

cd ~/repos/ankidecks/tools
BASEPATH="/home/tpb/repos/ankidecks/Canadian_Ham_Advanced"
DECK="Canadian_Ham_Advanced.json"

MISSINGFIELDS=$(/bin/grep -c -e '\"\"' ${BASEPATH}/${NOTE})

if [ ${MISSINGFIELDS} -ne 0 ]; then
  echo "ERROR: ${BASEPATH}/${NOTE} is missing these non-optional fields:"
  /bin/grep -e '\"\"' ${BASEPATH}/${NOTE}
  exit 1
fi

ruby add_note.rb -f ${BASEPATH}/${DECK} -n ${BASEPATH}/${NOTE}

if [ "$?" -eq 0 ]; then
  /bin/sed -i -e 's/\(\(front\|back\).*":"\)[^"]*\("\)/\1\3/' ${BASEPATH}/${NOTE}
fi
