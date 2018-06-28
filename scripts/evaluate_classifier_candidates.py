# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import division
import csv
import sys
import glob
import spacy
import pandas as pd
from pandas import ExcelFile

# Load english words
nlp = spacy.load("en_core_web_sm")

# Avoid ascii error
reload(sys)
sys.setdefaultencoding('utf8')

# Candidate polymers
candidate_polymers = []

def cleanup_poly(pl):
    new_pl = pl.strip().strip(',').strip('.')
    if len(new_pl)>=2 and new_pl[0] == '(' and new_pl[len(new_pl)-1]==')':
        new_pl=new_pl.rstrip(')').lstrip('(')
    return new_pl


def readlist(ifile):
    poly_list = []
    f = open(ifile)
    lines = f.readlines()
    for line in lines:
        poly = cleanup_poly(line.strip("\n"))
        upoly = u'%s' % (poly)
        poly_list.append(upoly)
    return poly_list

ground_truth_polymers = readlist ('../ground_truth/ground_truth_list_format.txt')
print len(ground_truth_polymers)

candidates = readlist('../candidates/listformat/filtered_classifier_candidates.txt')

dictionary = [x.strip().lower() for x in ground_truth_polymers]
dictionary = list(set(dictionary))
print "Number of polymer names in the dictionary: ", len(dictionary)

candidate_polymers = [x.strip().lower() for x in candidates]
candidate_polymers = list(set(candidate_polymers))
print "Number of candidate polymers in this file: ", (len(candidate_polymers))


TP = 0
FP = 0
for candidate in candidate_polymers:
    #ucandidate = u'%s' % candidate
    #if candidate.lower() in nlp.vocab:
    #    continue

    if candidate in dictionary:
        TP = TP + 1
    else:
        FP = FP + 1

precision = (TP/(TP+FP)*100)

FN = 0
for poly in dictionary:
    if poly not in candidate_polymers:
        FN = FN + 1

recall = (TP/(TP+FN)*100)
print "True pos: ", TP
print "False pos: ", FP
print "Precision: ", precision
print "Recall: ", recall
