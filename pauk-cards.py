#!/usr/bin/python
#
# Pauk-Card
#
# Convert a CSV file to pauker xml
# See http://pauker.sf.net/
#
# Coded by Bastian Ballmann
# http://www.datenterrorist.de
#
# License GPLv3

import sys
import csv
import gzip
import codecs

if len(sys.argv) == 1:
    print sys.argv[0] + ": <file>"
    sys.exit(0)

try:
    vocabulary = csv.reader(codecs.EncodedFile(open(sys.argv[1], "rb"), "utf-8"),
                            delimiter=";")
except IOError, e:
    print "Cannot read file " + sys.argv[1]
    print str(e)
    sys.exit(1)
except UnicodeDecodeError:
    print "The csv file must be encoded in utf-8"
    print "You can use a tool like iconv or a text editor to recode it"
    sys.exit(1)

out_file = sys.argv[1]
out_file = out_file.replace(".csv", ".pau.gz")

try:
    out = gzip.open(out_file, "w")
except IOError, e:
    print "Cannot write file " + out_file
    print str(e)
    sys.exit(1)

out.write("""<?xml version="1.0" encoding="UTF-8"?>
<!--This is a lesson file for Pauker (http://pauker.sourceforge.net)-->
<Lesson LessonFormat="1.7">""")
out.write("<Description>Lesson " + sys.argv[1] + "</Description>\n")
out.write("<Batch>\n")

for row in vocabulary:
    left = row[0]
    right = row[1].strip("\n")

    # left to right
    out.write("""<Card>
      <FrontSide Orientation="LTR" RepeatByTyping="false">""")
    out.write("<Text>" + left + "</Text>\n")
    out.write("""<Font Background="-1" Bold="false" Family="Dialog" Foreground="-13421773" Italic="false" Size="18"/>
      </FrontSide>
      <ReverseSide Orientation="LTR" RepeatByTyping="false">""")
    out.write("<Text>" + right + "</Text>\n")
    out.write("""<Font Background="-1" Bold="false" Family="Dialog" Foreground="-13421773" Italic="false" Size="18"/>
      </ReverseSide>
    </Card>""")

    # right to left
    out.write("""<Card>
      <FrontSide Orientation="LTR" RepeatByTyping="false">""")
    out.write("<Text>" + right + "</Text>\n")
    out.write("""<Font Background="-1" Bold="false" Family="Dialog" Foreground="-13421773" Italic="false" Size="18"/>
      </FrontSide>
      <ReverseSide Orientation="LTR" RepeatByTyping="false">""")
    out.write("<Text>" + left + "</Text>\n")
    out.write("""<Font Background="-1" Bold="false" Family="Dialog" Foreground="-13421773" Italic="false" Size="18"/>
      </ReverseSide>
    </Card>""")

out.write(""" </Batch>
  <Batch/>
  <Batch/>
</Lesson>
""")
out.close()

print "Wrote file " + out_file
