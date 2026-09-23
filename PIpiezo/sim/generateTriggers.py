#!/bin/env dls-python

for row in range(10): 
    print "TWS",
    for col in range(10):
        print "1 %4d 1" % (200*row + 20 * col + 20),
    print
    