#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:44:59 2018

@author: rucsa
"""

def group_clusters(clusters, companies):
    cluster_labels = list(set(clusters))
    groups = {}
    for c in cluster_labels:
        if groups.get(c, None) == None:
            groups[c] = []
        for i in range (0, len(companies)):
            if clusters[i] == c:
                groups[c].append(i)
    return groups    