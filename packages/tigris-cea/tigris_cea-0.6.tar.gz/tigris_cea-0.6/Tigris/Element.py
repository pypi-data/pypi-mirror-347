# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
from netCDF4 import Dataset
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Element :
    
    #==========================================================================
    DTYPES = {}
    DTYPES['int8']     = {'np':np.int8   } #  8 octets, -128 à 127
    DTYPES['uint8']    = {'np':np.uint8  } #  8 octets, 0 à 255
    DTYPES['int16']    = {'np':np.int16  } # 16 octets, -32768 à 32767
    DTYPES['uint16']   = {'np':np.uint16 } # 16 octets, 0 à 65535
    DTYPES['int32']    = {'np':np.int32  } # 32 octets, -2147483648 à 2147483647
    DTYPES['uint32']   = {'np':np.uint32 } # 32 octets, 0 à 4294967295
    DTYPES['int64']    = {'np':np.int64  } # 64 octets, -9223372036854775808 à 9223372036854775807
    DTYPES['uint64']   = {'np':np.uint64 } # 64 octets, 0 à 18446744073709551615
    DTYPES['float16']  = {'np':np.float16} # 16 octets, ~±65504, 3 chiffres significatifs
    DTYPES['float32']  = {'np':np.float32} # 32 octets, ~±3.4 × 10^38, 7 chiffres significatifs
    DTYPES['float64']  = {'np':np.float64} # 64 octets, ~±1.8 × 10^308, 15 chiffres significatifs
    
    #--------------------------------------------------------------------------
    ATTRS_PREFIX    = "ATTRS_"
    STYLE_PREFIX    = "STYLE_"
    ATTR_LABEL      = "LABEL"
    ATTR_ELEMENT    = "ELEMENT"
    ATTR_FORMULA    = "FORMULA"
    ATTR_COMPUTED   = "COMPUTED"
    PREFIX_BEACON   = "BEACON"
    PREFIX_AXE_PATH = 'PATH_'
    
    #--------------------------------------------------------------------------
    DETAILS_ALIGN   = 18 # espacement entre la gauche et les ":" pour les détails
    
    #==========================================================================
    INDEX = 1
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        if kwargs.pop('get_index',True) :
            self.index = Element.INDEX
            Element.INDEX += 1
        else :
            self.index = None
            
        #----------------------------------------------------------------------
        self.etype = type(self).__name__
        
        #----------------------------------------------------------------------
        self.file = None
        self.path = None
        self.label = None
        self.icon = None
        
        #----------------------------------------------------------------------
        self.axes = None
        self.edge_axes = []
        
        #----------------------------------------------------------------------
        self.loaded_nc = None
        
        #----------------------------------------------------------------------
        self.attributes = {}
        self.style = {}
        
        #----------------------------------------------------------------------
        self.configure(**kwargs)
        
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "{}({})".format(self.etype, "/".join(self.path))
    
    #==========================================================================
    def set_file(self, file) :
        #----------------------------------------------------------------------
        self.file = file
        
    #==========================================================================
    def configure(self, **kwargs) :
        #----------------------------------------------------------------------
        if 'path' in kwargs.keys() :
            self.path = kwargs['path'].copy()
            self.label = self.path[-1]
            
        #----------------------------------------------------------------------
        if 'label' in kwargs.keys() :
            self.label = kwargs['label']
            
        #----------------------------------------------------------------------
        self._configure(**kwargs)
        self.set_attributes(**kwargs)
        
    #==========================================================================
    def _configure(self, **kwargs) :
        pass
    
    #==========================================================================
    def details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("#---------------------------------------------------------------")
        print("> Elément '{}' ({})".format(self.label, type(self).__name__))
        print("   - calcul".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.file.nc_path))
        print("   - chemin".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.path))
        
        #----------------------------------------------------------------------
        self._details(**kwargs)
        
    #==========================================================================
    def _details(self, **kwargs) :
        pass
        
    #==========================================================================
    def set_attributes(self, **kwargs) :
        #----------------------------------------------------------------------
        for k,v in kwargs.items() :
            if hasattr(self, k) : continue
            self.attributes[k] = v
            
    #==========================================================================
    def get_attribute(self, k, default=None) :
        #----------------------------------------------------------------------
        return self.attributes.get(k, default)
        
    #==========================================================================
    def set_style(self, **kwargs) :
        #----------------------------------------------------------------------
        for k,v in kwargs.items() :
            self.style[k] = v
            
    #==========================================================================
    def get_style(self, k, default=None) :
        #----------------------------------------------------------------------
        return self.style.get(k, default)
    
    #==========================================================================
    def get_beacon(self, field=None) :
        #----------------------------------------------------------------------
        B = "'E{}".format(self.index)
        if field is not None : B += "_{}".format(self.get_field_index(field)+1)
        B += "'"
        
        #----------------------------------------------------------------------
        return B
        
    #==========================================================================
    def save(self, ds) :
        #----------------------------------------------------------------------
        for p in range(len(self.path)) :
            _path = "/".join(self.path[:p+1])
            gp = ds.createGroup(_path)
        
        #----------------------------------------------------------------------
        self._save(gp)
        
        gp.setncattr(Element.ATTR_LABEL  , self.label)
        gp.setncattr(Element.ATTR_ELEMENT, type(self).__name__)
        
        #----------------------------------------------------------------------
        for prefix,dico in [(Element.ATTRS_PREFIX,self.attributes), (Element.STYLE_PREFIX,self.style)] :
            for k,v in dico.items() :
                if v is None : v = 'NONE'
                elif type(v) == bool : v = 'TRUE' if v else 'FALSE'
                
                gp.setncattr(prefix+k, v)
        
    #==========================================================================
    def _save(self, gp) :
        pass
        
    #==========================================================================
    def load(self, gp) :
        #----------------------------------------------------------------------
        self.loaded_nc = gp.filepath()
        self.configure(path=gp.path[1:].split("/"), label=gp.getncattr(Element.ATTR_LABEL))
        
        #----------------------------------------------------------------------
        attributes = {}
        style = {}
        for k in gp.ncattrs() :
            if   k.startswith(Element.ATTRS_PREFIX) : D,_k = attributes, k.replace(Element.ATTRS_PREFIX,"")
            elif k.startswith(Element.STYLE_PREFIX) : D,_k = style     , k.replace(Element.STYLE_PREFIX,"")
            else : continue
        
            v = gp.getncattr(k)
            if type(v) == str : v = {'NONE':None, 'TRUE':True, 'FALSE':False}.get(v,v)
            D[_k] = v
            
        #----------------------------------------------------------------------
        self.set_attributes(**attributes)
        self.set_style(**style)
        
        #----------------------------------------------------------------------
        self.vect_indices = None
        self._load(gp)
        
    #==========================================================================
    def _load(self, gp) :
        pass
    
    #==========================================================================
    def load_axes(self) :
        pass
        
    #==========================================================================
    def get_fields(self) :
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def get_dimensions(self) :
        #----------------------------------------------------------------------
        raise Exception("fonction 'get_dimensions' non configurée pour un élément de type {}".format(type(self).__name__))
        
    #==========================================================================
    def is_dim_edge(self, dim) :
        #----------------------------------------------------------------------
        return dim in self.edge_axes
        
    #==========================================================================
    def get_dim_size(self, dim) :
        #----------------------------------------------------------------------
        if dim not in self.get_dimensions() : return None
        
        #----------------------------------------------------------------------
        self.load_axes()
        if dim not in self.axes.keys() : return None
        
        if self.is_dim_edge(dim) : return len(self.axes[dim])-1
        else                     : return len(self.axes[dim])
        
    #==========================================================================
    def get_dim_value(self, dim, index) :
        #----------------------------------------------------------------------
        if dim not in self.get_dimensions() : return None
        
        #----------------------------------------------------------------------
        if self.is_dim_edge(dim) : return self.axes[dim][index],self.axes[dim][index+1]
        else                     : return self.axes[dim][index]
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_nc(nc_path) :
    #--------------------------------------------------------------------------
    ds = Dataset(nc_path, 'r')
    elements = read_gp(ds)
    ds.close()
    return elements
    
