# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:29:16 2019

@author: Ben
"""

# ToC:
# forward_euler(initial_point, t_f, n, y_deriv)
# rk4(initial_point, t_f, n, y_deriv)
# backward_euler()???

import numpy as np


def forward_euler(initial_point, t_f, n, y_deriv):
    """
    initial_point: tuple (t_0, y_0)
    t_f: double - final time, make < t_0 for reverse forward euler
    n: integer- number of points
    y_deriv: function(t,y)
    
    returns tuple(t_points: list, y_points: list)
    """
    
    t_0, y_0 = initial_point # unpacking
    
    t_points = np.linspace(t_0, t_f, n)
    y_points = [y_0]
    
    dt = t_points[1] - t_points[0] # time change increment - may be negative
    
    for i in range(1,n):
        y_points.append(dt * y_deriv(t_points[i-1], y_points[i-1]) + y_points[i-1])
        
    return (t_points, y_points)


def rk4(initial_point, t_f, n, y_deriv):
    """
    initial_point: tuple (t_0, y_0)
    t_f: double - final time, make < t_0 for reverse forward euler
    n: integer- number of points
    y_deriv: function(t,y)
    
    returns tuple(t_points: list, y_points: list)
    """
    t_0, y_0 = initial_point # unpacking
    
    t_points = np.linspace(t_0, t_f, n)
    y_points = [y_0]
    
    dt = t_points[1]-t_points[0] # timechange increment - may be negative
    
    for i in range(1, n):
        dt = t_points[i] - t_points[i-1] # should be 0.1

        t_n = t_points[i-1]
        y_n = y_points[i-1]

        k_1 = y_deriv(t_n, y_n)
        k_2 = y_deriv(t_n + 1/2*dt, y_n + 1/2*dt*k_1)
        k_3 = y_deriv(t_n + 1/2*dt, y_n + 1/2*dt*k_2)
        k_4 = y_deriv(t_n + dt, y_n + dt*k_3)

        y_points.append(y_n + 1/6*dt*(k_1 + 2*k_2 + 2*k_3 + k_4))

    return (t_points, y_points)
