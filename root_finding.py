# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:08:54 2019

@author: Ben
"""

# ToC: 
# bisection(x_a, x_b, function, error)
# secant(x_0, x_1, function, error)

import numpy as np

# root finding
def bisection(x_a, x_b, function, error):
    """
    x_a: double - on one side of y=0
    x_b: double - on other side of y=0
    function: function(x) - to be zero-d
    error: double - error range
    """
    same_side_error = False
    x_n = (x_a+x_b)/2
    f_x = function(x_n)
    
    while(abs(f_x) > error):
        if(function(x_a)*function(x_b) > 0 ):
            print('Error: points are on same side of y=0')
            same_side_error = True
            break
        
    elif function(x_a)*f_x >= 0:
        x_a = x_n
        
    else: # if f(x_b)*f_x >= 0
        x_b = x_n
        
    x_n = (x_a+x_b)/2
    f_x = function(x_n)
    
    
    if not same_side_error:
        return x_n
    
def secant(x_0, x_1, function, error):
    """
    x_a: double - on one side of y=0
    x_b: double - on other side of y=0
    function: function(x) - to be zero-d
    error: double - error range
    """
    
    def close_enough(a,b,error_range):
        return abs(a-b) <= error_range
    
    x_2 = x_1 - (function(x_1)*(x_1-x_0))/(function(x_1)-function(x_0))
    f_x_2= function(x_2)
    error_range = error
    zero_denominator_error = False
    
    
    while(not close_enough(f_x_2, 0, error_range)):
        if( (function(x_1) - function(x_0)) == 0):
            print("Zero denominator error")
            break
        
        x_0 = x_1
        x_1 = x_2
        
        x_2 = x_1 - (function(x_1)*(x_1-x_0))/(function(x_1) - function(x_0))
        
        f_x_2 = function(x_2)
        
    if not zero_denominator_error:
        return x_2