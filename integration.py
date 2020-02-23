# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:29:31 2019

@author: Ben
"""

# ToC:
# mc_dots(lower_left, x_length, y_length, function, n)
# mc_rectangle(x_start, x_end, n ,y_func)
# riemann_left(x_start, x_end, n, y_func)
# riemann_right(x_start, x_end, n, y_func)
# riemann_middle(x_start, x_end, n, y_func)
# simpson(x_start, x_end, n, y_func)
# trapezoid(x_start, x_end, n, y_func)
# polar_wedges(theta_start, theta_end, n, r_func)
# box_muller(n, mu, sigma_sq)
# lcg(n, m, a, c)
# sig_figs(num, n)
# dec_figs(num, n)

import numpy as np
import random as rand

# integration methods - maybe I can combine these into one function? 

def mc_dots(lower_left, x_length, y_length, function,n):
    """
    lower_left: tuple - lower left point of box
    x_length: float - x dimension of box, > 0
    y_length: float - y dimension of box, > 0
    function: function(x,y) - the value is < 0 when (x,y) is in the graph
    n: int - number of poitns to generate
    
    returns approx area
    """
    
    area = 0
    
    for i in range(n):
        # gen random points
        x_point = lower_left[0] + rand.random()*x_length
        y_point = lower_left[1] + rand.random()*y_length
        
        # check if points in graph
        if function(x_point, y_point) <= 0:
            area += 1
            
        # divide in counts by total counts
        area = area*(x_length*y_length)/n
        
    return area

def mc_rectangles(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    
    """
    
    area = 0
    
    for i in range(n):
        x_point = x_start + rand.random()*(x_end-x_start)
        area += y_func(x_point)
        
    area = (area/n)*abs(x_end-x_start)
    
    return area

# non random integration approximations
def riemann_left(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    """
    
    interval = (x_end - x_start)
    sum = 0
    
    for i in range(n):
        sum += y_func(x_start + i*interval) * interval
        
    return sum
    
def riemann_right(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    """
    interval = (x_end-x_start)/n
    sum = 0
    
    for i in range(n):
        sum += y_func(x_start + (i+1)*interval) * interval
        
    return sum

def riemann_middle(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    """
    interval = (x_end-x_start)/n
    sum = 0
    
    for i in range(n):
        sum += y_func(x_start + (i+0.5)*interval) * interval
        
    return sum

# newton-cotes integration methods
def simpson(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    """
    interval = (x_end-x_start)/n
    sum = 0
    
    for i in range(n):
        sum += (y_func(x_start + i*interval) + 4*y_func(x_start + (i+0.5)*interval) + y_func(x_start + (i+1)*interval )) * interval / 6
                
    return sum

def trapezoid(x_start, x_end, n, y_func):
    """
    x_start: float
    x_end: float
    n: int
    y_func: function(x)
    
    returns approx area
    """
    interval = (x_end-x_start)/n
    sum = 0
    
    for i in range(n):
        sum += ( y_func(x_start + i*interval) + y_func(x_start + (i+1)*interval)) / 2
    
    return sum


def polar_wedges(theta_start, theta_end, n, r_func):
    """
    theta_start: float
    theta_end: float
    n: int
    r_func: function(theta)
    
    """
    
    sum = 0
    interval = (theta_end-theta_start)/n
    
    for i in range(n):
        sum += 1/2 * interval * r_func(theta_start + interval*(i+0.5))**2
        
    return sum

# random number generation
def box_muller(n, mu, sigma_sq):
    """
    n: int
    mu: float - mean
    sigma_sq: float - variance
    
    returns list of n points distributed in ~N(mu, sigma_sq)
    
    """
    lst = []
    
    for i in range(int(n/2)):
        x_1 = rand.random()
        x_2 = rand.random()
        
        z_1 = mu + sigma_sq**0.5 * (-2*np.log(x_1))**0.5 * np.sin(2*np.pi*x_2)
        z_2 = mu + sigma_sq**0.5 * (-2*np.log(x_1))**0.5 * np.cos(2*np.pi*x_2)
        
        lst.append(z_1)
        lst.append(z_2)
    
    if(n%2==1):
        x_1 = rand.random()
        x_2 = rand.random()
        
        z_1 = mu + sigma_sq**0.5 * (-2*np.log(x_1))**0.5 * np.sin(2*np.pi*x_2)
#        z_2 = mu + sigma_sq**0.5 * (-2*np.log(x_1))**0.5 * np.cos(2*np.pi*x_2)
        
        lst.append(z_1)
#        lst.append(z_2)
        
    return lst

def lcg(n, m, a, c):
    """
    n: int - number of values
    m: int - the modulus
    a: int - the multiplier
    c: int - the increment
    
    # values from Numerical Recipes: 
    # (100, 2**32, 1664525, 1013904223)
    
    returns a list of n iteratively generated pseudorandom numbers
    """
    
    # pseudorandomly generated seed
    seed = rand.random()
    
    rand_list = [seed] # initiate list
    
    for i in range(n-1):
        rand_list.append((a*rand_list[i] + c)%m)
        
    # adjust values to be in range [0, 1)
    for i in range(n-1):
        rand_list[i] /= m
        
    return rand_list

# rounding functions
def sig_figs(num, n):
    """
    num: float
    n: int
    
    returns num with n sig figs
    
    """
    
def dec_figs(num, n):
    """
    num: float
    n: int
    
    returns num with n decimals after point
    """
