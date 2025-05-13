# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import numpy as np
import datetime
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def to_float(value, default=None) :
    try : return float(value)
    except : return default
    
#==============================================================================
def round_to_fmt(M, dtype=None, fmt='{:.6G}') :
    #--------------------------------------------------------------------------
    if dtype is not None : M = np.array(M, dtype=dtype)
    return np.reshape([float(fmt.format(v)) for v in np.ravel(M)], M.shape)
    
#==============================================================================
def get_temp_dir(dirpath) :
    #--------------------------------------------------------------------------
    _dirpath = os.path.join(dirpath, "_TEMP")
    os.makedirs(_dirpath, exist_ok=True)
    return _dirpath

#==============================================================================
def get_temp_path(dirpath, name=None, element=None) :
    #--------------------------------------------------------------------------
    _dirpath = get_temp_dir(dirpath)
    if element is not None : return os.path.join(_dirpath, "_".join(element.path)+".tmp")
    if name    is not None : return os.path.join(_dirpath, "_".join(name)+".tmp")

#==============================================================================
def get_icon_path(name) :
    #--------------------------------------------------------------------------
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icons", "{}.png".format(name))
    if os.path.exists(path) : return path
    return None

#==============================================================================
def get_now(local=False, fmt=None) :
    #--------------------------------------------------------------------------
    if local : dt = datetime.datetime.now()
    else :
        try : dt = datetime.datetime.now(datetime.UTC)
        except : dt = datetime.datetime.utcnow()
    
    if fmt is not None : return dt.strftime(fmt)
    return dt
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

