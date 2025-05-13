'''
Make mp4 videos for simulation results.

Videos are made by:
make every frame by figures.py functions, then put frames together into a video.

Public Function:
- make_video:   make video based simulation results.

Private Functions
- get_max_lim:  Get the max lim (interval) over many lims, and then expand it a bit for better accommodation.
                Essentially takes union of those intervals. 
- video_lim:    Find a large enough xlim and ylim for video.
- sort_frames:  Put frames in order.
other not documented here.

'''


from . import figures
from .tools import file_tools as file_t


import matplotlib.pyplot as plt
import numpy as np
import os
import imageio.v2 as imageio
import re
from moviepy import VideoFileClip


# a list of supported figures
SUPPORTED_FIGURES = ['UV_heatmap', 'pi_heatmap', 'UV_bar', 'pi_bar', 'UV_hist', 'pi_hist', 'UV_pi']


# map function name to functios in figures.py
# functions not in this dictionary is not supported for videos.
FUNC_DICT = {'UV_heatmap': figures.UV_heatmap, 'UV_bar': figures.UV_bar, 'UV_hist': figures.UV_hist, 
             'pi_heatmap': figures.pi_heatmap, 'pi_bar': figures.pi_bar, 'pi_hist': figures.pi_hist, 'UV_pi': figures.UV_pi}


# Map some color maps to regular colors, used to change colors when an invalid color name is given
SNS_PLT_COLOR_DICT = {'Greens': 'green', 'Purples': 'purple', 'BuPu': 'violet', 'YlGn': 'yellowgreen'}
# Map regular colors to color maps
PLT_SNS_COLOR_DICT = {'green': 'Greens', 'purple': 'Purples', 'violet': 'BuPu', 'yellowgreen': 'YlGn'}




def convert_color(func_name, U_color, V_color):
    '''
    Converts some invalid colors.
    If making heatmap videos but gave single colors, map to color maps.
    If making barplot or histogram videos but gave single colors, map to Matplotlib
    '''

    if 'heatmap' in func_name:
        # if making heatmaps but give regular colors
        if U_color in PLT_SNS_COLOR_DICT.keys():
            print('Making heatmaps, changed \'' + U_color + '\' to \'' + PLT_SNS_COLOR_DICT[U_color] + '\'')
            U_color = PLT_SNS_COLOR_DICT[U_color]
        if V_color in PLT_SNS_COLOR_DICT.keys():
            print('Making heatmaps, changed \'' + V_color + '\' to \'' + PLT_SNS_COLOR_DICT[V_color] + '\'')
            V_color = PLT_SNS_COLOR_DICT[V_color]
        
        return U_color, V_color

    elif 'heatmap' not in func_name:
        # if making barplots or histogram
        if U_color in SNS_PLT_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + U_color + '\' to \'' + SNS_PLT_COLOR_DICT[U_color] + '\'')
            U_color = SNS_PLT_COLOR_DICT[U_color]
        if V_color in SNS_PLT_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + V_color + '\' to \'' + SNS_PLT_COLOR_DICT[V_color] + '\'')
            V_color = SNS_PLT_COLOR_DICT[V_color]

        return U_color, V_color



def get_max_lim(lims):
    '''
    Get the max lim over many lims, i.e., the lowest lower bound and highest upper bound.
    And then expand it a bit for better accommodation.

    Input:
        lim:    list or np.array, has form [lim1, lim2, ...]
    
    Returns:
        A max lim which contains all lims.
    '''

    lims = np.array(lims)
    
    lim_min = np.min(lims[:, 0]) # min of min
    lim_max = np.max(lims[:, 1]) # max of max
    r = lim_max - lim_min

    if lim_min != 0:
        # negative values are reached
        # extend both upper bound and lower bound 
        return [lim_min - r * 0.05, lim_max + r * 0.05]
    else:
        # only extend upper bound
        return [0, lim_max + r * 0.05]




def frame_lim(sim, func, frames):
    '''
    Find a large enough xlim and ylim for frames, if not heatmaps.

    Inputs:
        sim:        A stochastic_model.simulation object, the simulation results.
        frames:     How many frame to make for the video.
    
    Returns:
        xlim and ylim for U and V, 4 in total.
    '''
    
    # take 10 samples and store their lims in list
    U_xlist = []
    U_ylist = []
    V_xlist = []
    V_ylist = []
    
    for i in range(10):
        U_fig, V_fig = func(sim, start = i / 10, end = (i / 10 + 1 / frames))

        U_xlist.append(U_fig.get_axes()[0].get_xlim())
        U_ylist.append(U_fig.get_axes()[0].get_ylim())
        V_xlist.append(V_fig.get_axes()[0].get_xlim())
        V_ylist.append(V_fig.get_axes()[0].get_ylim())

        plt.close(U_fig)
        plt.close(V_fig)
    
    # get the largest 'range' based on the lists
    U_xlim = get_max_lim(U_xlist)
    U_ylim = get_max_lim(U_ylist)
    V_xlim = get_max_lim(V_xlist)
    V_ylim = get_max_lim(V_ylist)
    
    return U_xlim, U_ylim, V_xlim, V_ylim




def frame_heatmap_lim(sim, func, frames):
    '''
    Find a large enough color bar lim for frames, if heatmaps.

    Inputs:
        sim:        A stochastic_model.simulation object, the simulation results.
        frames:     How many frame to make for the video.
    
    Returns:
        clim for U and V
    '''

    U_list = []
    V_list = []

    for i in range(10):
        U_fig, V_fig = func(sim, start = i / 10, end = (i / 10 + 1 / frames))

        U_ax = U_fig.get_axes()[0]
        U_list.append(U_ax.collections[0].get_clim())
        V_ax = V_fig.get_axes()[0]
        V_list.append(V_ax.collections[0].get_clim())

        plt.close(U_fig)
        plt.close(V_fig)

    U_clim = get_max_lim(U_list)
    V_clim = get_max_lim(V_list)

    return U_clim, V_clim



