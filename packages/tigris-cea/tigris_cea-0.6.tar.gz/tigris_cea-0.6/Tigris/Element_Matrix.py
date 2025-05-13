# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import numpy as np
from copy import deepcopy
from netCDF4 import Dataset
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Mesh,Vector
from utils import round_to_fmt
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Matrix(Element) :
    
    #==========================================================================
    ATTR_DTYPE        = 'DTYPE'
    ATTR_VMIN         = 'VMIN'
    ATTR_VMAX         = 'VMAX'
    ATTR_ICONS        = 'ICONS'
    ATTR_STAGS        = "STAGS"
    FIELDS_NAME       = 'FIELDS'
    VAR_MATRIX        = 'matrix'
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.dimensions      = None
        self.axes_paths      = None
        self.axes_stags      = None
        self.sizes           = None
        self.dtype           = 'float32'
        self.null_value      = np.nan
        self.vmin            = None
        self.vmax            = None
        self.vmins           = None
        self.vmaxs           = None
        self.linked_elements = None
        #----------------------------------------------------------------------
        self.M = None
        
        #----------------------------------------------------------------------
        Element.__init__(self, **kwargs)
        
    #==========================================================================
    def _configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'dimensions'      in kwargs.keys() : self.dimensions      = kwargs['dimensions'].copy()
        if 'axes'            in kwargs.keys() : self.axes            = deepcopy(kwargs['axes'])
        if 'axes_paths'      in kwargs.keys() : self.axes_paths      = deepcopy(kwargs['axes_paths'])
        if 'axes_stags'      in kwargs.keys() : self.axes_stags      = deepcopy(kwargs['axes_stags'])
        if 'sizes'           in kwargs.keys() : self.sizes           = deepcopy(kwargs['sizes'])
        if 'dtype'           in kwargs.keys() : self.dtype           = kwargs['dtype']
        if 'null_value'      in kwargs.keys() : self.null_value      = kwargs['null_value']
        if 'vmin'            in kwargs.keys() : self.vmin            = kwargs['vmin']
        if 'vmax'            in kwargs.keys() : self.vmax            = kwargs['vmax']
        if 'linked_elements' in kwargs.keys() : self.linked_elements = deepcopy(kwargs['linked_elements'])
        
        #----------------------------------------------------------------------
        if 'M' in kwargs.keys() :
            M = np.array(kwargs['M'])
            if self.sizes is None : self.sizes = {dim:M.shape[d] for d,dim in enumerate(self.dimensions)}
            self.create(kwargs.get('array_path'))
            self.M[:] = M[:]
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        field = kwargs.pop('field',None)
        if field is not None :
            print("   - sous-élément".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(field))
            
        #----------------------------------------------------------------------
        print("   - dimensions".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.dimensions))
        self.load_axes()
        for dim in self.dimensions :
            if dim in self.axes :
                print("   - axe {}".format(dim).ljust(Element.DETAILS_ALIGN,' ')+": {} {}, [{:.5G} -> {:.5G}]".format(self.sizes[dim],
                                                                                                                      "maille(s)" if dim in self.edge_axes else 'valeur(s)',
                                                                                                                      np.nanmin(self.axes[dim]), np.nanmax(self.axes[dim])))
        #----------------------------------------------------------------------
        vmin,vmax = self.get_range(field)
        # print(vmin,vmax)
        # if field is not None :
            # f = self.get_field_index(field)
            # vmin,vmax = self.vmins[f], self.vmaxs[f]
        # else : vmin,vmax  = self.vmin, self.vmax
        print("   - valeurs".ljust(Element.DETAILS_ALIGN,' ')+": [{:.5G} -> {:.5G}]".format(vmin, vmax))
        
        #----------------------------------------------------------------------
        if self.get_attribute(Element.ATTR_COMPUTED, False) :
            print("   - formule".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.get_attribute(Element.ATTR_FORMULA)))
            print("   - balises :")
            for k,v in self.attributes.items() :
                if k.startswith(Element.PREFIX_BEACON+"_") :
                    beacon = k.replace(Element.PREFIX_BEACON+"_", '')
                    print("      - {} -> {}".format(beacon, v))
        
    #==========================================================================
    def set_attributes(self, **kwargs) :
        #----------------------------------------------------------------------
        Element.set_attributes(self, **kwargs)
        
        #----------------------------------------------------------------------
        k = Matrix.FIELDS_NAME.lower()
        if k in self.attributes.keys() and type(self.attributes[k]) == str : self.attributes[k] = [self.attributes[k]]
        
    #==========================================================================
    def create(self, array_path=None) :
        #----------------------------------------------------------------------
        if None in [self.sizes,self.dimensions,self.null_value,self.dtype] :
            return
        
        #----------------------------------------------------------------------
        shape = tuple([self.sizes[dim] for dim in self.dimensions])
        
        #----------------------------------------------------------------------
        if array_path is not None :
            if os.path.exists(array_path) : os.remove(array_path)
            self.M = np.memmap(array_path, dtype=self.dtype, mode='w+', shape=shape)
            return array_path
        
        #----------------------------------------------------------------------
        else :
            self.M = np.full(shape, self.null_value, dtype=self.dtype)
        
    #==========================================================================
    def _save(self, gp) :
        #----------------------------------------------------------------------
        gp.setncattr(Matrix.ATTR_DTYPE, self.dtype)
        
        #----------------------------------------------------------------------
        for dim in self.dimensions :
            gp.createDimension(dim, self.sizes[dim])
            
            if self.axes is not None and dim in self.axes.keys() :
                N_axe = len(self.axes[dim])
                if N_axe == self.sizes[dim]+1 :
                    gp.createDimension(dim+"_stag", N_axe)
                    # dim_var = gp.createVariable(dim+"_stag", 'f', dimensions=(dim+"_stag",), zlib=True)
                    dim_var = gp.createVariable(dim, 'f', dimensions=(dim+"_stag",), zlib=True)
                else :
                    dim_var = gp.createVariable(dim, 'f', dimensions=(dim,), zlib=True)
                dim_var[:] = self.axes[dim][:]
                
            if self.axes_paths is not None and dim in self.axes_paths.keys() :
                gp.setncattr(Element.PREFIX_AXE_PATH+dim, self.axes_paths[dim])
                
            if self.axes_stags is not None :
                gp.setncattr(Matrix.ATTR_STAGS, self.axes_stags)
            
        #----------------------------------------------------------------------
        if self.M is None : self.load_matrix()
        
        dtype_np = Element.DTYPES[self.dtype]['np']
        matrix_var = gp.createVariable(Matrix.VAR_MATRIX, dtype_np, dimensions=tuple(self.dimensions), fill_value=self.null_value, zlib=True)
        matrix_var[:] = self.M[:]
        
        if Matrix.FIELDS_NAME in self.dimensions :
            icons = []
            vmins,vmaxs = [],[]
            for f,field in enumerate(self.get_fields()) :
                
                indices = []
                for dim in self.dimensions :
                    if dim == Matrix.FIELDS_NAME : indices.append(f)
                    else : indices.append(slice(0,self.sizes[dim],1))
                    
                m = self.get_matrix_data(indices)
                vmin = np.nanmin(m)
                vmax = np.nanmax(m)
                
                vmins.append(vmin)
                vmaxs.append(vmax)
            
                if vmin != vmax :
                    if len(self.dimensions) == 2 : icons.append('curve')
                    else : icons.append('matrix')
                else :
                    if vmin == 0.0 : icons.append('null')
                    else : icons.append('constant')
                
            gp.setncattr(Matrix.ATTR_ICONS, icons)
            gp.setncattr(Matrix.ATTR_VMIN, vmins)
            gp.setncattr(Matrix.ATTR_VMAX, vmaxs)
                
        #----------------------------------------------------------------------
        else :
            if self.vmin is None : self.vmin = np.nanmin(self.M)
            if self.vmax is None : self.vmax = np.nanmax(self.M)
            gp.setncattr(Matrix.ATTR_VMIN, self.vmin)
            gp.setncattr(Matrix.ATTR_VMAX, self.vmax)
            
        #----------------------------------------------------------------------
        self.M = None # pour libérer le fichier tmp
        
    #==========================================================================
    def _load(self, gp) :
        #----------------------------------------------------------------------
        matrix_var = gp.variables[Matrix.VAR_MATRIX]
        
        #----------------------------------------------------------------------
        self.dimensions = []
        self.axes = {}
        self.axes_paths = {}
        self.sizes = {}
        #----------------------------------------------------------------------
        for dim in matrix_var.dimensions :
            self.dimensions.append(dim)
            self.sizes[dim] = gp.dimensions[dim].size
            
            if dim in gp.variables.keys() : # axe local
                self.axes[dim] = round_to_fmt(gp.variables[dim][:])
                
                if dim not in self.edge_axes and len(self.axes[dim]) == self.sizes[dim]+1 :
                    self.edge_axes.append(dim)
                
            if Element.PREFIX_AXE_PATH+dim in gp.ncattrs() : # axe global
                self.axes_paths[dim] = gp.getncattr(Element.PREFIX_AXE_PATH+dim)
            
            if Matrix.ATTR_STAGS in gp.ncattrs() :
                self.axes_stags = gp.getncattr(Matrix.ATTR_STAGS)
            
        #----------------------------------------------------------------------
        self.dtype      = gp.getncattr(Matrix.ATTR_DTYPE)
        self.null_value = matrix_var._FillValue
        self.field_icons = None
        if Matrix.ATTR_ICONS in gp.ncattrs() :
            self.field_icons = gp.getncattr(Matrix.ATTR_ICONS)
            if type(self.field_icons) == str : self.field_icons = [gp.getncattr(Matrix.ATTR_ICONS)]
        
        #----------------------------------------------------------------------
        if Matrix.FIELDS_NAME in self.dimensions :
            self.vmins = gp.getncattr(Matrix.ATTR_VMIN)
            self.vmaxs = gp.getncattr(Matrix.ATTR_VMAX)
            
            # print(type(self.vmins), self.vmins.shape)
            
            if type(self.vmins) == np.float32 :
                self.vmins = [self.vmins]
                self.vmaxs = [self.vmaxs]
        else :
            self.vmin = gp.getncattr(Matrix.ATTR_VMIN)
            self.vmax = gp.getncattr(Matrix.ATTR_VMAX)
            
        #----------------------------------------------------------------------
        self.M = None
        
        #----------------------------------------------------------------------
        if self.get_attribute(Element.ATTR_COMPUTED,False) : self.icon = 'combiner' 
        elif len(self.dimensions) == 1 : self.icon = 'curve'
        else : self.icon = 'matrix'
        
    #==========================================================================
    def coord_to_index(self, dim, x, allow_out=False) :
        #----------------------------------------------------------------------
        self.load_axes()
        if dim not in self.axes : return None
        
        #----------------------------------------------------------------------
        X = self.axes[dim]
        #----------------------------------------------------------------------
        if dim in self.edge_axes : N = len(X)-2
        else : N = len(X)-1
        #----------------------------------------------------------------------
        if x < X[0] : return 0 if allow_out else None
        if x > X[-1] : return N if allow_out else None
        #----------------------------------------------------------------------
        i = np.where(X<=x)[0][-1]
        if dim not in self.edge_axes and x-X[i] > X[i+1]-x : i += 1
        return i
        
    #==========================================================================
    def get_indices(self, positions=None, graph_dimensions=None, searches={}, field=None) :
        #----------------------------------------------------------------------
        indices = []
        for dim in self.dimensions :
            
            if positions is None :
                if dim == Matrix.FIELDS_NAME : i = self.get_field_index(field)
                else : i = slice(0, self.sizes[dim])
            
            else :
                if graph_dimensions is not None and dim in graph_dimensions :
                    i = slice(0, self.sizes[dim])
                    
                elif dim == Matrix.FIELDS_NAME :
                    i = self.get_field_index(field)
                
                elif dim in searches.keys() :
                    i = self.coord_to_index(dim, searches[dim])
                else :
                    pos = positions[dim]
                    if pos['origin'] == 'element' : i = pos['pos']
                    elif dim in self.vect_indices.keys() : i = self.vect_indices[dim][pos['pos']]
                    else : i = pos['pos']
                
            indices.append(i)
            
        #----------------------------------------------------------------------
        return indices
    
    #==========================================================================
    def load_axes(self, round_fmt='{:.6G}') : self.load_data(axes=True , matrix=False, round_fmt=round_fmt)
    def load_matrix(self, round_fmt='{:.6G}') : self.load_data(axes=False, matrix=True, round_fmt=round_fmt)
    def load_data(self, axes=True, matrix=True, round_fmt='{:.6G}') :
        #----------------------------------------------------------------------
        ds = Dataset(self.loaded_nc, 'r')
        
        #----------------------------------------------------------------------
        if axes :
            for dim,path in self.axes_paths.items() :
                gp = ds
                for gp_name in path : gp = gp.groups[gp_name]
                etype = gp.getncattr(Element.ATTR_ELEMENT)
                if etype == 'Mesh' :
                    self.axes[dim] = round_to_fmt(gp.variables[Mesh.EDGES_NAME][:])
                    if dim not in self.edge_axes : self.edge_axes.append(dim)
                elif etype == 'Vector' :
                    self.axes[dim] = round_to_fmt(gp.variables[Vector.VALUES_NAME][:])
                else : raise Exception("le type d'élément '{}' n'est pas implémenté pour un axe de matrice".format(etype))
            
            #------------------------------------------------------------------
            self.vect_indices = {} # file -> element
            for dim in self.dimensions :
                if dim not in self.axes.keys() : continue
                X = self.axes[dim]
                if self.file.vects is not None and dim in self.file.vects.keys() :
                    self.vect_indices[dim] = []
                    for ic,x in enumerate(self.file.vects[dim].values) :
                        if x < X[0] : ie = 0
                        elif x > X[-1] : ie = len(X)-1
                        else : ie = np.where(X<=x)[0][-1]
                        self.vect_indices[dim].append(ie)
                
        #----------------------------------------------------------------------
        if matrix :
            gp = ds
            for gp_name in self.path : gp = gp.groups[gp_name]
            matrix_var = gp.variables[Matrix.VAR_MATRIX]
            
            # TODO : tester la taille et passer en mem
            self.M = np.array(matrix_var[:], dtype=Element.DTYPES[self.dtype]['np'])
            
        #----------------------------------------------------------------------
        ds.close()
        
    #==========================================================================
    def get_fields(self) :
        #----------------------------------------------------------------------
        if Matrix.FIELDS_NAME not in self.dimensions : return None
        return self.get_attribute("fields")
        
    #==========================================================================
    def get_field_index(self, field) :
        #----------------------------------------------------------------------
        if field is None : return None
        fields = self.get_fields()
        if fields is None : return None
        if field not in fields : return None
        return fields.index(field)
    
    #==========================================================================
    def get_field_icon(self, field) :
        #----------------------------------------------------------------------
        if self.field_icons is None : return
        return self.field_icons[self.get_field_index(field)]
    
    #==========================================================================
    def get_matrix_data(self, indices, round_fmt=None) :
        #----------------------------------------------------------------------
        if self.M is None : self.load_data(round_fmt=round_fmt)
        return self.M[tuple(indices)]
        
    #==========================================================================
    def get_dimensions(self) :
        #----------------------------------------------------------------------
        return [d for d in self.dimensions if d != Matrix.FIELDS_NAME]
    
    #==========================================================================
    def get_dim_size(self, dim) :
        #----------------------------------------------------------------------
        size = Element.get_dim_size(self, dim)
        if size is not None : return size
        
        #----------------------------------------------------------------------
        if dim not in self.axes.keys() :
            self.load_data()
            size = self.M.shape[self.dimensions.index(dim)]
            return size
        
    #==========================================================================
    def get_lims(self, dim) :
        #----------------------------------------------------------------------
        self.load_axes()
        if dim not in self.axes : return None,None
        return self.axes[dim][0], self.axes[dim][-1]
        
    #==========================================================================
    def get_range(self, field=None) :
        #----------------------------------------------------------------------
        if field is None :
            return self.vmin,self.vmax
            
        #----------------------------------------------------------------------
        f = self.get_field_index(field)
        return self.vmins[f], self.vmaxs[f]
    
    #==========================================================================
    def is_dim_nodes(self, dim) :
        #----------------------------------------------------------------------
        self.load_axes()
        return len(self.axes[dim]) == self.sizes[dim]
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
