# -*- coding: utf-8 -*-
"""
This module contains functions for neutron unit conversions and calculations related to neutron scattering experiments.

Written by: Nicolai Amin
Date: 2025-05-06
"""
import numpy as np

def E2v_(E):
    """Convert energy to velocity.

    Args:
        E (float): Energy in meV.

    Returns:
        float: Velocity in m/s.
    """
    
    
    return 437.4* np.sqrt(E) 

def v2E_(v):
    """Convert velocity to energy.

    Args:
        v (float): Velocity in m/s.

    Returns:
        float: Energy in meV.
    """
    return (v/437.4)**2 

def E2k_(E):
    """Convert energy to wavevector.

    Args:
        E (float): Energy in meV.

    Returns:
        float: Wavevector in 1/Å.
    """
    return 0.6947 * np.sqrt(E) 

def k2E_(k):
    """Convert wavevector to energy.
    
    Args:
        k (float): Wavevector in 1/Å.
        
    Returns:
        float: Energy in meV.
    """
    return (k/0.6947)**2 

def v2k_(v):
    """Convert velocity to wavevector.
    
    Args:
        v (float): Velocity in m/s.
        
    Returns:    
        float: Wavevector in 1/Å.
    """
    return v *1.588*10**(-3) 

def k2v_(k):
    """Convert wavevector to velocity.
    
    Args:
        k (float): Wavevector in 1/Å.
        
    Returns:
        float: Velocity in m/s.
    """
    return k*629.6 

def lambda2E_(L):
    """Convert wavelength to energy.
    
    Args:   
        L (float): Wavelength in Å.
    
    Returns:    
        float: Energy in meV.
    """
    return (9.045/L)**2

def E2lambda_(E):
    """Convert energy to wavelength.
    
    Args:
        E (float): Energy in meV.
        
    Returns:    
        float: Wavelength in Å.
    """ 
    return 9.045/np.sqrt(E) 

def lambda2v_(L):
    """Convert wavelength to velocity.
    
    Args:
        L (float): Wavelength in Å.
    
    Returns:    
        float: Velocity in m/s.
    """
    return 3956.0/L 

def v2lambda_(v):
    """Convert velocity to wavelength.
    
    Args:
        v (float): Velocity in m/s.
    
    Returns:    
        float: Wavelength in Å.
    """
    return 3956.0/v 

def lambda2k_(L):
    """Convert wavelength to wavevector.
    
    Parameters:
    L (float): Wavelength in Å.
    
    Returns:
    float: Wavevector in 1/Å.
    """
    return 2*np.pi/L

def k2lambda_(k):
    """
    Convert wavevector to wavelength.
    
    Parameters:
    k (float): Wavevector in 1/Å.
    
    Returns:
    float: Wavelength in Å.
    """
    return 2*np.pi/k 

def theta_Bragg(L, d):
    """
    Calculate the Bragg angle for a given lattice spacing and wavelength.

    Parameters:
    d (float): Lattice spacing.
    L (float): Wavelength.

    Returns:
    float: Bragg angle in radians.
    """
    return np.arcsin(L / (2 * d))

def lambda_Bragg(d, theta):
    """
    Calculate the wavelength for a given lattice spacing and Bragg angle.

    Parameters:
    d (float): Lattice spacing.
    theta (float): Bragg angle in radians.

    Returns:
    float: Wavelength.
    """
    return 2 * d * np.sin(theta)

def d_Bragg(L, theta):
    """
    Calculate the lattice spacing for a given wavelength and Bragg angle.

    Parameters:
    L (float): Wavelength.
    theta (float): Bragg angle in radians.

    Returns:
    float: Lattice spacing.
    """
    return L / (2 * np.sin(theta))
