#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2025/5/15 11:51'
import pandas as pd

df = pd.read_excel('/Users/haoyang/Downloads/台账/台账/2025.03.19托克逊县公安局末梢情报(208条） - 副本.xlsx')

xx = df.head(10)
print(xx)
