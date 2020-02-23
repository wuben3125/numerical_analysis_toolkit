# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:22:19 2019

@author: Ben
"""

# ToC
# naive_mult(first, second)
# strassen_mult_single(a,b)
# strassen_mult_recursive(a, b, threshold)

import numpy as np

def naive_mult(first, second):
    """
    first: np.ndarray or 2D list
    second: np.ndarray or 2D list
    
    returns product
    """
    
    # check dimensions
    if len(first[0]) == len(second):
        product = np.zeros((len(first), len(second[0])))
#        length = len(first[0])
        
        for i in range(len(first)):
            for j in range(len(second[0])):
#                for k in range(length):
#                    product[i][j] += first[i][k] * second[k][j]
                product[i][j] = np.dot(first[i], second[:][j])
                
        return product
        
    else:
        print("Incompatible dimensions")
        
def strassen_mult_single(a,b):
    """
    first: np.ndarray or 2D list - has even dimensions
    second: np.ndarray or 2D list - has even dimensions
    
    returns product
    """
    
    # dimension checking
    if len(a)==len(a[0])==len(b)==len(b[0]) and len(a)%2==0:
        length = len(a)
        
        a_1_1= a[:length//2, :length//2]
        a_1_2= a[:length//2, length//2:]
        a_2_1= a[length//2:, :length//2]
        a_2_2= a[length//2:, length//2:]
        
        b_1_1= b[:length//2, :length//2]
        b_1_2= b[:length//2, length//2:]
        b_2_1= b[length//2:, :length//2]
        b_2_2= b[length//2:, length//2:]
        
        m_1 = naive_mult((a_1_1 + a_2_2), (b_1_1 + b_2_2))
        m_2 = naive_mult((a_2_1 + a_2_2), b_1_1)
        m_3 = naive_mult(a_1_1, (b_1_2 - b_2_2))
        m_4 = naive_mult(a_2_2, (b_2_1 - b_1_1))
        m_5 = naive_mult((a_1_1 + a_1_2), b_2_2)
        m_6 = naive_mult((a_2_1 - a_1_1), (b_1_1 + b_1_2))
        m_7 = naive_mult((a_1_2 - a_2_2), (b_2_1 + b_2_2))
        
        
        c = np.zeros((length, length))
        
        c[:length//2, :length//2] = m_1 + m_4 - m_5 + m_7
        c[:length//2, length//2:] = m_3 + m_5
        c[length//2:, :length//2] = m_2 + m_4
        c[length//2:, length//2:] = m_1 - m_2 + m_3 + m_6
        
        return c
            
    else:
        print("Invalid dimensions")
        
def strassen_mult_recursive(a, b, threshold):
    """
    a: np.ndarray - nxn matrix
    b: np.ndarray - nxn matrix
    threshold: int 
    
    """
    # error checking
    if len(a)!=len(b) or len(a[0])!=len(b[0]):
        print("Error: mismatched matrix bounds")
        return None    
    
    if len(a) < threshold:
        return naive_mult(a,b)     

    elif len(a)%2==1:  # base case of odd dimensions
        return naive_mult(a,b)
        
    else:
        length = len(a)
        c = np.zeros((length, length))

        a_1_1= a[:length//2, :length//2]
        a_1_2= a[:length//2, length//2:]
        a_2_1= a[length//2:, :length//2]
        a_2_2= a[length//2:, length//2:]

        b_1_1= b[:length//2, :length//2]
        b_1_2= b[:length//2, length//2:]
        b_2_1= b[length//2:, :length//2]
        b_2_2= b[length//2:, length//2:] 

        m_1 = strassen_mult_recursive((a_1_1 + a_2_2), (b_1_1 + b_2_2), threshold)
        m_2 = strassen_mult_recursive((a_2_1 + a_2_2), b_1_1, threshold)
        m_3 = strassen_mult_recursive(a_1_1, (b_1_2 - b_2_2), threshold)
        m_4 = strassen_mult_recursive(a_2_2, (b_2_1 - b_1_1), threshold)
        m_5 = strassen_mult_recursive((a_1_1 + a_1_2), b_2_2, threshold)
        m_6 = strassen_mult_recursive((a_2_1 - a_1_1), (b_1_1 + b_1_2), threshold)
        m_7 = strassen_mult_recursive((a_1_2 - a_2_2), (b_2_1 + b_2_2), threshold)

        c[:length//2, :length//2] = m_1 + m_4 - m_5 + m_7
        c[:length//2, length//2:] = m_3 + m_5
        c[length//2:, :length//2] = m_2 + m_4
        c[length//2:, length//2:] = m_1 - m_2 + m_3 + m_6

        return c
