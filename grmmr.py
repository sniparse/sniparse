#!/usr/bin/env python

import sqlite3
# grammatic data
dbm = sqlite3.connect('/usr/share/sniparse/ifs/gramm.db')
curs = dbm.cursor()
print 'connet'
curs.execute("select Verbs from English")
verbs = curs.fetchall()
curs.execute("select Nouns from English")
nouns = curs.fetchall()
curs.execute("select Pronouns from English")
pronouns = curs.fetchall()
curs.execute("select Adjetives from English")
adjetives = curs.fetchall()
curs.execute("select Adverbs from English")
adverbs = curs.fetchall()
curs.execute("select Prepositions from English")
prepositions = curs.fetchall()
dbm.close()





