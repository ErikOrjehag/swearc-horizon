#!/usr/bin/env python
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

import Image
#import cv
import sys
sys.path.append("./gst_camera_source")

from multi_image_source import multiimagesrc
import tracker

import time

usage = \
"""usage: qrtracker -d <device> -wh <size> -h\n
     -d   : <device> can be e.g. /dev/video0\n
     -wh  : <size> size of captured video frame in form AxB, for example: -wh 640x480\n
     -h   : run headless, dump track in the end
     -s   :
"""

def parse_options(argv, expected_options):
    print "parsing options"
    opt = None
    for o in argv:
        print o
        if o[0] == "-":
            if o in expected_options:
                opt = o
                expected_options[opt] = True
        elif opt:
            expected_options[opt] = o
            opt = None


#def process_pygame_events():
#    for event in pygame.event.get():
#        if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
#            if (event.key == pygame.K_ESCAPE):
#                return True
#    return False


def loop(track, headless, ss, size):
    done = False
    ctr = 0
    time_start = time.time()
    frame_counter = 0
    same = 0
    last_text = ""
    while not done:
        #if not headless:
        #    done = process_pygame_events()
        if ss:
            ss.step()

        if src.has_data():
            cv_im = src.get_image()

            out_im, labels, text_data, x, y, w, h = tracker.tracker_scan(cv_im, headless)
            if not headless:
                data = out_im.tostring()
                mode = out_im.mode
                size = out_im.size
                img = pygame.image.fromstring (data, size, mode)
                screen.blit(img, (0,0))
                screen.blit(img, (0,0))
                pygame.display.flip()

            #for k,v in labels.iteritems():
            #    if ss:
            #        ms = float(max(size))
            #        ss.push_data((k, v[0]/ms, v[1]/ms, v[2]))
            #    if k not in track:
            #        track[k] = []
            #    track[k].append((ctr, v))
            #ctr+=1
            #if ctr%100 == 0: # dump tracks every 100 increments of ctr or at least try to
            #    track={}

            time_now = time.time()
            frame_counter += 1
            dt = time_now - time_start

            if (time_now - time_start) >= 0.1:
                if last_text == "":
                   last_text = text_data
                elif text_data == last_text:
                    last_text = text_data
                    same += 1
                print frame_counter, "frames in", dt, "seconds (", frame_counter/dt, "fps ) data: " + text_data + " x " + str(x) +" y " + str(y) + \
                                                                                     " Width " + str(w) + " Height " + str(h)
                if same == 20:
                    print ("end")
                    return text_data, x, y, w, h
                frame_counter = 0
                time_start = time.time()


if __name__=="__main__":
    options = {"-wh": None, "-d": None, "-h": None, "-s": None, "-host": None, "-port": None}
    parse_options(sys.argv[1:], options)
    sys.argv = sys.argv[:1]
    from camera_source import camerasrc

    device = "/dev/video0"
    if options["-d"] == None:
        print "device name is not set, suggesting /dev/video0"
    else:
        device = options["-d"]

    size=(640,480)
    if options["-wh"] == None:
        print "video frame size is not set, suggesting 640x480"
    else:
        sz = options["-wh"].split("x")
        size = (int(sz[0]), int(sz[1]))

    headless = False
    if options["-h"] == True:
        headless = True

    serve = False
    ss = None
    #if options["-s"] == True:
    #    host = "localhost"
    #    if options["-host"]:
    #        host = options["-host"]
    #    port = 40000
    #    if options["-port"]:
    #        port = options["-port"]
    #    serve = True
    #    ss = server.socket_server(host, port)



    src = camerasrc(size[0], size[1], device)

    if not headless:
        import pygame
        pygame.init()
        screen=pygame.display.set_mode(size)
        pygame.display.set_caption("visualizer")
        clock = pygame.time.Clock()

    tracker.tracker_init(size, headless)

    track = {}
    try:
        print (loop(track, headless, ss, size))
    except KeyboardInterrupt:
        print "finalizing"

