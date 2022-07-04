import pandas as pd


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
    df = pd.read_csv('weber-yo-yo/all_emo.csv')
    #print(df)
    token_lens = list(df.numTokens)
    print("nb tokens", sum(token_lens))
    sums = preprocess(token_lens)
    num_parts = 100
    res = optimal_equal_part(token_lens, sums, num_parts)
    res.append(df.shape[0]) # ajouter l'indice de la derniere phrase
    repeat_times_list = []
    for i in range(1,len(res)):
        repeat_times = res[i] - res[i-1]
        repeat_times_list.append(repeat_times)
    final_slice = []
    for index in range(num_parts - 1):
        rep = repeat_times_list[index] # get each repeat times
        for times in range(rep):
            final_slice.append(index)
    final_slice.append(final_slice[len(final_slice) - 1])
    df["progress"] = final_slice
    df.to_csv("weber-yo-yo/all_emo.csv")
    


'''
import pandas as pd


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
    df = pd.read_csv('weber-yo-yo/all_emo.csv')
    #print(df)
    token_lens = list(df.numTokens)
    print("nb tokens", sum(token_lens))
    sums = preprocess(token_lens)
    num_parts = 100
    res = optimal_equal_part(token_lens, sums, num_parts)
    print(res)
    print(len(res))
    print(df.loc[0:res[0]])
    res.insert(0, 0)
    res.append(len(df))
    partition_sizes = []
    for i in range(1, len(res)):
        partition_size = sum(df.loc[res[i-1]:res[i]-1].numTokens)
        partition_sizes.append(partition_size)
        print(f"Size of partition {i}:", partition_size, "tokens")
        print(f"    Start replica #{res[i-1]}, end replica #{res[i]-1}")

    print("Maximum partition size", max(partition_sizes), "tokens")
    print("Minimum partition size", min(partition_sizes), "tokens")
'''