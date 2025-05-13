'''
Helper functions for making figures.

Functions:
- heatmap:          Make a heatmap based on input data. Sets title, text ... as well
- bar:              Make a barplot. Sets title, text ... as well.
- scatter:          Make a scatter plot. Sets title, text ... as well.
- gen_title:        Generates a title when the plot is about an interval of time.
- gen_text:         Generates a text about standard deviation info.
- scale_interval:   scale interval if sim's data was already reduced.
- ave_interval:     Calculates average value of data over a time interval.
- ave_interval_1D:  Return in a 1D format.
'''


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# move ax a bit left if add text
# default value is [0.125, 0.11, 0.9, 0.88]


def heatmap(data, cmap = "Greens", annot = False, fmt = '.3g', title = None, text = None):
    '''
    Helper function for making heatmaps.

    Inputs:
        data:   1D data for which you want to make a heatmap. 
        cmap:   Color of heatmap. Uses matplotlib color maps
        annot:  Whether to show numbers of every block.
        fmt:    Number format for annotations. How many digits you want to keep.
        title:  The title you want to add. None means no title.
        text:   Adds some text in a text block at the top-right corner.

    Returns:
        fig:    Seaborn heatmap.
    '''

    fig, ax = plt.subplots()
    if text != None:
        ax.text(0.63, 0.9, text, size = 10, linespacing = 1.5, transform = plt.gcf().transFigure)

    ax = sns.heatmap(data, cmap = cmap, annot = annot, fmt = fmt)
    ax.title.set_text(title)
    
    return fig



def bar(data, color = "green", xlabel = None, ylabel = None, title = None, text = None):
    '''
    Helper Function for making barplots.

    Inputs:
        data:   2D data to make barplot.
        color:  Uses Matplotlib colors.
        xlabel, y_label: 
                Label for axes.
        title:  Title for the barplot.
        text:   Adds some text in a text block at the top-right corner.
    
    Returns:
        fig:    A Matplotlib barplot.
    '''

    N = np.array(data).size
    xaxis = np.array([i for i in range(N)])
    
    # make figure larger if has more data points
    fig, ax = plt.subplots()
    if N > 60:
        fig.set_size_inches(min(N * 0.12, 9.6), 4.8)

    if text != None:
        ax.text(0.63, 0.9, text, size = 10, linespacing = 1.5, transform = plt.gcf().transFigure)

    ax.bar(x = xaxis, height = data, color = color)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.title.set_text(title)
    
    return fig



def scatter(X, Y, color = "orange", alpha = 0.25, xlabel = "x", ylabel = "y", title = None):
    '''
    Helper function for makeing scatter plots.

    Inputs:
        X:      x-coordinates of points.
        Y:      y-coordinates of points.
        Note color is Matplotlib colors.
    
    Returns:
        fig:    A Matplotlib scatter plot.
    '''
    
    fig, ax = plt.subplots()
    ax.scatter(X, Y, color = color, alpha = alpha)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.title.set_text(title)

    return fig



def gen_title(title, start, end):
    '''
    Generate a title for plot when it's about an interval of time.
    '''
    title += ", " + str(round(start * 100, 1)) + " ~ " + str(round(end * 100, 1)) + "%"
    return title



def gen_text(ave, std):
    '''
    Generate text about standard deviation info.
    '''
    text = "ave: " + str(round(ave, 3)) + ", std: " + str(round(std, 3))
    return text



def ave_interval(data, start_index, end_index):
    '''
    Calculate average value of data over an interval. Return a 2D np.array
    Assume data is 3D with shape N x M x K, then takes average on the 3rd axis.

    Input:
        data:       3D np.array or list. Will take average on the 3rd axis.
        start_index, end_index: 
                    over what interval to take average.

    Returns:
        data_ave:   2D np.array with shape N x M, contains average value of data.
    '''
    
    N = len(data)
    M = len(data[0])
    
    # plot a particular record
    if start_index == end_index:
        start_index = end_index - 1
        
    data_ave = np.zeros((N, M))
    
    for i in range(N):
        for j in range(M):
            for k in range(start_index, end_index):
                data_ave[i][j] += data[i][j][k]
            data_ave[i][j] /= (end_index - start_index)
    
    return data_ave



def ave_interval_1D(data, start_index, end_index):
    '''
    Calculate average value of data over an interval. Return a 1D np.array.
    Assume data is 3D and has shape (1 x M x K) or (N x 1 x K). Then implicitly 'compress' that 1 and takes average on the 3rd axis.

    Input:
        data:       3D np.array or list. One of its dimensions must have size 1. Will take average on the 3rd axis.
        start_index, end_index: 
                    over what interval to take average.

    Returns:
        data_ave:   1D np.array with len N * M, contains average value of data.
    '''
    
    N = len(data)
    M = len(data[0])

    if start_index == end_index:
        start_index = end_index - 1
        
    data_ave = np.zeros(N * M)
    
    for i in range(N):
        for j in range(M):
            for k in range(start_index, end_index):
                data_ave[i * M + j] += data[i][j][k]
            data_ave[i * M + j] /= (end_index - start_index)
    
    return data_ave



def scale_interval(interval, compress_itv):
    # scale interval if sim's data was already reduced.
    if compress_itv < 1:
        raise ValueError('figures.scale_interval has compress_itv < 1:', compress_itv)

    interval = int(interval / compress_itv)
    if interval == 0:
        print('Warning: data already smoothed by an interval: sim.compress_itv =', compress_itv, 'which is coarser than your', interval)
        interval = 1

    return interval


