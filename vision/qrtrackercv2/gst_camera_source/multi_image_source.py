#!/usr/bin/env python
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

import Image
import imagesrc
import fnmatch
import os

class multiimagesrc(imagesrc.imagesrc):
    filenames = None
    def __init__ (self, files):
        self.filenames = files
        # path, regex = os.path.split(files)
        # for f in os.listdir(path):
        print self.filenames
        self.index = 0

    def get_image(self):
        print "image", self.index, ":", self.filenames[self.index]
        im = Image.open(self.filenames[self.index])
        self.index+=1
        return im

    def has_data(self):
        if self.index>=len(self.filenames):
            return False
        return True
