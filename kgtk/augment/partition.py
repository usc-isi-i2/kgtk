import numpy as np

##########################################
#    Partition Functions
##########################################


def get_intervals_for_values_based_on_percentile(values, num_bins):
    values = np.array(values)
    indexes = np.arange(len(values))

    # sort values and corresponding labels in ascending order
    indexes = np.array([i for i, v in sorted(zip(indexes, values), key=lambda pair: pair[1])])
    values.sort()

    interval_bounds = []
    for i in range(num_bins):
        index_of_lbound = int((i / num_bins) * len(values))
        index_of_ubound = int(((i + 1) / num_bins) * len(values)) - 1
        lbound = values[index_of_lbound]
        ubound = values[index_of_ubound]
        interval_bounds.append((lbound, ubound))
    intervals_for_values = []
    cur_interval_idx = 0
    for i in range(len(values)):
        while values[i] > interval_bounds[cur_interval_idx][1]:
            cur_interval_idx += 1
        intervals_for_values.append(interval_bounds[cur_interval_idx])

    # rearrange intervals to original order of values
    intervals_for_values_unscrambled = np.zeros(len(intervals_for_values), dtype=tuple)
    for i in range(len(indexes)):
        intervals_for_values_unscrambled[indexes[i]] = intervals_for_values[i]

    return intervals_for_values_unscrambled


def get_bins_jenks(df):
    """
    MODE: JENKS
    Partition the 1D array in Jenks Natural Breaks Algorithms
    """
    import jenkspy

    num_bins = len(get_bins_kde(df))
    values = np.array(df.loc[:, "node2"])
    if num_bins < 2:
        return [min(values)]

    breaks = jenkspy.jenks_breaks(values, num_bins)
    return breaks[:-1]


def get_bins_kde(df):
    """
    MODE: KDE
    Partition the 1D array in KDE
    """
    from sklearn.neighbors import KernelDensity
    from scipy.signal import argrelextrema
    from matplotlib.pyplot import plot

    values = np.array(df.loc[:, "node2"])
    kde = KernelDensity(kernel='gaussian', bandwidth=3).fit(values.reshape(-1, 1))
    s = np.linspace(min(values), max(values))
    e = kde.score_samples(s.reshape(-1, 1))
    plot(s, e)
    mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
    return [min(values)] + [s[i] for i in mi]


def get_bins_quantile(df, num_bins=None):
    """
    MODE: ORIGIN, QUANTILE
    Partition the 1D array into a list of entity nodes
    """
    if num_bins is None:
        num_bins = len(get_bins_kde(df))

    # Add two columns
    try:
        df.insert(loc=len(df.columns), column="lower_bound", value=["" for i in range(df.shape[0])])
        df.insert(loc=len(df.columns), column="upper_bound", value=["" for i in range(df.shape[0])])
    except Exception:
        pass

    values = np.array(df.loc[:, "node2"])

    # Partition the nodes based on node2
    intervals_for_values = get_intervals_for_values_based_on_percentile(values, num_bins)

    intervals = set(intervals_for_values)
    set_ = set()

    for i, (p1, p2) in enumerate(sorted(intervals, key=lambda x: x[0])):
        set_.add(p1)
    return sorted(set_)


def get_bins_fixed_length(df, num_bins=None):
    """
    MODE: FIXED_LENGTH
    """
    if num_bins is None:
        num_bins = len(get_bins_kde(df))
    values = np.array(df.loc[:, "node2"])
    values.astype(float)
    values = np.asarray(values, dtype=np.float64)
    return np.linspace(values.min(), values.max() - values.min(), num_bins + 1)[:-1]
