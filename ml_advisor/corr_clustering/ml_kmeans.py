#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 22:03:51 2018

@author: rucsa
"""

import pandas as pd

from sklearn import cluster

data = pd.read_hdf("hdfs/distance_matrix.hdf5", "dataset1/x")

#You could turn your matrix of distances into raw data and input these to K-Means 
#clustering. The steps would be as follows:
#
#1) Distances between your N points must be squared euclidean ones. 
#   Perform "double centering" of the matrix: 
#       Substract row mean from each element; 
#       in the result, substract column mean from each element; 
#       in the result, add matrix mean to each element; divide by minus 2. 
#   The matrix you have now is the SSCP (sum-of-squares-and-cross-product) matrix 
#   between your points wherein the origin is put at geometrical centre of the 
#   cloud of N points. (Read explanation of the double centering here.)
#
#2) Perform PCA (Principal component analysis) on that matrix and obtain NxN component 
#   loading matrix. Some of last columns of it are likely to be all 0, - so cut them off. 
#   What you stay with now is actually principal component scores, the coordinates of 
#   your N points onto principal components that pass, as axes, through your cloud. 
#   This data can be treated as raw data suitable for K-Means input.
#
#P.S. If your distances aren't geometrically correct squared euclidean ones you 
#may encounter problem: the SSCP matrix may be not positive (semi)definite. 
#This problem can be coped with in several ways but with loss of precision.