#==============================================================================
def read_gp(gp) :
    #--------------------------------------------------------------------------
    from Element_Constants import Constant, Vector, Mesh
    from Element_Matrix import Matrix
    from Element_Cuboids import Cuboid, PolyCuboid
    
    #--------------------------------------------------------------------------
    elements = []
    for _gp_name,_gp in gp.groups.items() :
        if Element.ATTR_ELEMENT in _gp.ncattrs() :
            class_name = _gp.getncattr(Element.ATTR_ELEMENT)
            if   class_name == 'Element'    : element = Element(get_index=class_name != 'Element')
            elif class_name == 'Constant'   : element = Constant(get_index=class_name != 'Element')
            elif class_name == 'Vector'     : element = Vector(get_index=class_name != 'Element')
            elif class_name == 'Mesh'       : element = Mesh(get_index=class_name != 'Element')
            elif class_name == 'Matrix'     : element = Matrix(get_index=class_name != 'Element')
            elif class_name == 'Cuboid'     : element = Cuboid(get_index=class_name != 'Element')
            elif class_name == 'PolyCuboid' : element = PolyCuboid(get_index=class_name != 'Element')
            else : raise Exception("type {} inconnu".format(class_name))
            
            element.load(_gp)
            elements.append(element)
        else :
            elements += read_gp(_gp)
        
    return elements
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

