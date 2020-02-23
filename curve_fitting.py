# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:54:51 2019

@author: Ben
"""

# ToC:
# interpolate(x_list, y_list, **kwargs)
    # _lin_function(x_1, y_1, x_2, y_2, x)
    # _linear_interpolation(x_list, y_list, resolution)
    # _get_poly_coeffs(x_list, y_list)
    # _poly_function(coeffs, x)
    # _polynomial_interpolation(x_list, y_list, resolution)
    # _get_spline_coeffs(x_list, y_list)
    # _spline_function(coeffs, x)
    # _spline_interpolation(x_list, y_list, start_2nd_d, end_2nd_d, resolution)
# curve_fit(x_list, y_list, n, resolution)
import numpy as np
import matplotlib.pyplot as plt

# all-purpose interpolation function
def interpolate(x_list, y_list, **kwargs):
    """
    x_list: list - x points
    y_list: list - y poitns
    
    **kwargs:
        interpolation_type: str - "linear", "polynomial", "spline", default is "linear"
        resolution: int - approx density of points per 1 x unit
        start_2nd_d: float - value of first 2nd derivative for cubic spline
        end_2nd_d: float - value of last 2nd derivative for cubic spline
        
    plots scatterplot and graph
    """
    interpolation_type = None
    resolution = 1000 # default resolution
    start_2nd_d = 0 # for cubic spline
    end_2nd_d = 0 
    
    # unpacking **kwargs
    if kwargs is not None:
        for key in kwargs.keys():
            # print("%s == %s" %(key, kwargs[key]))
            if key == 'interpolation_type':
                interpolation_type = kwargs[key]
            elif key == 'resolution':
                resolution = kwargs[key]
            elif key == 'start_2nd_d':
                start_2nd_d = kwargs[key]
            elif key == 'end_2nd_d':
                end_2nd_d = kwargs[key]
                
    if interpolation_type == 'linear':
        print('Using linear interpolation')
        x_plot, y_plot = _linear_interpolation(x_list, y_list, resolution)
        title = 'Linear Interpolation'
        
    elif interpolation_type == 'polynomial':
        print('Using polynomial interpolation')
        x_plot, y_plot = _polynomial_interpolation(x_list, y_list, resolution)
        title = 'Polynomial Interpolation'
        
    elif interpolation_type == 'spline':
        print('Using cubic spline interpolation')
        x_plot, y_plot = _spline_interpolation(x_list, y_list, start_2nd_d, end_2nd_d, resolution)
        title = 'Cubic Spline Interpolation'
        
    else: 
        print("Defaulting to linear interpolation")
        x_plot, y_plot = _linear_interpolation(x_list, y_list, resolution)
        title = 'Linear Interpolation'
        
    print(f"Resolution: {resolution} points per x unit")
        
    plt.scatter(x_list, y_list)
    plt.plot(x_plot, y_plot)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    
    # what about returning thea cutal points? 
    
# linear
def _lin_function(x_1, y_1, x_2,y_2,x):
    """
    x_1: float
    y_1: float
    x_2: float
    y_2: float
    x: float
    
    returns tuple(x_plot:list, y_plot: list)
    """
    return y_1 + (x-x_1)/(x_2-x_1)*(y_2-y_1)

def _linear_interpolation(x_list, y_list, resolution):
    """
    x_list: list - x points
    y_list: list
    resolution: int - approx number of poitns per 1 x unit
    
    returns tuple(x_plot: list, y_plot: list)
    """
    x_plot = []
    y_plot = []
    
    # calculates points interval by interval
    for i in range(len(x_list)-1):
        x_points = np.linspace(x_list[i], x_list[i+1], int(abs(x_list[i+1]-x_list[i])*resolution)) # inclusive
        y_points = _lin_function(x_list[i], y_list[i], x_list[i+1], y_list[i+1], x_points)
        
        x_plot.extend(x_points)
        y_plot.extend(y_points)
        
    return x_plot, y_plot

# polynomial
def _get_poly_coeffs(x_list, y_list):
    """
    x_list: list
    y_list: list
    
    returns polynomial coefficient of length {degree+1}
    
    """
    length = len(x_list)
    A = np.zeros((length,length))
    b = np.zeros((length,1))
    
    for i in range(length):
        b[i] = y_list[i]
        for j in range(length):
            A[i][j] = np.power(x_list[i], length-1-j)
    
    return np.linalg.inv(A).dot(b)

def _poly_function(coeffs, x):
    """
    coeffs: list
    x: float
    calculates y(x) for polynomials of given coefficients
    
    
    """
    length = len(coeffs)
    output = 0
    for i in range(length):
        output += coeffs[i]*np.power(x, length-1-i)
    return output

def _polynomial_interpolation(x_list, y_list, resolution):
    """
    x_list: list - x points
    y_list: list
    resolution: int - approx number of points per 1 x unit
    
    returns tuple(x_plot: list, y_plot: list)
    """
    coeffs = _get_poly_coeffs(x_list, y_list)
    
    x_plot = []
    y_plot = []
    
    # instantiate x points
    for i in range(len(x_list)-1):
        x_points = np.linspace(x_list[i], x_list[i+1], int(abs(xList[i+1]-x_list[i])*resolution))
        y_points = _poly_function(coeffs, x_points)
        
        x_plot.extend(x_points)
        y_plot.extend(y_points)
        
    print(f"Interpolating with polynomial of degree {len(coeffs)-1}")
    return x_plot, y_plot

# spline interpolation
def _get_spline_coeffs(x_list, y_list, start_2nd_d, end_2nd_d):
    """
    # for cubic spline
    
    x_list: list - x points
    y_list: list - y points
    start_2nd_d: float - value of 2nd derivative for first point
    end_2nd_d: float - value of 2nd derivative for last point
    
    returns a vector of a, b, c, d coefficients for each cubic spline function
    """
    
    #Ax = b
    length = len(x_list)
    A = np.zeros( ((length-1)*4, (length-1)*4) )
    b = np.zeros((length-1)*4)
    
    # first 2nd derivative - first row
    A[0,0:2] = [6*x_list[0], 2]
    b[0] = start_2nd_d
    
    # loop over spline itnervals
    for i in range(length-2): # stops at number of points-2, since last point is a special case
        A[1 + 4*i + 0][i*4:(i+1)*4] = [x_list[i]**3, x_list[i]**2, x_list[i], 1]
        b[1 + 4*i + 0] = y_list[i]
        
        A[1 + 4*i + 1][i*4:(i+1)*4] = [3*x_list[i+1]**2, 2*x_list[i+1], 1, 0]
        A[1 + 4*i + 1][(i+1)*4:(i+2)*4] = [-3*x_list[i+1]**2, -2*x_list[i+1], -1, 0] 
        
        A[1 + 4*i + 2][i*4:(i+1)*4] = [6*x_list[i+1], 2, 0, 0]
        A[1 + 4*i + 2][(i+1)*4:(i+2)*4] = [-6*x_list[i+1], -2, 0, 0]
        
        A[1 + 4*i + 3][i*4:(i+1)*4] = [x_list[i+1]**3, x_list[i+1]**2, x_list[i+1], 1]
        b[1 + 4*i + 3] = y_list[i+1] 
    
    # last 3 rows
    
    A[-3][-4:] = [x_list[-2]**3, x_list[-2]**2, x_list[-2], 1]
    b[-3] = y_list[length-2]
    
    A[-2][-4:] = [x_list[-1]**3, x_list[-1]**2, x_list[-1], 1]
    b[-2] = y_list[-1]
    
    A[-1][-4:] = [6*x_list[-1], 2, 0, 0]
    b[-1] = end_2nd_d
    
    return np.linalg.inv(A).dot(b)

def _spline_function(coeffs, x):
    """
    coeffs: list - cubic spline coefficients
    x: float
    
    returns y(x) according to cubic spline coefficients
    """
    a,b,c,d = coeffs
    
    return a*x**3 + b*x**2 + c*x + d

def _spline_interpolation(x_list, y_list, start_2nd_d, end_2nd_d, resolution):
    """
    x_list: list - x points
    y_list: list - y points
    start_2nd_d: float - value of 2nd derivative for first point
    end_2nd_d: float - value of 2nd derivative for last point
    resolution: int - approx number of points per 1 x unit in return tuple
    
    returns tuple (x_plot: list, y_plot: list)
    """
    
    coeffs = _get_spline_coeffs(x_list, y_list, start_2nd_d, end_2nd_d)
    
    x_plot = []
    y_plot = []
    
    for i in range(len(x_list)-1):
        x_points = np.linspace(x_list[i], x_list[i+1], int(abs(x_list[i+1]-x_list[i])*resolution))
        y_points = _spline_function(coeffs[i*4 : (i+1)*4], x_points)
        
        x_plot.extend(x_points)
        y_plot.extend(y_points)
        
    return x_plot, y_plot

# curve fitting
def curve_fit(x_list, y_list, deg, resolution):
    """
    x_list: list - x points
    y_list: list - y points, same length as x_list
    deg: int - degree of polynomial to be fitted with LSR
    resolution: int - approx number of points per x unit
    """
    
    length = len(x_list)
    
    # check so a polynomial of deg degree isn't underfitted
    if deg > length-1:
        print('Error: polynomial is underfit')
        return # blank
    
    # if exact fit or overfit, use pseudoinverse
    else:
        print(f"Curve-fitting using polynomial of degree {deg}")
    
        x_plot = []
        y_plot = []
        
        # get coefficients
        # Ax=b --> x ~ (A^t A)^-1 (A^t) b
        A = np.zeros((length,deg+1))
        b = np.array([y_list]).transpose() # column vector
        
        # create A row by row 
        for i in range(length):
            x_val = x_list[i]
            for j in range(deg):
                A[i][j] = x_val**(deg - j) # also includes ^0, but that's alright for now
        
            A[i][deg] = 1
        
        coeffs = (np.linalg.inv( A.transpose().dot(A) )).dot( (A.transpose()).dot(b) )
             
        # get points
        for i in range(length-1):
            x_points = np.linspace(x_list[i], x_list[i+1], int(abs(x_list[i+1]-x_list[i])*resolution))
            x_plot.extend(x_points)
            
            y_points = _poly_function(coeffs, x_points)
            y_plot.extend(y_points)
    
    return (x_plot, y_plot)