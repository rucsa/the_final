#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 18:17:21 2018

@author: rucsa
"""

import numpy as np
def cart_to_pole(x, y):
    raw = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (raw, phi)