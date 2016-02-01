"""
This example shows how to filter and modify tags and write the rusults back.
It changes all tag values 'yes/no' to '1/0'.
"""

import osmium as o
import sys

class BoolNormalizer(o.SimpleHandler):

    def __init__(self, writer):
        o.SimpleHandler.__init__(self)
        self.writer = writer

    def normalize(self, o):
        # if there are no tags we are done
        if len(o.tags) == 0:
            return o

        newtags = {}
        # pyosmium is much faster writing an original osmium object than
        # a osmium.mutable.*. Therefore, keep track if the tags list was
        # actually changed.
        modified = False
        for t in o.tags:
            if t.v == 'yes':
                newtags[t.k] = '1'
                modified = True
            elif t.v == 'no':
                newtags[t.k] = '0'
                modified = True
            else:
                newtags[t.k] = t.v

        if modified:
            # We have changed tags. Create a new object as a copy of the
            # original one with the tag list replaced.
            return o.replace(tags=newtags)
        else:
            # Nothing changed, so simply return the original object
            # and discard the tag list we just created.
            return o

    def node(self, o):
        self.writer.add_node(self.normalize(o))

    def way(self, o):
        self.writer.add_way(self.normalize(o))

    def relation(self, o):
        self.writer.add_relation(self.normalize(o))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python normalize_boolean.py <infile> <outfile>")
        sys.exit(-1)


    writer = o.SimpleWriter(sys.argv[2])
    BoolNormalizer(writer).apply_file(sys.argv[1])

    writer.close()