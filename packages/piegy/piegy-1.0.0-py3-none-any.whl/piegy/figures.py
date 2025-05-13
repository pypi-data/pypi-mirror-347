'''
Contains all the major plot functions. 

Plots for population:
- UV_heatmap:       Used for 2D space (both N, M > 1), plot distribution of U, V in all patches within a specified time interval.
                    Average population over that interval is taken.
- UV_bar:           Used for 1D space (N or M == 1), counterpart of UV_heatmap.
                    Plot average distribution of U, V in a specified time interval in a barplot.
- UV_dyna:         Plot change of total U, V overtime.
- UV_hist:          Make a histogram of U, V in a specified time interval.
- UV_std:           Plot change of standard deviation of U, V over time.
- UV_expected_val:  Calculate expected U, V distribution based on matrices, assuming no migration return values (np.array)
- UV_expected:      Calculate expected distribution of U, V based on matrices, assuming no migration.


Plots for payoff:
- pi_heatmap:       Used for 2D space, plot distribution of U_pi & V_pi within a specified time interval.
                    Average payoff over that interval is taken.
- pi_bar:           Used for 1D space, counterpart of pi_heatmap.
                    Plot average distribution of U_pi & V_pi in a specified time interval in a bar plot.
- pi_dyna:         Plot change of total U_pi, V_pi overtime.
- pi_hist:          Make a histogram of U_pi, V_pi in a specified time interval.
- pi_std:           Plot change of standard deviation of U_pi, V_pi over time.


Popu-payoff correlation:
- UV_pi:            Make two scatter plots: x-axes are U, V, y-axes are U's and V's payoff, in a specified time interval.
                    Reveals relationship between population and payoff.

'''


from .tools import figure_tools as figure_t
from . import model as model

import matplotlib.pyplot as plt
import numpy as np



# curve type in plot
# used by UV_dyna, UV_std, and pi_dyna
CURVE_TYPE = '-'



def UV_heatmap(sim, U_color = 'Purples', V_color = 'Greens', start = 0.95, end = 1.0, annot = False, fmt = '.3g'):
    '''
    Makes two heatmaps for U, V average distribution over a time interval, respectively. Works best for 2D space.
    1D works as well, but figures look bad.

    Inputs:
        sim:        A model.simulation object.
        U_color:    Color for U's heatmap, uses matplotlib color maps.
        V_color:    Color for V's heatmap.
        start:      (0,1) float, where the interval should start from. Intended as a 'percentage'. 
                    For example, start = 0.8 means the interval should start from the 80% point of sim.maxtime.
        end:        (0,1) float, where the interval ends.
        annot:      bool, whether to add annotations (show exact numbers for every patch).
        fmt:        Number format for annotations. How many digits you want to keep. Please set annot = True first and then use fmt.

    Returns:
        fig1, fig2: Two heatmaps of U, V distribution.
    '''
    
    start_index = int(start * sim.max_record)
    end_index = int(end * sim.max_record)
    
    # see ave_interval below
    U_ave = figure_t.ave_interval(sim.U, start_index, end_index)
    V_ave = figure_t.ave_interval(sim.V, start_index, end_index)
    
    #### plot ####
    
    U_title = figure_t.gen_title('U', start, end)
    U_text = figure_t.gen_text(np.mean(U_ave), np.std(U_ave))
    V_title = figure_t.gen_title('V', start, end)
    V_text = figure_t.gen_text(np.mean(V_ave), np.std(V_ave))

    fig1 = figure_t.heatmap(U_ave, U_color, annot, fmt, U_title, U_text)
    fig2 = figure_t.heatmap(V_ave, V_color, annot, fmt, V_title, V_text)
        
    return fig1, fig2
    


