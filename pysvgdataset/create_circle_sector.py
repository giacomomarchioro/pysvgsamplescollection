#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:15:38 2018

@author: opdate
"""

import numpy as np

def write_svgarc(xcenter,ycenter,r,startangle,endangle,output='arc.svg'):
    if startangle > endangle: 
        raise ValueError("startangle must be smaller than endangle")
    
    if endangle - startangle < 360:
        large_arc_flag = 0
        radiansconversion = np.pi/180.
        xstartpoint = xcenter + r*np.cos(startangle*radiansconversion)
        ystartpoint = ycenter - r*np.sin(startangle*radiansconversion)
        xendpoint = xcenter + r*np.cos(endangle*radiansconversion)
        yendpoint = ycenter - r*np.sin(endangle*radiansconversion)
        #If we want to plot angles larger than 180 degrees we need this
        if endangle - startangle > 180: large_arc_flag = 1
        with open(output,'a') as f:
            f.write(r"""<path d=" """)
            f.write("M %s %s" %(xstartpoint,ystartpoint))
            f.write("A %s %s 0 %s 0 %s %s" 
                    %(r,r,large_arc_flag,xendpoint,yendpoint))
            f.write("L %s %s" %(xcenter,ycenter))
            f.write(r"""Z"/>""" )
    
    else:
        with open(output,'a') as f:
            f.write(r"""<circle cx="%s" cy="%s" r="%s"/>"""
                    %(xcenter,ycenter,r))
            
        
if __name__ == '__main__':
    write_svgarc(xcenter=150,ycenter=190,r=40,startangle=85,endangle=775)