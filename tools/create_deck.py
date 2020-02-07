#!/usr/bin/python

import uuid
import os
import sys
import textwrap

# Steps:
# - get name of deck
# - replace spaces with underscores/dashes
# - create the directory
# - Incrememt the Deck ID file
# - Build the template with a new GUID
# - Put card #1 into the file

DeckFileName='_'.join(sys.argv[1:])
DeckName=' '.join(sys.argv[1:])

# Create the directory for the deck
try:
    os.mkdir(DeckFileName)
except OSError:
    print ("Unable to create directory: %s" % DeckFileName)
    exit(1)

# Determine a unique number to insert into to faux GUID for the deck:
GuidSetsFile=open("tools/guid-sets.list", 'r')
GuidLines=GuidSetsFile.read().splitlines()
LastGuidSet=int(GuidLines[-1].split('-')[0])
GuidSetsFile.close()

NextGuidSet="%02d" % (LastGuidSet+1)

GuidSetsFile=open("tools/guid-sets.list", 'a')
GuidSetsFile.write("%s-%s\n" % (NextGuidSet,DeckName))
GuidSetsFile.close()

DeckUUID=str(uuid.uuid4())

BaseJSON=textwrap.dedent("""\
        {
            "__type__": "Deck",
            "children": [],
            "crowdanki_uuid": "%s",
            "deck_config_uuid": "%s",
            "deck_configurations": [
              {
                "__type__": "DeckConfig",
                "autoplay": true,
                "crowdanki_uuid": "%s",
                "dyn": false,
                "lapse": {
                  "delays": [
                    10
                  ],
                  "leechAction": 0,
                  "leechFails": 8,
                  "minInt": 1,
                  "mult": 0.0
                },
                "maxTaken": 60,
                "name": "Default",
                "new": {
                  "bury": true,
                  "delays": [
                    1,
                    10
                  ],
                  "initialFactor": 2500,
                  "ints": [
                    1,
                    4,
                    7
                  ],
                  "order": 1,
                  "perDay": 20,
                  "separate": true
                },
                "replayq": true,
                "rev": {
                  "bury": true,
                  "ease4": 1.3,
                  "fuzz": 0.05,
                  "ivlFct": 1.0,
                  "maxIvl": 36500,
                  "minSpace": 1,
                  "perDay": 100
                },
                "timer": 0
              }
        ],
        "desc": "",
        "dyn": 0,
        "extendNew": 10,
        "extendRev": 50,
        "media_files": [],
        "mid": "1496861969393",
        "name": "%s",
        "note_models": [
            {
              "__type__": "NoteModel",
              "crowdanki_uuid": "bfa36940-2042-11e9-8b6a-acbc3287506b",
              "css": ".card {\\n font-family: arial;\\n font-size: 20px;\\n text-align: center;\\n color: black;\\n background-color: white;\\n}\\n",
                   "flds": [
                {
                  "font": "Arial",
                  "media": [

                  ],
                  "name": "Front",
                  "ord": 0,
                  "rtl": false,
                  "size": 20,
                  "sticky": false
                },
                       {
                  "font": "Arial",
                  "media": [

                  ],
                  "name": "Back",
                  "ord": 1,
                  "rtl": false,
                  "size": 20,
                  "sticky": false
                },
                {
                  "font": "Arial",
                  "media": [

                  ],
                  "name": "RerverseCardID",
                  "ord": 2,
                  "rtl": false,
                  "size": 20,
                  "sticky": false
                },
                {
                  "font": "Arial",
                  "media": [

                  ],
                  "name": "Reference",
                  "ord": 3,
                  "rtl": false,
                  "size": 20,
                  "sticky": false
                }
              ],
              "latexPost": "\\\\end{document}",
              "latexPre": "\\\\documentclass[12pt]{article}\\n\\\\special{papersize=3in,5in}\\n\\\\usepackage[utf8]{inputenc}\\n\\\\usepackage{amssymb,amsmath}\\n\\\\pagestyle{empty}\\n\\\\setlength{\\\\parindent}{0in}\\n\\\\begin{document}\\n",
              "name": "Basic",
              "req": [
                [
                  0,
                  "all",
                  [
                    0
                  ]
                ]
              ],
              "sortf": 0,
              "tags": [

              ],
              "tmpls": [
                {
                  "afmt": "{{FrontSide}}\\n\\n<hr id=answer>\\n\\n{{Back}}\\n\\n<br/><br/>\\nSee: <br/>{{Reference}}",
                  "bafmt": "",
                  "bqfmt": "",
                  "did": null,
                  "name": "Card 1",
                  "ord": 0,
                  "qfmt": "{{Front}}"
                }
              ],
              "type": 0,
              "vers": [

              ]
            }
          ],
          "notes": [
            {
              "__type__": "Note",
              "data": "",
              "fields": [
                "Do you know where this Anki deck originated?",
                "This deck is part of an open collaborative effort started by YYC Net Lab.  This deck is provided free of charge and without warranty.  For updates please see the link below.  If you notice any errors or would like to add some cards please reach out to YYC Net Lab through Github.<br><br>To stop seeing this card click on 'More' in the bottom right and select 'Suspend Card'.",
                "610%s00000",
                "https://github.com/yycnetlab/ankidecks"
              ],
              "flags": 0,
              "guid": "610%s00000",
              "note_model_uuid": "bfa36940-2042-11e9-8b6a-acbc3287506b",
              "tags": [

              ]
            }
          ]
        }
        """ % ( DeckUUID, DeckUUID, DeckUUID, DeckName, NextGuidSet, NextGuidSet))

FileHandle = open("%s/%s.json" % (DeckFileName, DeckFileName), "w")
FileHandle.write(BaseJSON)
FileHandle.close()