def UV_bar(sim, U_color = 'purple', V_color = 'green', start = 0.95, end = 1.0):
    '''
    Makes two barplots for U, V average distribution over a time interval. Works best for 1D space.
    2D works as well, but figures look bad.

    Inputs:
        sim:        A model.simulation object.
        U_color:    Color of U's barplot. Uses Matplotlib colors.
                    See available colors at: https://matplotlib.org/stable/gallery/color/named_colors.html
        V_color:    Color of V's barplot. Uses Matplotlib colors.
        start:      (0,1) float. How much proportion of sim.maxtime you want the interval to start from.
        end:        (0,1) float. Where you want the interval to end.

    Returns:
        fig1, fig2: Two Matplotlib bar plots, for U and V, respectively.
    '''
    
    start_index = int(start * sim.max_record)
    end_index = int(end * sim.max_record)
    
    U_ave = figure_t.ave_interval_1D(sim.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(sim.V, start_index, end_index)

    #### plot ####

    U_title = figure_t.gen_title('U', start, end)
    U_text = figure_t.gen_text(np.mean(U_ave), np.std(U_ave))
    V_title = figure_t.gen_title('V', start, end)
    V_text = figure_t.gen_text(np.mean(V_ave), np.std(V_ave))

    fig1 = figure_t.bar(U_ave, color = U_color, xlabel = 'patches', ylabel = 'U', title = U_title, text = U_text)
    fig2 = figure_t.bar(V_ave, color = V_color, xlabel = 'patches', ylabel = 'V', title = V_title, text = V_text)

    return fig1, fig2




def UV_dyna(sim, interval = 20, grid = True):
    '''
    Plots how total U, V change overtime.
    The curves are not directly based on every single data point. 
    Rather, it takes the average over many intervals of points to smooth out local fluctuations.
        For example, interval = 20 means the first point on the curves are based on the average value of data points 0~19.
        So if there are 2000 data points in total, then there will be 2000 / 20 = 100 points on the curves.

    Inputs:
        sim:        A model.simulation object.
        interval:   How many data points to take average over. Larger value makes curves smoother, but also loses local fluctuations.
                    NOTE: this interval doesn't overlap with sim.compress_itv. 
                    e.g. you already took average over every 20 data points, then using interval <= 20 here has no smoothing effect.
        grid:       Whether to add grid lines to plot.
    
    Returns:
        fig:        A Matplotlib figure, contains U's, V's, and U+V population.
    '''
    
    # store the average values in lists
    U_curve = []
    V_curve = []
    total_curve = []

    interval = figure_t.scale_interval(interval, sim.compress_itv)
    interval_num = int(sim.max_record / interval)
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(sim.U, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(sim.V, i * interval, (i + 1) * interval)
        
        U_curve.append(np.sum(U_ave))
        V_curve.append(np.sum(V_ave))
        total_curve.append(U_curve[-1] + V_curve[-1])
        
    #### plot ####   
    xaxis = np.linspace(0, sim.maxtime, len(U_curve))

    fig, ax = plt.subplots()
    ax.grid(grid)
    ax.plot(xaxis, U_curve, CURVE_TYPE, label = 'U')
    ax.plot(xaxis, V_curve, CURVE_TYPE, label = 'V')
    ax.plot(xaxis, total_curve, CURVE_TYPE, label = 'total')
    ax.title.set_text('U & V over time')
    ax.legend()

    return fig




def UV_hist(sim, U_color = 'purple', V_color = 'green', start = 0.95, end = 1.0):
    '''
    Makes density histograms for U, V's average distribution over an interval.
    Sometimes it may not be shown in density plots due to matplotlib features.

    Returns:
        fig1, fig2: Two Matplotlib histograms, for U and V, respectively.
    '''

    start_index = int(start * sim.max_record)
    end_index = int(end * sim.max_record)
    
    U_ave = figure_t.ave_interval_1D(sim.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(sim.V, start_index, end_index)
    
    #### plot ####
    
    fig1, ax1 = plt.subplots()
    ax1.set_xlabel('U')
    ax1.set_ylabel('density')
    ax1.hist(U_ave, color = U_color, density = True)
    ax1.title.set_text(figure_t.gen_title('U hist', start, end))
    
    fig2, ax2 = plt.subplots()
    ax2.set_xlabel('V')
    ax2.set_ylabel('density')
    ax2.hist(V_ave, color = V_color, density = True)
    ax2.title.set_text(figure_t.gen_title('V hist', start, end))

    return fig1, fig2




def UV_std(sim, interval = 20, grid = True):
    '''
    Plots how standard deviation of U, V change over time.
    Takes average over many small interval to smooth out local fluctuations.

    Returns:
        fig:    A Matplotlib figure, contains U's and V's std curves.
    '''

    interval = figure_t.scale_interval(interval, sim.compress_itv)
    interval_num = int(sim.max_record / interval)
    
    U_std = []
    V_std = []
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(sim.U, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(sim.V, i * interval, (i + 1) * interval)
        
        U_std.append(np.std(U_ave))
        V_std.append(np.std(V_ave))
    
    #### plot ####
    xaxis = np.linspace(0, sim.maxtime, len(U_std))

    fig, ax = plt.subplots()
    ax.grid(grid)
    ax.plot(xaxis, U_std, CURVE_TYPE, label = 'U std')
    ax.plot(xaxis, V_std, CURVE_TYPE, label = 'V std')
    ax.legend()
    ax.set_xlabel('time (records)', fontsize = 11)
    ax.title.set_text('std_dev over time')
    
    return fig



def UV_expected_val(sim):
    '''
    Calculate expected U & V distribution based on matrices, assume no migration.
    To differentiate from UV_expected in figures.py: this one return arrays (values).
    '''
    
    U_expected = np.zeros((sim.N, sim.M))
    V_expected = np.zeros((sim.N, sim.M))
    
    for i in range(sim.N):
        for j in range(sim.M):
            # say matrix = [a, b, c, d]
            # U_proportion = (d - b) / (a - b - c + d)
            U_prop = (sim.X[i][j][3] - sim.X[i][j][1]) / (sim.X[i][j][0] - sim.X[i][j][1] - sim.X[i][j][2] + sim.X[i][j][3])
            # equilibrium payoff, U_payoff = V_payoff
            eq_payoff = U_prop * sim.X[i][j][0] + (1 - U_prop) * sim.X[i][j][1]
            
            # payoff / kappa * proportion
            U_expected[i][j] = eq_payoff / sim.P[i][j][4] * U_prop
            V_expected[i][j] = eq_payoff / sim.P[i][j][5] * (1 - U_prop)
                
    return U_expected, V_expected




def UV_expected(sim, U_color = 'Purples', V_color = 'Greens', annot = False, fmt = '.3g'):
    '''
    Calculate expected population distribution based on matrices, assuming no migration.
    For the formulas, see stochastic_mode.expected_UV

    Some Inputs:
        Note the colors are color maps.
    
    Returns:
    fig1, fig2: If 2D (N and M both > 1), then fig1 and fig2 are heatmaps.
                If 1D (N or M == 1), then fig1 and fig2 are barplots.
    '''
    
    U_expected, V_expected = UV_expected_val(sim)
    
    U_text = figure_t.gen_text(np.mean(U_expected), np.std(U_expected))
    V_text = figure_t.gen_text(np.mean(V_expected), np.std(V_expected))
    
    #### plot ####
    
    if (sim.N != 1) and (sim.M != 1):
        # 2D
        fig1 = figure_t.heatmap(U_expected, U_color, annot, fmt, title = 'Expected U', text = U_text)
        fig2 = figure_t.heatmap(V_expected, V_color, annot, fmt, title = 'Expected V', text = V_text)

    else:
        # 1D     
        fig1 = figure_t.bar(U_expected.flatten(), color = U_color, xlabel = 'patches', ylabel = 'popu', title = 'Expected U', text = U_text)
        fig2 = figure_t.bar(V_expected.flatten(), color = V_color, xlabel = 'patches', ylabel = 'popu', title = 'Expected V', text = V_text)

    return fig1, fig2




def pi_heatmap(sim, U_color = 'BuPu', V_color = 'YlGn', start = 0.95, end = 1.0, annot = False, fmt = '.3g'):
    '''
    Make heatmaps for payoff in a specified interval.
    Works best for 2D. 1D works as well, but figures look bad.

    Some Inputs:.
        Note the colors are matplotlib color maps.

    Returns:
        fig1, fig2: Seaborn heatmaps, for U's & V's payoff distribution, respectively.
    '''
    
    start_index = int(sim.max_record * start)
    end_index = int(sim.max_record * end)
    
    U_pi_ave = figure_t.ave_interval(sim.U_pi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval(sim.V_pi, start_index, end_index)
    
    U_title = figure_t.gen_title('U_pi', start, end)
    U_text = figure_t.gen_text(np.mean(U_pi_ave), np.std(U_pi_ave))
    V_title = figure_t.gen_title('V_pi', start, end)
    V_text = figure_t.gen_text(np.mean(V_pi_ave), np.std(V_pi_ave))
    
    fig1 = figure_t.heatmap(U_pi_ave, U_color, annot, fmt, U_title, U_text)
    fig2 = figure_t.heatmap(V_pi_ave, V_color, annot, fmt, V_title, V_text)

    return fig1, fig2




def pi_bar(sim, U_color = 'violet', V_color = 'yellowgreen', start = 0.95, end = 1.0):
    '''
    Make barplot for payoff in a specified interval.
    Works best for 1D. 2D works as well, but figures look bad.

    Returns:
        fig1, fig2: Matplotlib barplots, for U's and V's payoff distribution, respectively.
    '''
    
    start_index = int(sim.max_record * start)
    end_index = int(sim.max_record * end)
    
    U_pi_ave = figure_t.ave_interval_1D(sim.U_pi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval_1D(sim.V_pi, start_index, end_index)
    
    U_title = figure_t.gen_title('U_pi', start, end)
    U_text = figure_t.gen_text(np.mean(U_pi_ave), np.std(U_pi_ave))
    V_title = figure_t.gen_title('V_pi', start, end)
    V_text = figure_t.gen_text(np.mean(V_pi_ave), np.std(V_pi_ave))
    
    fig1 = figure_t.bar(U_pi_ave, U_color, 'patches', 'pi', U_title, U_text)
    fig2 = figure_t.bar(V_pi_ave, V_color, 'patches', 'pi', V_title, V_text)

    return fig1, fig2




def pi_dyna(sim, interval = 20, grid = True):
    '''
    Plot how payoffs change over time.

    Returns:
        fig:    Matplotlib figure of U's, V's, and U+V payoff, either total or not.
    '''
    
    U_curve = []
    V_curve = []
    total_curve = []

    interval = figure_t.scale_interval(interval, sim.compress_itv)
    interval_num = int(sim.max_record / interval)
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(sim.U_pi, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(sim.V_pi, i * interval, (i + 1) * interval)
    
        U_curve.append(np.sum(U_ave))
        V_curve.append(np.sum(V_ave))
        total_curve.append(U_curve[-1] + V_curve[-1])
        
    #### plot ####    
    xaxis = np.linspace(0, sim.maxtime, len(U_curve))
    
    fig, ax = plt.subplots()
    ax.grid(grid)
    ax.plot(xaxis, U_curve, CURVE_TYPE, label = 'U_pi')
    ax.plot(xaxis, V_curve, CURVE_TYPE, label = 'V_pi')
    ax.plot(xaxis, total_curve, CURVE_TYPE, label = 'total')
    ax.set_xlim(0, sim.maxtime)
    ax.title.set_text('U&V _pi over time')
    ax.legend()

    return fig




def pi_hist(sim, U_color = 'violet', V_color = 'yellowgreen', start = 0.95, end = 1.0):
    '''
    Makes deensity histograms of U's and V's payoffs in a sepcified interval.
    Sometimes it may not be shown in density plots due to matplotlib features.
    
    Returns:
        fig1, fig2:     histogram of U's and V's payoff.
    '''

    start_index = int(start * sim.max_record)
    end_index = int(end * sim.max_record)

    U_pi_ave = figure_t.ave_interval_1D(sim.U_pi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval_1D(sim.V_pi, start_index, end_index)
    
    #### plot ####
    
    fig1, ax1 = plt.subplots()
    ax1.set_xlabel('U_pi')
    ax1.set_ylabel('density')
    ax1.hist(U_pi_ave, color = U_color, density = True)
    ax1.title.set_text(figure_t.gen_title('U_pi hist', start, end))
    
    fig2, ax2 = plt.subplots()
    ax2.set_xlabel('V_pi')
    ax2.set_ylabel('density')
    ax2.hist(V_pi_ave, color = V_color, density = True)
    ax2.title.set_text(figure_t.gen_title('V_pi hist', start, end))

    return fig1, fig2




def pi_std(sim, interval = 20, grid = True):
    '''
    Plots how standard deviation of payoff change over time.

    Returns:
        fig:    Matplotlib figure of the std of payoffs.
    '''
    
    
    interval = figure_t.scale_interval(interval, sim.compress_itv)
    interval_num = int(sim.max_record / interval)
    
    U_pi_std = []
    V_pi_std = []
    
    for i in range(interval_num):
        U_pi_ave = figure_t.ave_interval(sim.U_pi, i * interval, (i + 1) * interval)
        V_pi_ave = figure_t.ave_interval(sim.V_pi, i * interval, (i + 1) * interval)
        
        U_pi_std.append(np.std(U_pi_ave))
        V_pi_std.append(np.std(V_pi_ave))
    
    #### plot ####
    xaxis = np.linspace(0, sim.maxtime, len(U_pi_std))
    
    fig, ax = plt.subplots()
    ax.grid(grid)
    ax.plot(xaxis, U_pi_std, CURVE_TYPE, label = 'U_pi std')
    ax.plot(xaxis, V_pi_std, CURVE_TYPE, label = 'V_pi std')
    ax.legend()
    ax.set_xlabel('time (records)', fontsize = 11)
    ax.title.set_text('std over time')
    
    return fig




def UV_pi(sim, U_color = 'violet', V_color = 'yellowgreen', alpha = 0.25, start = 0.95, end = 1.0):
    '''
    Make two scatter plots: x-axes are population and y-axes are payoff in a specified time interval.
    Reveals relationship between population and payoff.

    Returns:
        fig1, fig2: U's and V's population-payoff scatter plots.
    '''
    
    start_index = int(start * sim.max_record)
    end_index = int(end * sim.max_record)
    
    U_ave = figure_t.ave_interval_1D(sim.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(sim.V, start_index, end_index)

    U_pi_ave = figure_t.ave_interval(sim.U_pi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval(sim.V_pi, start_index, end_index)
    
    
    fig1 = figure_t.scatter(U_ave, U_pi_ave, U_color, alpha, xlabel = 'U', ylabel = 'U_pi', title = 'U - U_pi')
    fig2 = figure_t.scatter(V_ave, V_pi_ave, V_color, alpha, xlabel = 'V', ylabel = 'V_pi', title = 'V - V_pi')
    
    return fig1, fig2


