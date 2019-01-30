#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:15:38 2018

@author: opdate
"""

import math
def svgarc(xcenter,ycenter,r,startangle,endangle):
    if startangle > endangle: 
        raise ValueError("startangle must be smaller than endangle")
    
    lines = []
    if endangle - startangle < 360:
        large_arc_flag = 0
        radiansconversion = math.pi/180.
        xstartpoint = xcenter + r*math.cos(startangle*radiansconversion)
        ystartpoint = ycenter - r*math.sin(startangle*radiansconversion)
        xendpoint = xcenter + r*math.cos(endangle*radiansconversion)
        yendpoint = ycenter - r*math.sin(endangle*radiansconversion)
        #If we want to plot angles larger than 180 degrees we need this
        if endangle - startangle > 180: large_arc_flag = 1
        lines.append(r"""<path d=" """)
        lines.append("M %s %s" %(xstartpoint,ystartpoint))
        lines.append("A %s %s 0 %s 0 %s %s" 
                     %(r,r,large_arc_flag,xendpoint,yendpoint))
        lines.append("L %s %s" %(xcenter,ycenter))
        lines.append(r"""Z"/>""")
    
    else:
        lines.append(r"""<circle cx="%s" cy="%s" r="%s"/>"""
                    %(xcenter,ycenter,r))
    
    return lines
            
def draw_mtf_aligment(xcenter,ycenter,r):
    l = svgarc(xcenter=xcenter,
                     ycenter=ycenter,
                     r=r,startangle=85,endangle=175)
    l2 = svgarc(xcenter=xcenter,
                      ycenter=ycenter,
                      r=r,startangle=265,endangle=355)
    return l +l2
    
if __name__ == '__main__':
    l = svgarc(xcenter=150,ycenter=190,r=50,startangle=85,endangle=175)
    l2 = svgarc(xcenter=150,ycenter=190,r=50,startangle=265,endangle=355)
    for i in l+l2:
        print(i)