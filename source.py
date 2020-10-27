#!/usr/bin/env python2.7
#
#    bl-hotcorners: a script for adding hot corners to Openbox.
#    Copyright (C) 2012 Philip Newborough   <corenominal@corenominal.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Renamed for BunsenLabs

from Xlib import display
from Xlib.ext.xtest import fake_input
from Xlib import X
from subprocess import Popen, PIPE, STDOUT
import sys, time, os, ConfigParser, re
import argparse

check_intervall = 0.2

ap = argparse.ArgumentParser(description="Hotcorners")
ap.add_argument("-k", "--kill", help="attempt to kill any runnng instances",
            action="store_true")
ap.add_argument("-d", "--daemon", help="run daemon and listen for cursor triggers",
            action="store_true")
opts = ap.parse_args(sys.argv[1:])

p = Popen(['xdotool','getdisplaygeometry'], stdout=PIPE, stderr=STDOUT)
Dimensions = p.communicate()
Dimensions = Dimensions[0].replace('\n', '')
Dimensions = Dimensions.split(' ')
width = int(Dimensions[0])
height = int(Dimensions[1])
hw = width / 2
rt = width - 1
bt = height - 1

if opts.kill:
    print "Attempting to kill any running instances..."
    os.system('pkill -9 -f bl-hotcorners')
    exit()

elif opts.daemon:
    Config = ConfigParser.ConfigParser()
    cfgdir = os.getenv("HOME")+"/.config/bl-hotcorners"
    rcfile = cfgdir+"/bl-hotcornersrc"
    bounce = 40
    disp = display.Display()
    root=display.Display().screen().root

    def mousepos():
        data = root.query_pointer()._data
        return data["root_x"], data["root_y"], data["mask"]

    def mousemove(x, y):
        fake_input(disp, X.MotionNotify, x=x, y=y)
        disp.sync()

    try:
        cfgfile = open(rcfile)
    except IOError as e:
        if not os.path.exists(cfgdir):
            os.makedirs(cfgdir)
        cfgfile = open(rcfile,'w')
        Config.add_section('Hot Corners')
        Config.set('Hot Corners','top_left_corner_command', 'gmrun')
        Config.set('Hot Corners','top_right_corner_command', '')
        Config.set('Hot Corners','bottom_left_corner_command', '')
        Config.set('Hot Corners','bottom_right_corner_command', '')
        Config.write(cfgfile)
        cfgfile.close()

    while True:
        Config.read(rcfile)
        time.sleep(check_intervall)
        pos = mousepos()

        if pos[0] == 0 and pos[1] == 0:
            if Config.get('Hot Corners','top_left_corner_command') != '':
                time.sleep(0.2)
                pos = mousepos()
                if pos[0] == 0 and pos[1] == 0:
                    mousemove(pos[0] + bounce, pos[1] + bounce)
                    os.system('(' + Config.get('Hot Corners','top_left_corner_command') + ') &')
                    mousemove(pos[0] + bounce, pos[1] + bounce)
                    time.sleep(2)

        elif pos[0] == rt and pos[1] == 0:
            if Config.get('Hot Corners','top_right_corner_command') != '':
                time.sleep(0.2)
                pos = mousepos()
                if pos[0] == rt and pos[1] == 0 :
                    mousemove(pos[0] - bounce, pos[1] + bounce)
                    os.system('(' + Config.get('Hot Corners','top_right_corner_command') + ') &')
                    mousemove(pos[0] - bounce, pos[1] + bounce)
                    time.sleep(2)

        elif pos[0] == 0 and pos[1] == bt:
            if Config.get('Hot Corners','bottom_left_corner_command') != '':
                time.sleep(0.2)
                pos = mousepos()
                if pos[0] == 0 and pos[1] == bt:
                    mousemove(pos[0] + bounce, pos[1] - bounce)
                    os.system('(' + Config.get('Hot Corners','bottom_left_corner_command') + ') &')
                    mousemove(pos[0] + bounce, pos[1] - bounce)
                    time.sleep(2)

        elif pos[0] == rt and pos[1] == bt:
            if Config.get('Hot Corners','bottom_right_corner_command') != '':
                time.sleep(0.2)
                pos = mousepos()
                if pos[0] == rt and pos[1] == bt:
                    mousemove(pos[0] - bounce, pos[1] - bounce)
                    os.system('(' + Config.get('Hot Corners','bottom_right_corner_command') + ') &')
                    mousemove(pos[0] - bounce, pos[1] - bounce)
                    time.sleep(2)