def sort_frames(images):
    '''
    Put frames in order.

    Inputs:
        images: A list of dirs (frame names)
    '''
    numeric_part, non_numeric_part = re.match(r'(\d+) (\D+)', images).groups()
    return (int(numeric_part), non_numeric_part)



def make_mp4(dirs, frame_dirs, duration, video_name):
    '''
    Convert frames into a mp4 video.

    Inputs:
        dirs:       where to store the video.
        frame_dirs: where to find frames.
        duration:   how long the video should be.
        video_name: name of the video.
    '''

    # png to gif
    images = [img for img in os.listdir(frame_dirs) if img.endswith('.png')] 
    images.sort(key = sort_frames)

    image_list = []
    for img in images:
        img_path = os.path.join(frame_dirs, img)
        image_list.append(imageio.imread(img_path))
    gif_dirs = dirs + '/temp.gif'
    imageio.mimsave(gif_dirs, image_list, format = 'gif', duration = duration)
    
    # gif to mp4
    clip = VideoFileClip(gif_dirs)
    clip.write_videofile(video_name, logger = None)
    # delete gif
    os.remove(gif_dirs)



def make_video(sim, func_name = 'UV_heatmap', frames = 100, speed = 1.25, dpi = 120, U_color = 'Greens', V_color = 'Purples', annot = False, fmt = '.3g', del_frames = False, dirs = 'videos'):
    '''
    Make a mp4 video based on simulation results.

    Inputs:
    - sim:            a stochastic_model.simulation object, the simulation results.
    - func_name:      what function to use to make the frames. Should be one of the functions in figures.py
    - frames:         how many frames to make. Use more frames for more smooth evolutions.
    - speed:          how long every frame should last. Use larger number for slower video.
    - dpi:            dpi of frames
    - U_color:        color for U's videos. Color maps or regular colors, based on what function you use.
    - V_color:        color for V's videos.
    - annot:          used by heatmaps. Whether to show numbers.
    - fmt:            number format
    - del_frames:     whether to delete frames after making video.
    - dirs:           where to store the frames and videos.
    '''
    
    if func_name not in FUNC_DICT.keys():
        raise ValueError(func_name + ' not supported for videos.')
    func = FUNC_DICT[func_name]

    # convert color if invalid colors are given
    U_color, V_color = convert_color(func_name, U_color, V_color)
    
    # print progress
    one_progress = frames / 100
    current_progress = one_progress
    
    if 'heatmap' in func_name:
        # make sure a fixed color bar for all frames
        U_clim, V_clim = frame_heatmap_lim(sim, func, frames)
    else:
        # make sure y axis not changing if not making heatmaps
        U_xlim, U_ylim, V_xlim, V_ylim = frame_lim(sim, func, frames)

    
    U_frame_dirs = dirs + '/U-' + func_name
    V_frame_dirs = dirs + '/V-' + func_name
    
    if os.path.exists(U_frame_dirs):
        file_t.del_dirs(U_frame_dirs)
    os.makedirs(U_frame_dirs)
    if os.path.exists(V_frame_dirs):
        file_t.del_dirs(V_frame_dirs)
    os.makedirs(V_frame_dirs)

        
    #### for loop ####
    
    for i in range(frames):
        if i > current_progress:
            print('making frames', round(i / frames * 100), '%', end = '\r')
            current_progress += one_progress
        
        if 'heatmap' in func_name:
            U_fig, V_fig = func(sim, U_color, V_color, start = i / frames, end = (i + 1) / frames, annot = annot, fmt = fmt)
        else:
            U_fig, V_fig = func(sim, U_color, V_color, start = i / frames, end = (i + 1) / frames)
        U_ax = U_fig.get_axes()[0]
        V_ax = V_fig.get_axes()[0]
        
        if 'heatmap' in func_name:
            U_ax.collections[0].set_clim(U_clim)
            V_ax.collections[0].set_clim(V_clim)
        else:
            # make sure y axis not changing if not heatmap and not UV_pi
            U_ax.set_ylim(U_ylim)
            V_ax.set_ylim(V_ylim)
            if ('hist' in func_name) or (func_name == 'UV_pi'):
                # need to set xlim as well for UV_pi and histograms
                U_ax.set_xlim(U_xlim)
                V_ax.set_xlim(V_xlim)

        U_fig.savefig(U_frame_dirs + '/' + str(i) + ' U' + '.png', dpi = dpi)
        V_fig.savefig(V_frame_dirs + '/' + str(i) + ' V' + '.png', dpi = dpi)
        
        plt.close(U_fig)
        plt.close(V_fig)
        
    #### for loop ends ####
    
    # frames done
    print('making mp4...      ', end = '\r')
    
    # make videos based on frames
    make_mp4(dirs, U_frame_dirs, frames * speed, dirs + '/U-' + func_name + '.mp4')
    make_mp4(dirs, V_frame_dirs, frames * speed, dirs + '/V-' + func_name + '.mp4')
    
    if del_frames:
        file_t.del_dirs(U_frame_dirs)
        file_t.del_dirs(V_frame_dirs)
        print('video saved: ' + dirs + ', frames deleted')
    else:
        print('video saved: ' + dirs + '      ')



