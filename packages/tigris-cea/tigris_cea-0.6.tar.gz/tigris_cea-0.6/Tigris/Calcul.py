# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import shutil
from netCDF4 import Dataset
from time import sleep
#------------------------------------------------------------------------------
from File import File
from Element import Element,read_nc
from Element_Constants import Mesh, Vector
from utils import get_temp_dir
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Calcul(File) :
    
    #==========================================================================
    ATTR_CODE     = "CODE"
    ATTR_CALCUL   = "CALCUL_NAME"
    ATTR_POSTDATE = "POSTDATE"
    ATTR_DIRPATH  = 'DIRECTORY_PATH'
    #--------------------------------------------------------------------------
    CONFIG_NAME  = "0-CONFIG"
    COORD_NAME   = "1-COORDS"
    ZONES_NAME   = "2-ZONES"
    PROPS_NAME   = "3-PROPS"
    RESULTS_NAME = "4-RESULTS"
    #--------------------------------------------------------------------------
    CODE_NAMES = {'porflow':'Porflow', 'min3p':'Min3P', 'hytec':'HYTEC', 'crunch':'Crunch'}
    
    #==========================================================================
    DETAILS_ALIGN = 18 # espacement entre la gauche et les ":" pour les détails
    
    #==========================================================================
    def __init__(self, code) :
        #----------------------------------------------------------------------
        File.__init__(self)
        self.icon = code
        
        #----------------------------------------------------------------------
        self.code = code
        self.code_name = Calcul.CODE_NAMES[self.code]
        
        #----------------------------------------------------------------------
        self.dirpath = None
        self.config = None
        self.elements = None
        
    #==========================================================================
    def details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("#---------------------------------------------------------------")
        print("> Calcul '{}' ({})".format(self.alias, self.code_name))
        print("   - dossier".ljust(Element.DETAILS_ALIGN,' ')+": {}".format(self.dirpath))
        
        #----------------------------------------------------------------------
        print("   - coordonnées :")
        
        #----------------------------------------------------------------------
        for dim,mesh in sorted(self.meshs.items(), key=lambda e:e[0]) :
            print("      -> {}".format(dim).ljust(Calcul.DETAILS_ALIGN,' ')+": {} mailles, [{:.5G} -> {:.5G}]".format(mesh.N, mesh.edges[0], mesh.edges[-1]))
        
        #----------------------------------------------------------------------
        for dim,vect in sorted(self.vects.items(), key=lambda e:e[0]) :
            print("      -> {}".format(dim).ljust(Calcul.DETAILS_ALIGN,' ')+": {} valeurs, [{:.5G} -> {:.5G}]".format(vect.N, vect.values[0], vect.values[-1]))
        
        #----------------------------------------------------------------------
        self._details(**kwargs)
    
    #==========================================================================    
    def _details(self, **kwargs) :
        pass
    
    #==========================================================================
    def load(self, nc_path, alias=None, logs=True) :
        #----------------------------------------------------------------------
        if logs : print("> Chargement du calcul {} ({}) ... ".format(self.code_name, os.path.basename(nc_path)), end="", flush=True)
        
        #----------------------------------------------------------------------
        self.nc_path = nc_path
        self.meshs  = {}
        self.vects  = {}
        
        #----------------------------------------------------------------------
        self.elements = read_nc(nc_path)
        for e in self.elements :
            e.set_file(self)
            
            if e.path[0] == Calcul.CONFIG_NAME :
                self.config = e
                continue
            
            elif e.path[0] == Calcul.COORD_NAME :
                if   isinstance(e, Mesh)   : self.meshs[e.path[1]] = e
                elif isinstance(e, Vector) : self.vects[e.path[1]] = e
            
        #----------------------------------------------------------------------
        self.name    = self.config.get_attribute(Calcul.ATTR_CALCUL)
        self.dirpath = self.config.get_attribute(Calcul.ATTR_DIRPATH)
        self.alias = self.name if alias is None else alias
        
        #----------------------------------------------------------------------
        self._load()
        
        #----------------------------------------------------------------------
        lims = {m.dimension:(m.edges[0], m.edges[-1]) for m in self.meshs.values()}
        for m in self.meshs.values() : m.set_lims(lims)
        
        #----------------------------------------------------------------------
        if logs : print("OK")

    #==========================================================================
    def _load(self) :
        pass
        
    #==========================================================================
    def _save(self, ds) :
        pass
        
    #==========================================================================
    def is_dim_edge(self, dim) :
        #----------------------------------------------------------------------
        return dim in self.meshs.keys()
    
    #==========================================================================
    def get_dim_size(self, dim) :
        #----------------------------------------------------------------------
        if   dim in self.meshs.keys() : return self.meshs[dim].N
        elif dim in self.vects.keys() : return self.vects[dim].N
        
    #==========================================================================
    def get_dim_value(self, dim, indice) :
        #----------------------------------------------------------------------
        if   dim in self.meshs.keys() : return self.meshs[dim].edges[indice], self.meshs[dim].edges[indice+1]
        elif dim in self.vects.keys() : return self.vects[dim].values[indice]
        return None
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Calcul_Convertor :
    
    #==========================================================================
    def __init__(self, **opts) :
        #----------------------------------------------------------------------
        self.name = None
        self.dirpath = None
        self.nc_path = None
        
        #----------------------------------------------------------------------
        self.config = None
        self.meshs  = None
        self.vects  = None
        
    #==========================================================================
    def convert(self, **opts) :
        #----------------------------------------------------------------------
        self.meshs = {}
        self.vects = {}
        
        #----------------------------------------------------------------------
        self._convert(**opts)
            
        #----------------------------------------------------------------------
        self.save(opts.get('nc_path', None))
        
        #----------------------------------------------------------------------
        print("> Conversion terminée")
    
    #==========================================================================
    def save(self, nc_path=None) :
        #----------------------------------------------------------------------
        if nc_path is None : self.nc_path = os.path.join(self.dirpath, self.name+".nc")
        else : self.nc_path = nc_path
        
        #----------------------------------------------------------------------
        ncpath_temp = self.nc_path+"_tmp"
        
        #----------------------------------------------------------------------
        print('> Ecriture du fichier NetCDF :')
        ds = Dataset(ncpath_temp, 'w')
        
        #----------------------------------------------------------------------
        print("   - configuration ... ", end="", flush=True)
        self.config.save(ds)
        print("OK")
        
        #----------------------------------------------------------------------
        if self.meshs is not None :
            print("   - maillage ... ", end="", flush=True)
            for mesh in self.meshs.values() : mesh.save(ds)
            print("OK")
            
        #----------------------------------------------------------------------
        if self.vects is not None :
            print("   - coordonnées ... ", end="", flush=True)
            for vect in self.vects.values() : vect.save(ds)
            print("OK")
            
        #----------------------------------------------------------------------
        self._save(ds)
            
        #----------------------------------------------------------------------
        ds.close()
        
        #----------------------------------------------------------------------
        print("   - sauvegarde ... ", end="", flush=True)
        #----------------------------------------------------------------------
        if os.path.exists(self.nc_path) :
            first = True
            while True :
                try : os.remove(self.nc_path) ; break
                except :
                    if first : print("(fichier '{}' ouvert) ... ".format(os.path.basename(self.nc_path)), end="", flush=True)
                    first = False
                sleep(0.5)
        #----------------------------------------------------------------------
        shutil.move(ncpath_temp, self.nc_path)
        print("OK")
        
        #----------------------------------------------------------------------
        print("   - suppression des fichiers temporaires ... ", end="", flush=True)
        shutil.rmtree(get_temp_dir(self.dirpath))
        print("OK")
        
        #----------------------------------------------------------------------
        print("> Ecriture terminée !")
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  


        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** PROGRAM ***
#------------------------------------------------------------------------------
# if __name__ == '__main__' :
#     nc_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Porflow/Porflow-Simple/test.nc"
#     calcul = Calcul.load_calcul(nc_path)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

