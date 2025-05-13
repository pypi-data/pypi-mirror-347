# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import shutil
from netCDF4 import Dataset
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QApplication,QFileDialog
#------------------------------------------------------------------------------
from Element import Element, read_nc
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class File :
    
    #==========================================================================
    OPERATION_NAME = "5-OPERATIONS"
    INDEX = 1
    
    #==========================================================================
    def __init__(self, **kwargs) :
        #----------------------------------------------------------------------
        self.index = File.INDEX
        File.INDEX += 1
        
        #----------------------------------------------------------------------
        self.name = kwargs.get('name',None)
        self.alias = kwargs.get('alias',self.name)
        self.nc_path = kwargs.get('nc_path',None)
        self.icon = 'nocode'
        
        #----------------------------------------------------------------------
        if self.name is None :
            if self.nc_path is not None : self.name = os.path.basename(self.nc_path).replace('.nc','')
            else : self.name = 'ncfile'
        
        #----------------------------------------------------------------------
        self.elements = []
        self.meshs  = None
        self.vects = None
        
    #==========================================================================
    def details(self) :
        #----------------------------------------------------------------------
        print("#---------------------------------------------------------------")
        print("> Fichier '{}'".format(self.alias))
        
        #----------------------------------------------------------------------
        for element in self.elements :
            element.details()
    
    #==========================================================================
    def load(self, nc_path, alias=None, logs=True) :
        #----------------------------------------------------------------------
        self.nc_path = nc_path
        
        #----------------------------------------------------------------------
        self.name  = os.path.basename(nc_path).replace('.nc','')
        self.alias = self.name if alias is None else alias
        
        #----------------------------------------------------------------------
        if logs : print("> Chargement du fichier '{}' ... ".format(self.name), end="", flush=True)
        
        #----------------------------------------------------------------------
        self.elements = read_nc(nc_path)
        for e in self.elements :
            e.set_file(self)
            
        #----------------------------------------------------------------------
        if logs : print("OK")
    
    #==========================================================================
    def save(self, nc_path=None, logs=True) :
        #----------------------------------------------------------------------
        if nc_path is not None :
            self.nc_path = nc_path
        else :
            nc_path = self.nc_path
            
        #----------------------------------------------------------------------
        if logs : print("> Sauvegarde du fichier '{}' ... ".format(self.name), end="", flush=True)
        
        #----------------------------------------------------------------------
        if nc_path is None :
            filename = "{}.nc".format(self.name)
            if QApplication.instance() is None : _ = QApplication([])
            nc_path,_ = QFileDialog.getSaveFileName(None, "Enregistrer sous", filename, "Tous les fichiers (*);;NetCDF (*.nc)", "NetCDF (*.nc)")
            
        #----------------------------------------------------------------------
        if nc_path == '' :
            if logs : print("annulé")
            return
        
        #----------------------------------------------------------------------
        ncpath_temp = self.nc_path+"_tmp"
        
        #----------------------------------------------------------------------
        ds = Dataset(ncpath_temp, 'w')
        for e in sorted(self.elements, key=lambda e:e.path) : e.save(ds)
        ds.close()
        
        #----------------------------------------------------------------------
        shutil.move(ncpath_temp, nc_path)
        if logs : print("OK")
        
    #==========================================================================
    def add_element(self, element, replace=False) :
        #----------------------------------------------------------------------
        for e,_element in enumerate(self.elements) :
            if _element.path == element.path :
                if replace :
                    self.elements.pop(e)
                else :
                    raise Exception("chemin d'élément déjà utilisé")
               
        #----------------------------------------------------------------------                                         
        self.elements.append(element)
        
    #==========================================================================
    def get_element(self, path=None, index=None) :
        #----------------------------------------------------------------------
        if path is not None and type(path) == str :
            path = path.split("/")
        
        #----------------------------------------------------------------------
        for element in self.elements :
            if path is not None and element.path == path : return element
            if index is not None and element.index == index : return element
        
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def remove_element(self, element, logs=True) :
        #----------------------------------------------------------------------
        if logs : print("> Suppression de l'élément '{}' ... ".format(element.label), end="", flush=True)
    
        #----------------------------------------------------------------------
        self.elements.remove(element)
        self.save(logs=False)
        
        #----------------------------------------------------------------------
        if logs : print("OK")
        
    #==========================================================================
    def get_dim_size(self, dim) : return None
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** PROGRAM ***
#------------------------------------------------------------------------------
if __name__ == '__main__' :
    nc_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Porflow/Porflow-Simple/test.nc"
    file = File(name='azd')
    file.add_element(Element(path=['A','B'], label='label'))
    # file.load(nc_path)
    file.save()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

