#!/usr/bin/env python
"""Main Image Semgentation testing program
 Requires: argument one is operation type:
               seg for segmentation
               fit for fitness function
          -seg requires arguments in order:
               filename, red min + max, green min + max, blue min + max
          -fit requires arguments in order:
               generated mask, ideal mask
 Effects:  Runs segmentation tool as specified:
          -seg outputs output.png of background (black) and 
           foreground (white) which depend on parameters passed
          -fit outputs the difference in # of black/white pixels
           between a generated mask and an ideal mask
"""

import sys # for argv
import segmentation
import fitness

def main():

    try:
        if sys.argv[1] == "seg":
            segmentation.runSegmenter(sys.argv[2], map(int, sys.argv[3:]))
        
        elif sys.argv[1] == "fit":
            fitness.runFitness(sys.argv[2], sys.argv[3])
        
        else:
            print "No valid tool specified"
            print __doc__
        
    except:
        print __doc__

main()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4