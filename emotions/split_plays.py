#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Made by madame Bernhard, reference: https://arxiv.org/abs/2005.01653
'''

# Requirements: os, pandas

import pandas as pd
import os
import shutil

def preprocess(values):
    sums_array = [0]
    s = 0
    for x in values:
        s = s + x
        sums_array.append(s)
    return sums_array


def psum(sums_array, i, j):
    return sums_array[j] - sums_array[i]


def optimal_equal_part(values, sums_array, k):
    n = len(values)
    avg = sum(values)/k
    print("avg", avg)
    best_error = [[0 for _ in range(k)] for _ in range(n + 1)]
    best_breaks = [[[] for _ in range(k)] for _ in range(n + 1)]
    for m in range(n+1):
        best_error[m][0] = abs(psum(sums_array, 0, m) - avg)
        best_breaks[m][0] = []
    for b in range(1, k):
        m = n
        final_break = n
        while m >= 0:
            if final_break > m:
                final_break = m
            while psum(sums_array, final_break, m) < avg and final_break > 0:
                final_break = final_break -1
            if ((best_error[final_break+1][b-1]
                    + abs(psum(sums_array, final_break+1, m) - avg))
                < (best_error[final_break][b-1]
                    + abs(psum(sums_array, final_break, m) - avg))):
                final_break = final_break + 1
            best_error[m][b] = (best_error[final_break][b-1]
                                + abs(psum(sums_array, final_break, m) - avg))
            best_breaks[m][b] = best_breaks[final_break][b-1] + [final_break]
            m = m - 1
    return best_breaks[n][k-1]


if __name__ == '__main__':
    suffix = "/results2/"
    prefix = "results2/"
    li_dir = os.listdir("."+suffix)
    for dir in li_dir:
        if os.path.isdir(dir):
            file_path = prefix + dir + "/rolling_mean.csv"
            shutil.copy(file_path, file_path+".old")
            df = pd.read_csv(file_path)
            token_lens = list(df.numTokens)
            sums = preprocess(token_lens)
            num_parts = 100
            res = optimal_equal_part(token_lens, sums, num_parts)
            res.insert(0,0)
            res.append(df.shape[0]) # ajouter index of the last phrase
            repeat_times_list = []
            for i in range(1,len(res)):
                repeat_times = res[i] - res[i-1]
                repeat_times_list.append(repeat_times)
            final_slice = []
            slice_index = 1
            for index in range(num_parts):
                rep = repeat_times_list[index] # get each repeat times
                for times in range(rep):
                    final_slice.append(slice_index)
                if (rep != 0): # if the slice is valid, add slice index
                    slice_index += 1
            df["progress"] = final_slice
            df.to_csv(file_path,index=False)
    