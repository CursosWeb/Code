#!/usr/bin/env python3

import os

import rembg

dir = 'misc'
input = 'cafe.jpg'
output = 'cafe-nobg.jpg'

with open(input, 'rb') as ifile:
    with open(output, 'wb') as ofile:
        image = ifile.read()
        image_nobg = rembg.remove(image)
        ofile.write(image_nobg)