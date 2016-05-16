#!/usr/bin/env python
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

import pygst
import Image
pygst.require("0.10")
import gst
import sys
import imagesrc
import cv


class camerasrc(imagesrc.imagesrc):
    def __init__(self, width, height, device):

        multicast_ip = "224.1.1.1"
        multicast_udp_port = 5000

        self.appsink = gst.parse_launch("appsink drop=true max-buffers=1")
        cf_yuv = gst.parse_launch("capsfilter caps=\"video/x-raw-yuv,width="+str(width)+",height="+str(height)+"\"")
        tee = gst.parse_launch("tee name=t")

        queue_local = gst.element_factory_make("queue", "local")
        queue_serv = gst.element_factory_make("queue", "serv")

        cf = gst.parse_launch("capsfilter caps=\"video/x-raw-rgb,width="+str(width)+",height="+str(height)+",bpp=24,red_mask=16711680, green_mask=65280, blue_mask=255, endianness=4321\"")
        ff = gst.element_factory_make("ffmpegcolorspace", "converter")
        src = gst.parse_launch("v4l2src device="+device)

        vr = gst.parse_launch("videorate")
        ffcs = gst.parse_launch("ffmpegcolorspace")
        cf2 =  gst.parse_launch("capsfilter caps=\"video/x-raw-yuv,width="+str(width)+",height="+str(height)+"\"")
        x264 = gst.parse_launch("x264enc tune=zerolatency byte-stream=true bitrate=300")
        rtp = gst.parse_launch("rtph264pay")
        udpsink = gst.parse_launch("udpsink host="+str(multicast_ip)+" port="+str(multicast_udp_port)+" auto-multicast=true")

        print "creating pipe"
        self.pipe = gst.Pipeline(name="ecvpipe")
        self.pipe.add(src)
        self.pipe.add(cf_yuv)
        self.pipe.add(tee)
        self.pipe.add(ff)
        self.pipe.add(cf)
        self.pipe.add(vr)
        self.pipe.add(ffcs)
        self.pipe.add(cf2)
        self.pipe.add(x264)
        self.pipe.add(rtp)
        self.pipe.add(udpsink)
        self.pipe.add(queue_local)
        self.pipe.add(queue_serv)
        self.pipe.add(self.appsink)
        print "done"
        src.link(cf_yuv)
        gst.element_link_many(cf_yuv, tee)
        tee.link(queue_local)
        queue_local.link(ff)
        ff.link(cf)
        cf.link(self.appsink)
        tee.link(queue_serv)
        queue_serv.link(vr)
        vr.link(ffcs)
        ffcs.link(cf2)
        cf2.link(x264)
        x264.link(rtp)
        rtp.link(udpsink)
        print "setting state \"playing\""
        self.pipe.set_state(gst.STATE_PLAYING)
        self.imagewidth = width
        self.imageheight = height

        self.imcur = cv.CreateImageHeader((self.imagewidth, self.imageheight), 8, 3)

    def get_image(self):
        data = self.appsink.emit("pull-buffer")
        if data == None:
            print "pull-buffer underrun (broken camera ?)"
            exit()
        cv.SetData(self.imcur, data[:], self.imagewidth*3)
        pi = Image.fromstring("RGB", cv.GetSize(self.imcur), self.imcur.tostring())
        return pi

    def has_data(self):
        return True
