# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
from copy import deepcopy
from itertools import product
from netCDF4 import Dataset
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Mesh
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Cuboid(Element) :
    
    #==========================================================================
    ATTR_COORDS  = 'COORDS'
    ATTR_INDICES = 'INDICES'
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.coordinates = None
        self.indices     = None
        self.axes_paths  = None
        self.value       = np.nan
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        self.icon = 'cube'
        
        #----------------------------------------------------------------------
        self.set_style(edge_color='white', face_color=None)
        
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'coordinates' in kwargs.keys() : # x0,x1,y0,y1,z0,z1
            self.coordinates = kwargs['coordinates']
            
        #----------------------------------------------------------------------
        if 'indices' in kwargs.keys() : # i0,i1,j0,j1,k0,k1
            self.indices = kwargs['indices']
            
        #----------------------------------------------------------------------
        if 'axes_paths' in kwargs.keys() :
            self.axes_paths = deepcopy(kwargs['axes_paths'])
            
        #----------------------------------------------------------------------
        if 'value' in kwargs.keys() :
            self.value = kwargs['value']
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - coordonnées".ljust(Element.DETAILS_ALIGN,' ')+": x=[{}:{}], y=[{}:{}], z=[{}:{}]".format(*self.coordinates))
        print("   - indices".ljust(Element.DETAILS_ALIGN,' ')+": i=[{}:{}], j=[{}:{}], k=[{}:{}]".format(*[i+1 for i in self.indices]))
        print("   - valeur".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.value))
        
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        gp.setncattr(Cuboid.ATTR_COORDS, self.coordinates)
        gp.setncattr(Cuboid.ATTR_INDICES, [int(v) for v in self.indices])
        
        #----------------------------------------------------------------------
        if self.axes_paths is not None :
            for dim,axe_path in self.axes_paths.items() :
                gp.setncattr(Element.PREFIX_AXE_PATH+dim, self.axes_paths[dim])
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        self.coordinates = gp.getncattr(Cuboid.ATTR_COORDS)
        self.indices     = gp.getncattr(Cuboid.ATTR_INDICES)
    
        #----------------------------------------------------------------------
        self.axes_paths = {}
        for k in gp.ncattrs() :
            value = gp.getncattr(k)
            if k.startswith(Element.PREFIX_AXE_PATH) :
                dim = k.replace(Element.PREFIX_AXE_PATH,'')
                self.axes_paths[dim] = value
                
    #==========================================================================
    def coord_to_index(self, dim, x, allow_out=False) :
        #----------------------------------------------------------------------
        self.load_axes()
        if dim not in self.axes.keys() : return None
        
        #----------------------------------------------------------------------
        X = self.axes[dim]
        N = len(X)-1
        #----------------------------------------------------------------------
        if x < X[0]  : return 0 if allow_out else None
        if x > X[-1] : return N if allow_out else None
        #----------------------------------------------------------------------
        return np.where(X<=x)[0][-1]
    
    #==========================================================================
    def load_axes(self) :
        #----------------------------------------------------------------------
        self.axes = {}
        
        ds = Dataset(self.loaded_nc, 'r')
        #----------------------------------------------------------------------
        for dim,path in self.axes_paths.items() :
            gp = ds
            for gp_name in path : gp = gp.groups[gp_name]
            etype = gp.getncattr(Element.ATTR_ELEMENT)
            if etype == 'Mesh' :
                self.axes[dim] = np.array(gp.variables[Mesh.EDGES_NAME][:])
                if dim not in self.edge_axes : self.edge_axes.append(dim)
            else : raise Exception("le type d'élément '{}' n'est pas implémenté pour un axe de matrice".format(etype))
        #----------------------------------------------------------------------
        ds.close()
        
    #==========================================================================
    def split(self, M) :
        #----------------------------------------------------------------------
        i0,i1,j0,j1,k0,k1 = self.indices
        #----------------------------------------------------------------------
        I = np.unique(np.vstack((M[:,0],M[:,1]+1)))
        J = np.unique(np.vstack((M[:,2],M[:,3]+1)))
        K = np.unique(np.vstack((M[:,4],M[:,5]+1)))
        #----------------------------------------------------------------------
        DI = [(I[i],I[i+1]-1) for i in range(len(I)-1) if I[i]>= i0 and I[i+1]-1 <= i1]
        DJ = [(J[j],J[j+1]-1) for j in range(len(J)-1) if J[j]>= j0 and J[j+1]-1 <= j1]
        DK = [(K[k],K[k+1]-1) for k in range(len(K)-1) if K[k]>= k0 and K[k+1]-1 <= k1]
        #----------------------------------------------------------------------
        cuboids = [(*di,*dj,*dk) for di,dj,dk in product(DI,DJ,DK)]
        return cuboids
        
    #==========================================================================
    def get_dimensions(self) :
        #----------------------------------------------------------------------
        return ['X','Y','Z']
    
    #==========================================================================
    def contains(self, i,j,k) :
        #----------------------------------------------------------------------
        i0,i1,j0,j1,k0,k1 = self.indices
        #----------------------------------------------------------------------
        if i < i0 : return False
        if i > i1 : return False
        if j < j0 : return False
        if j > j1 : return False
        if k < k0 : return False
        if k > k1 : return False
        #----------------------------------------------------------------------
        return True
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PolyCuboid(Element) :
    
    #==========================================================================
    ATTR_SUB_PREFIX = "SUB_ELEMENT_"
    ATTR_OPERATION  = "OPERATION"
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.operation    = None
        self.sub_paths    = None
        self.sub_elements = None
        self.axes_paths   = None
        self.value        = None
        
        #----------------------------------------------------------------------
        self.cuboids      = None
        self.coordinates  = None
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        self.icon = 'polycube'
        
        #----------------------------------------------------------------------
        self.set_style(edge_color='white', face_color=None)
        
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'operation' in kwargs.keys() :
            if kwargs['operation'] not in ['UNION','INTER','NOT_INTER'] :
                raise Exception("l'opération '{}' est invalide".format(kwargs['operation']))
                
            self.operation = kwargs['operation']
            
        #----------------------------------------------------------------------
        if 'sub_paths' in kwargs.keys() :
            self.sub_paths = kwargs['sub_paths']
            
        #----------------------------------------------------------------------
        if 'sub_elements' in kwargs.keys() :
            self.sub_elements = kwargs['sub_elements']
            
        #----------------------------------------------------------------------
        if 'axes_paths' in kwargs.keys() :
            self.axes_paths = deepcopy(kwargs['axes_paths'])
            
        #----------------------------------------------------------------------
        if 'value' in kwargs.keys() :
            self.value = kwargs['value']
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - operation".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.operation))
        print("   - elements".ljust(Element.DETAILS_ALIGN,' ')+": {}".format([e.label for e in self.sub_elements]))
        print("   - valeur".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.value))
        
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        for i,sub_path in enumerate(self.sub_paths) :
            gp.setncattr(PolyCuboid.ATTR_SUB_PREFIX+str(i), sub_path)
            
        #----------------------------------------------------------------------
        gp.setncattr(PolyCuboid.ATTR_OPERATION, self.operation)
        
        #----------------------------------------------------------------------
        for dim,axe_path in self.axes_paths.items() :
            gp.setncattr(Element.PREFIX_AXE_PATH+dim, self.axes_paths[dim])
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        sub_paths = []
        self.axes_paths = {}
        
        #----------------------------------------------------------------------
        for k in gp.ncattrs() :
            value = gp.getncattr(k)
            if k.startswith(PolyCuboid.ATTR_SUB_PREFIX) :
                i = int(k.replace(PolyCuboid.ATTR_SUB_PREFIX,''))
                sub_paths.append((i,value))
            elif k.startswith(Element.PREFIX_AXE_PATH) :
                dim = k.replace(Element.PREFIX_AXE_PATH,'')
                self.axes_paths[dim] = value
                
        #----------------------------------------------------------------------
        self.sub_paths = [e[1] for e in sorted(sub_paths, key=lambda e:e[0])]
        self.operation = gp.getncattr(PolyCuboid.ATTR_OPERATION)
        
    #==========================================================================
    def coord_to_index(self, dim, x, allow_out=False) :
        #----------------------------------------------------------------------
        self.load_axes()
        if dim not in self.axes.keys() : return None
        
        #----------------------------------------------------------------------
        X = self.axes[dim]
        N = len(X)-1
        #----------------------------------------------------------------------
        if x < X[0] : return 0 if allow_out else None
        if x > X[-1] : return N if allow_out else None
        #----------------------------------------------------------------------
        return np.where(X<=x)[0][-1]
    
    #==========================================================================
    def load_axes(self) :
        #----------------------------------------------------------------------
        self.axes = {}
        ds = Dataset(self.loaded_nc, 'r')
        
        #----------------------------------------------------------------------
        for dim,path in self.axes_paths.items() :
            gp = ds
            for gp_name in path : gp = gp.groups[gp_name]
            etype = gp.getncattr(Element.ATTR_ELEMENT)
            if etype == 'Mesh' :
                self.axes[dim] = np.array(gp.variables[Mesh.EDGES_NAME][:])
                if dim not in self.edge_axes : self.edge_axes.append(dim)
            else : raise Exception("le type d'élément '{}' n'est pas implémenté pour un axe de matrice".format(etype))
            
        #----------------------------------------------------------------------
        ds.close()
        
    #==========================================================================
    def get_sub_indices(self) :
        #----------------------------------------------------------------------
        indices = []
        for sub in self.sub_elements :
            if isinstance(sub, Cuboid) : indices.append(sub.indices)
            else : indices += sub.get_sub_indices()
        return indices
        
    #==========================================================================
    def compute_cuboids(self) :
        #----------------------------------------------------------------------
        if self.cuboids is not None : return
        
        #----------------------------------------------------------------------
        self.load_axes()
        M = np.array(self.get_sub_indices())
        
        #----------------------------------------------------------------------
        cuboids = []
        counts  = {}
        for sub in self.sub_elements :
            if isinstance(sub, Cuboid) :
                _cuboids = sub.split(M)
                
            if isinstance(sub, PolyCuboid) :
                sub.compute_cuboids()
                _cuboids = sub.cuboids
                
            for cuboid in _cuboids :
                if cuboid not in cuboids :
                    cuboids.append(cuboid)
                    counts[cuboid] = 0
                counts[cuboid] += 1
                
        #----------------------------------------------------------------------
        if   self.operation == 'UNION'     : self.cuboids = cuboids
        elif self.operation == 'NOT_INTER' : self.cuboids = [cuboid for cuboid in cuboids if counts[cuboid] == 1]
        elif self.operation == 'INTER'     : self.cuboids = [cuboid for cuboid in cuboids if counts[cuboid] > 1]
        
        #----------------------------------------------------------------------
        self.coordinates = []
        for i0,i1,j0,j1,k0,k1 in self.cuboids :
            x0 = self.axes['X'][i0]
            x1 = self.axes['X'][i1+1]
            y0 = self.axes['Y'][j0]
            y1 = self.axes['Y'][j1+1]
            z0 = self.axes['Z'][k0]
            z1 = self.axes['Z'][k1+1]
            self.coordinates.append((x0,x1,y0,y1,z0,z1))
        
    #==========================================================================
    def get_dimensions(self) :
        #----------------------------------------------------------------------
        return ['X','Y','Z']
    
    #==========================================================================
    def contains(self, i,j,k) :
        #----------------------------------------------------------------------
        N = len([sub for sub in self.sub_elements if sub.contains(i,j,k)])
        
        #----------------------------------------------------------------------
        if   self.operation == 'UNION'     : return N > 0
        elif self.operation == 'NOT_INTER' : return N == 1
        elif self.operation == 'INTER'     : return N > 1
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


