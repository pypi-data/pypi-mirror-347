# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import re
import numpy as np
from netCDF4 import Dataset
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QFont, QDropEvent
from PyQt5.QtWidgets import QFileDialog, QLabel, QWidget, QTextEdit
#------------------------------------------------------------------------------
from Element import Element
from Element_Matrix import Matrix
from File import File
from utils_qt import question_box, clear_layout
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Combiner_Code(QTextEdit) :
    
    #==========================================================================
    def __init__(self, combiner) :
        #----------------------------------------------------------------------
        self.combiner = combiner
        
        #----------------------------------------------------------------------
        QTextEdit.__init__(self)
        
        #----------------------------------------------------------------------
        self.setAcceptDrops(True)
        self.setFont(QFont('Courier',10))
    
    #==========================================================================
    def dragEnterEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            objs = event.source().get_selected_objects()
            
            if len(objs) == 1 and type(objs[0]['element']) == Matrix :
                event.accept()
                return
                
        #----------------------------------------------------------------------
        event.ignore()
        
    #==========================================================================
    def dropEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            objs = event.source().get_selected_objects()
            
            if len(objs) == 1 and type(objs[0]['element']) == Matrix :
                element = objs[0].get('element')
                field = objs[0].get('field',None)
                B = element.get_beacon(field=field)
                mimeData = QMimeData()
                mimeData.setText(B)
                _event = QDropEvent(event.posF(), event.possibleActions(), mimeData, event.mouseButtons(), event.keyboardModifiers())
                QTextEdit.dropEvent(self, _event)
                self.setFocus()
                return
                
        #----------------------------------------------------------------------
        event.ignore()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Combiner(QWidget) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        self.mw = mw
        
        #----------------------------------------------------------------------
        QWidget.__init__(self)
        
        #----------------------------------------------------------------------
        self.load_ui()
        
        #----------------------------------------------------------------------
        self.gp_save.setAcceptDrops(True)
        self.gp_save.dragEnterEvent = self.dragEnterEvent
        self.gp_save.dropEvent = self.dropEvent

        #----------------------------------------------------------------------
        for w in self.gp_save.findChildren(QWidget) :
            w.setAcceptDrops(False)
            
        #----------------------------------------------------------------------
        self.on_code_edited()
        
    #==========================================================================
    def load_ui(self) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Combiner.ui"), self)
        
        #----------------------------------------------------------------------
        self.te_code = Combiner_Code(self)
        self.layout_code.addWidget(self.te_code)
        self.te_code.textChanged.connect(self.on_code_edited)
        self.le_path.returnPressed.connect(lambda le=self.le_path : le.setText(le.text() if le.text() != '' else le.placeholderText()))
        self.le_name.returnPressed.connect(lambda le=self.le_name : le.setText(le.text() if le.text() != '' else le.placeholderText()))
        #----------------------------------------------------------------------
        self.but_get_file.clicked.connect(self.select_file)
        self.but_create.clicked.connect(self.create)
        self.but_close.clicked.connect(lambda e,state=False : self.set_activated(state))
        #----------------------------------------------------------------------
        for file in self.mw.files_manager.files :
            self.co_files.addItem(file.nc_path)
        
        #----------------------------------------------------------------------
        path = '/'.join([File.OPERATION_NAME])
        self.le_path.setText(path)
        self.le_path.setPlaceholderText(path)
        
    #==========================================================================
    def set_activated(self, state) :
        #----------------------------------------------------------------------
        self.mw.action_combiner.setChecked(state)
        self.mw.parameters_manager.udpate_docks()
        
        #----------------------------------------------------------------------
        if state : self.mw.stackedWidget.setCurrentWidget(self)
        else : self.mw.stackedWidget.setCurrentIndex(0)
        
    #==========================================================================
    def update_calculs(self) :
        #----------------------------------------------------------------------
        current = self.co_files.currentText()
        self.co_files.clear()
        self.co_files.addItem(current)
        
        #----------------------------------------------------------------------
        for file in self.mw.files_manager.files :
            if file.nc_path == current : continue
            self.co_files.addItem(file.nc_path)
        
    #==========================================================================
    def select_file(self) :
        #----------------------------------------------------------------------
        nc_path, _ = QFileDialog.getSaveFileName(self.mw, "Sélectionner un fichier .nc", "", "Tous (*);;NetCDF (*.nc)", "NetCDF (*.nc)")
        if nc_path == '' : return
        
        #----------------------------------------------------------------------
        items = [self.co_files.itemText(i) for i in range(self.co_files.count())]
        if nc_path not in items : self.co_files.addItem(nc_path)
        self.co_files.setCurrentText(nc_path)
    
    #==========================================================================
    def on_code_edited(self) :
        #----------------------------------------------------------------------
        clear_layout(self.layout_beacons)
    
        #----------------------------------------------------------------------
        valid,beacon_infos = self.check_beacons()
        self.gp_beacons.setVisible(valid)
        if not valid : return
        
        #----------------------------------------------------------------------
        r = 0
        for beacon,element,field in beacon_infos :
            path = [element.file.alias] + element.path.copy()
            if field is not None : path.append(field)
            self.layout_beacons.addRow(QLabel(beacon), QLabel(": " + "/".join(path)))
            r += 1
            
    #==========================================================================
    
    
    #==========================================================================
    #---- *** DRAG & DROP ***
    #==========================================================================
    def dragEnterEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            items = event.source().get_selected_items()
            if len(items) == 1 :
                event.accept()
                return
                
        #----------------------------------------------------------------------
        event.ignore()
                
    #==========================================================================
    def dropEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            ft = event.source()
            fm = ft.fm
            items = ft.get_selected_items()
            
            if len(items) == 1 :
                path = items[0].path
                
                file = fm.obj_from_path([path[0]]).get('element') # file.alias -> file
                self.co_files.setCurrentText(file.nc_path)
                
                if len(path) > 1 :
                    e = fm.obj_from_path(path)
                    element = e.get('element')
                    
                    if element is None : 
                        self.le_path.setText("/".join(path[1:]))
                        self.le_name.setText('')
                    else :
                        self.le_path.setText("/".join(path[1:-1]))
                        if element.get_fields() is None : self.le_name.setText(path[-1])
                        else : self.le_name.setText(e.get('field'))
                        
                    event.accept()
                    return
            
        #----------------------------------------------------------------------
        event.ignore()
        
    #==========================================================================
    
    
    #==========================================================================
    #---- *** CREATION ***
    #==========================================================================
    def check_beacons(self) :
        #----------------------------------------------------------------------
        code = self.te_code.toPlainText()
        
        #----------------------------------------------------------------------
        beacons = list(np.unique(re.findall(r"'(.*?)'", code)))
        beacon_infos = []
        for b,beacon in enumerate(beacons) :
            try :
                e_index = int(beacon.split("_")[0].replace('E',''))
                f_index = None if '_' not in beacon else int(beacon.split("_")[1])
            except : return False, "le format de la balise '{}' est invalide".format(beacon)
            #------------------------------------------------------------------
            try : element = self.mw.files_manager.obj_from_index(e_index)
            except : return False, "aucun élément associé à la balise '{}'".format(beacon)
            #------------------------------------------------------------------
            try :
                field = None
                if f_index is not None : field = element.get_fields()[f_index-1]
            except : return False, "l'élément associé à la balise '{}' n'a pas de champ '{}'".format(beacon, f_index)
            #------------------------------------------------------------------
            beacon_infos.append((beacon,element,field))
            
        #----------------------------------------------------------------------
        if len(beacon_infos) == 0 : return False,'aucune balise'
        return True,beacon_infos.copy()
    
    #==========================================================================
    def check_geometry(self, beacon_infos) :
        #----------------------------------------------------------------------
        dimensions = None
        axes = None
        
        #----------------------------------------------------------------------
        for beacon,element,field in beacon_infos :
            name = element.label
            if field is not None : name += "/"+field
            
            #------------------------------------------------------------------
            element.load_axes()
            _dimensions = [dim for dim in element.dimensions if dim != Matrix.FIELDS_NAME]
            _axes = {dim:element.axes[dim] for dim in _dimensions}
            
            #------------------------------------------------------------------
            if dimensions is None :
                dimensions = _dimensions.copy()
                axes       = _axes.copy()
                
            #------------------------------------------------------------------
            elif dimensions != _dimensions :
                return False, "balise '{}' non homogène (dimensions)".format(beacon),None
            
            #------------------------------------------------------------------
            else :
                for dim,_ax in _axes.items() :
                    ax = axes[dim]
                    if len(ax) != len(_ax) :
                        return False, "balise '{}' non homogène (taille de l'axe '{}')".format(beacon,dim),None
                    
                    elif not (ax==_ax).all() :
                        return False, "balise '{}' non homogène (valeurs de l'axe '{}')".format(beacon,dim),None
            
        #----------------------------------------------------------------------
        return True,dimensions,axes
        
    #==========================================================================
    def check_code(self, beacon_infos) :
        #----------------------------------------------------------------------
        code = self.te_code.toPlainText()
        for beacon,element,field in beacon_infos :
            code = code.replace("'{}'".format(beacon),"(0.5)")
            
        #----------------------------------------------------------------------
        mode = 'exec' if "result=" in code.replace(" ","") else 'eval'
        try :
            if mode == 'exec' : exec(code, {}, {})
            else : eval(code)
        #----------------------------------------------------------------------
        except Exception as e :
            return False, str(e)
        
        #----------------------------------------------------------------------
        return True,mode
        
    #==========================================================================
    def compute(self, beacon_infos) :
        #----------------------------------------------------------------------
        code = self.te_code.toPlainText()
        
        #----------------------------------------------------------------------
        variables = {}
        for beacon,element,field in beacon_infos :
            code = code.replace("'{}'".format(beacon),beacon)
            indices = element.get_indices(field=field)
            variables[beacon] = element.get_matrix_data(indices)
            
        #----------------------------------------------------------------------
        mode = 'exec' if "result=" in code.replace(" ","") else 'eval'
        try :
            if mode == 'exec' :
                namespace = {}
                exec(code, variables, namespace)
                M = namespace['result']
            else :
                M = eval(code, variables)
        except Exception as e :
            return False, str(e)
        
        #----------------------------------------------------------------------
        return True,M
        
    #==========================================================================
    def create(self) :
        #----------------------------------------------------------------------
        print("> Création de la variable")
        
        #----------------------------------------------------------------------
        print("   - vérification des balises ... ", end="", flush=True)
        #----------------------------------------------------------------------
        valid,beacon_infos = self.check_beacons()
        if not valid :
            print("Echec")
            print("   ->", beacon_infos)
            return
        #----------------------------------------------------------------------
        print("OK ({} balise(s) unique(s))".format(len(beacon_infos)))
        
        
        #----------------------------------------------------------------------
        print("   - vérification de la geométrie ... ", end="", flush=True)
        #----------------------------------------------------------------------
        valid,dimensions,axes = self.check_geometry(beacon_infos)
        if not valid :
            print("Echec")
            print("   ->", dimensions)
            return
        #----------------------------------------------------------------------
        print("OK ({})".format(", ".join(["{}={}".format(dim,len(axes[dim])) for dim in dimensions])))
        
        
        #----------------------------------------------------------------------
        print("   - vérification de la syntaxe ... ", end="", flush=True)
        #----------------------------------------------------------------------
        valid,mode = self.check_code(beacon_infos)
        if not valid :
            print("Echec")
            print("   ->", mode)
            return
        #----------------------------------------------------------------------
        print("OK (mode {})".format('expression' if mode == 'eval' else 'code'))
        
        
        #----------------------------------------------------------------------
        print("   - vérification du fichier netcdf ... ", end="", flush=True)
        #----------------------------------------------------------------------
        nc_path = self.co_files.currentText()
        if nc_path == '' :
            nc_path, _ = QFileDialog.getSaveFileName(self.mw, "Sélectionner un fichier .nc", "", "Tous (*);;NetCDF (*.nc)", "NetCDF (*.nc)")
            if nc_path == '' :
                print("annulé")
                return
            self.co_files.setCurrentText(nc_path)
            
        #----------------------------------------------------------------------
        file = None
        alias = None
        for _file in self.mw.files_manager.files :
            if os.path.samefile(_file.nc_path, nc_path) :
                file = _file
                alias = file.alias
                break
            
        #----------------------------------------------------------------------
        if file is None :
            file = File(nc_path=nc_path)
            if os.path.exists(nc_path) : file.load(nc_path, logs=False)
            print("file not loaded", alias)
            
        #----------------------------------------------------------------------
        if self.le_path.text() == '' : self.le_path.setText(self.le_path.placeholderText())
        if self.le_name.text() == '' : self.le_name.setText(self.le_name.placeholderText())
        #----------------------------------------------------------------------
        path = self.le_path.text().split("/") + [self.le_name.text()]
        test = file.get_element(path=path)
        if test is not None :
            rep = question_box('warning', "Variable existante", "Le fichier '{}' contient déjà une variable de même chemin".format(file.alias), buttons=[('Ok','Ecraser'),('Cancel','Annuler')])
            if rep == 'Cancel' :
                print("annulé")
                return
        #----------------------------------------------------------------------
        print("OK")
        
        #----------------------------------------------------------------------
        print("   - calcul ... ", end="", flush=True)
        #----------------------------------------------------------------------
        valid,M = self.compute(beacon_infos)
        if not valid :
            print("Echec")
            print("   ->", M)
            return
        #----------------------------------------------------------------------
        opts = {}
        opts[Element.ATTR_FORMULA] = self.te_code.toPlainText(),
        opts[Element.ATTR_COMPUTED] = True
        for beacon,element,field in beacon_infos :
            opts[Element.PREFIX_BEACON+"_"+beacon] = [element.file.nc_path] + element.path + ([field] if field is not None else [])
        #----------------------------------------------------------------------
        element = Matrix(path=path,
                         dimensions=dimensions,
                         axes=axes,
                         M=M,
                         **opts,
                         )
        
        #----------------------------------------------------------------------
        print("OK ({})".format(' x '.join([str(s) for s in M.shape])))
        
        #----------------------------------------------------------------------
        print("   - sauvegarde ... ", end="", flush=True)
        #----------------------------------------------------------------------
        file.add_element(element, replace=True)
        file.save(nc_path, logs=False)
        element.set_file(file)
        ds = gp = Dataset(nc_path, 'r')
        for gname in element.path : gp = gp.groups[gname]
        element.load(gp)
        ds.close()
        #----------------------------------------------------------------------
        print('OK (../{}/{})'.format(os.path.basename(nc_path), "/".join(path)))
        
        #----------------------------------------------------------------------
        if alias is None : self.mw.files_manager.load_file(nc_path)
        else : self.mw.files_manager.files_tree.update_file(file)
        
        #----------------------------------------------------------------------
        self.mw.files_manager.files_tree.expand_to_item([file.alias]+path)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


