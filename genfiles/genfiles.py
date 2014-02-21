#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys


FILE_PREFIX = ''
# number of zeros to fill (string.zfill)
NUM_ZEROS = 24

class GenFiles:
    """ generates postgresql write ahead logs' filenames """
    # set to 0 to stop the generator
    cont = 1

    def do_generate(self, prefix, beg, end):
        """ yields generated filename values starting from beg (decimal) value and finishing at end+1 (decimal) """
        # range actually works with hex arguments too (tested in 2.7) so we might not even need the parse_args function
        for f in range(beg, end+1):
            # continue generating ?
            if self.cont == 0:
                print "DEBUG    stop requested, stopping generator"
                self.toggle_generate()
                break
            # convert back to hex (uppercase), strip off the 0x in the beginning, and fill with zeroes
            yield prefix + str(hex(f)[2:]).upper().zfill(NUM_ZEROS)

    def toggle_generate():
        """ toggles the switch to allow/stop the generator """
        self.cont = 0 if self.cont == 1 else 1

    def parse_args(self, argv):
        """ extracts beginning and end decimal values from prefixed filenames in sys.argv"""
        # sort of deprecated .. 
        beg = argv[1][len(FILE_PREFIX):]
        end = argv[2][len(FILE_PREFIX):]
        # convert from hexadecimal to decimal
        beg = int(beg, 16)
        end = int(end, 16)
        print "DEBUG    total to be generated: %s" % (abs(beg-end)+1)
        if beg > end:
            return end, beg
        else:
            return beg, end

def usage():
    print " " 
    print " %s <start> <finish>" % sys.argv[0]
    print " " 
    if FILE_PREFIX:
        print "      prefix: \'%s\'" % str(FILE_PREFIX)
    print "         <start>,<finish>     start and finish (hex) padded to %s (NUM_ZEROS)" % NUM_ZEROS
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        # could add a conversion test here..
        usage()
    # this is not necessarily needed anymore but we may improve/use it later...
    if sys.argv[1].find(FILE_PREFIX) != 0 or sys.argv[2].find(FILE_PREFIX) != 0:
        print "DEBUG    expecting to start with %s" % FILE_PREFIX
    myGen = GenFiles()
    beg, end = myGen.parse_args(sys.argv)
    for f in myGen.do_generate(FILE_PREFIX, beg, end):
        print f


if __name__ == '__main__':
    main()
