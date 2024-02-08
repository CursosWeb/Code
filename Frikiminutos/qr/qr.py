#!/usr/bin/env python3

import pyqrcode

url='https://gsyc.urjc.es'
qr = pyqrcode.create(url)
qr.png("gsyc.png", scale=5)
