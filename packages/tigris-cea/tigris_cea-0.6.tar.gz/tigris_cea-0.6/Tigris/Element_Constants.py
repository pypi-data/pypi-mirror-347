# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
from Element import Element
from utils import round_to_fmt
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Constant(Element) :
    
    #==========================================================================
    ATTR_VALUE = 'value'
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.value = None
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        self.icon = "constant"
        
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'value' in kwargs.keys() :
            self.value = kwargs['value']
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - valeur".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.value))
        
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        gp.setncattr(Constant.ATTR_VALUE, self.value)
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        self.value = gp.getncattr(Constant.ATTR_VALUE)
    
    #==========================================================================
    def get_dimensions(self) :
        #----------------------------------------------------------------------
        return []
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Vector(Element) :
    
    #==========================================================================
    ATTR_DIM     = "dimension"
    VALUES_NAME  = "values"
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.dimension = None
        self.values    = None
        self.N         = None
        self.lims      = {} # défini manuellement, min et max suivant d'autres dimensions
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        self.icon = 'mesh'
    
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'dimension' in kwargs.keys() :
            self.dimension = kwargs['dimension']
            
        #----------------------------------------------------------------------
        if 'values' in kwargs.keys() :
            self.values = np.array(kwargs['values'])
            self.N = len(self.values)
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - dimension".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.dimension))
        print("   - valeurs".ljust(Element.DETAILS_ALIGN,' ')+": {} valeur(s), [{:.5G} -> {:.5G}]".format(self.N, np.nanmin(self.values), np.nanmax(self.values)))
        
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        gp.setncattr(Mesh.ATTR_DIM, self.dimension)
        #----------------------------------------------------------------------
        gp.createDimension(Vector.VALUES_NAME, self.N)
        values_var = gp.createVariable(Vector.VALUES_NAME, 'f', dimensions=(Vector.VALUES_NAME,), zlib=True)
        values_var[:] = self.values[:]
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        self.dimension = gp.getncattr(Vector.ATTR_DIM)
        self.values = round_to_fmt(gp.variables[Vector.VALUES_NAME][:])
        self.N = len(self.values)
        
    #==========================================================================
    def coord_to_index(self, x, mode='best', allow_out=True) :
        #----------------------------------------------------------------------
        if mode == 'exact' :
            try : return int(np.where(self.values==x)[0][0])
            except : return None
            
        #----------------------------------------------------------------------
        elif mode == 'best' :
            X = self.values
            if x < X[0] : return 0 if allow_out else None
            if x > X[-1] : return self.N-1 if allow_out else None
            i = np.where(X<=x)[0][-1]
            if abs(X[i+1]-x) < abs(X[i]-x) : i += 1
            return i
            
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def get_dimensions(self) : return []
    def set_lims(self, lims) : self.lims = lims.copy()
    def get_lims(self, axis) : return self.lims.get(axis,(None,None))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Mesh(Element) :
    
    #==========================================================================
    ATTR_DIM     = "dimension"
    EDGES_NAME   = "edges"
    CENTERS_NAME = "centers"
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.dimension = None
        self.edges     = None
        self.centers   = None
        self.N         = None
        self.lims      = {} # défini manuellement, min et max suivant d'autres dimensions
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        self.icon = 'mesh'
    
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'dimension' in kwargs.keys() :
            self.dimension = kwargs['dimension']
            
        #----------------------------------------------------------------------
        if 'edges' in kwargs.keys() :
            self.edges = np.array(kwargs['edges'])
            self.N = len(self.edges)-1
            
        #----------------------------------------------------------------------
        if 'centers' in kwargs.keys() :
            self.centers = np.array(kwargs['centers'])
            self.N = len(self.centers)
            
        #----------------------------------------------------------------------
        if self.centers is None and self.edges is not None :
            self.centers = np.round((self.edges[1:]+self.edges[:-1])/2.0, 5)
            
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - dimension".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.dimension))
        print("   - valeurs".ljust(Element.DETAILS_ALIGN,' ')+": {} maille(s), [{:.5G} -> {:.5G}]".format(self.N, self.edges[0], self.edges[-1]))
    
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        gp.setncattr(Mesh.ATTR_DIM, self.dimension)
        #----------------------------------------------------------------------
        gp.createDimension(Mesh.EDGES_NAME, self.N+1)
        edges_var = gp.createVariable(Mesh.EDGES_NAME, 'f', dimensions=(Mesh.EDGES_NAME,), zlib=True)
        edges_var[:] = self.edges[:]
        #----------------------------------------------------------------------
        gp.createDimension(Mesh.CENTERS_NAME, self.N)
        centers_var = gp.createVariable(Mesh.CENTERS_NAME, 'f', dimensions=(Mesh.CENTERS_NAME,), zlib=True)
        centers_var[:] = self.centers[:]
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        self.dimension = gp.getncattr(Mesh.ATTR_DIM)
        self.edges = round_to_fmt(gp.variables[Mesh.EDGES_NAME][:])
        self.centers = round_to_fmt(gp.variables[Mesh.CENTERS_NAME][:])
        self.N = len(self.centers)
        
    #==========================================================================
    def coord_to_index(self, x, mode='best', allow_out=False) :
        """
        mode :
            - left   : bordure min
            - center : centre
            - right  : bordure max
            - best   : maille la plus proche
        """
        #----------------------------------------------------------------------
        if mode == 'best' :
            X = self.edges
            if x < X[0] : return 0 if allow_out else None
            if x > X[-1] : return self.N-1 if allow_out else None
            return np.where(X<=x)[0][-1]
        
        #----------------------------------------------------------------------
        else :
            try :
                if   mode == 'center' : i = int(np.where(self.centers    == x)[0][0])
                elif mode == 'left'   : i = int(np.where(self.edges[:-1] == x)[0][0])
                elif mode == 'right'  : i = int(np.where(self.edges[1:]  == x)[0][0])
                return i
            except : return None
            
        #----------------------------------------------------------------------
        return None
    
    #==========================================================================
    def get_dimensions(self) : return []
    def set_lims(self, lims) : self.lims = lims.copy()
    def get_lims(self, axis) : return self.lims.get(axis,(None,None))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
