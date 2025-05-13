# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
from netCDF4 import Dataset
#------------------------------------------------------------------------------
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QCursor
from PyQt5.QtWidgets import QFileDialog, QMenu, QHBoxLayout, QLineEdit
#------------------------------------------------------------------------------
from Element import Element
from File import File
from Calcul import Calcul
from Calcul_Convertor import get_convert_dialog
from utils_qt import TreeWidget, TreeWidgetItem, QTreeWidget
from utils_qt import get_icon, get_button
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Files_Manager :
    
    #==========================================================================
    def __init__(self, mw, layout) :
        #----------------------------------------------------------------------
        self.mw = mw
        
        #----------------------------------------------------------------------
        self.files_tree = Files_Tree(self)
        layout.addLayout(self.files_tree.layout_search)
        layout.addWidget(self.files_tree)
        
        #----------------------------------------------------------------------
        self.files = []
        self.elements = {}
        self.items = {} # spath -> item
        
    #==========================================================================
    def convert_calcul(self, code) :
        #----------------------------------------------------------------------
        dialog = get_convert_dialog(self.mw, code)
        
        #----------------------------------------------------------------------
        dialog.exec_()
    
    #==========================================================================
    def load_file(self, nc_path=None, add_to_tree=True) :
        #----------------------------------------------------------------------
        if nc_path is None :
            nc_path, _ = QFileDialog.getOpenFileName(self.mw, "Sélectionner un fichier .nc", "", "Tous (*);;NetCDF (*.nc)", "NetCDF (*.nc)")
            if nc_path == '' : return
        
        #----------------------------------------------------------------------
        try : ds = Dataset(nc_path, 'r')
        except :
            print("Impossible de charger le fichier {}, format NetCDF (.nc) non reconnu".format(os.path.basename(nc_path)))
            return
        
        #----------------------------------------------------------------------
        if Calcul.CONFIG_NAME in ds.groups :
            gp = ds.groups[Calcul.CONFIG_NAME]
            code = gp.getncattr(Element.ATTRS_PREFIX+Calcul.ATTR_CODE)
        else :
            code = None
        ds.close()
        
        #----------------------------------------------------------------------
        if   code == 'porflow' : from Porflow import Porflow ; file = Porflow()
        elif code == 'min3p'   : from Min3p   import Min3p   ; file = Min3p()
        elif code == 'hytec'   : from Hytec   import Hytec   ; file = Hytec()
        elif code == 'crunch'  : from Crunch  import Crunch  ; file = Crunch()
        #----------------------------------------------------------------------
        elif code is None      : file = File(nc_path=nc_path)
        #----------------------------------------------------------------------
        else : raise Exception("le code '{}' est inconnu".format(code))
        
        #----------------------------------------------------------------------
        self.mw.set_busy(1)
        file.load(nc_path)
        if add_to_tree : self.add_file(file)
        self.mw.set_busy(-1)
        
        #----------------------------------------------------------------------
        return file
    
    #==========================================================================
    def add_file(self, file) :
        #----------------------------------------------------------------------
        names = [f.alias for f in self.files]
        if file.alias in names :
            i = 2
            while "{}({})".format(file.alias,i) in names : i += 1
            file.alias = "{}({})".format(file.alias,i)
            
        #----------------------------------------------------------------------
        self.files.append(file)
        self.files_tree.add_file(file)
        
        #----------------------------------------------------------------------
        self.mw.combiner.update_calculs()
        
    #==========================================================================
    def remove_file(self, alias) :
        #----------------------------------------------------------------------
        file = self.obj_from_path([alias]).get('element')
        if file is None : return
        
        #----------------------------------------------------------------------
        item = self.items[file.alias]
        index = self.files_tree.indexOfTopLevelItem(item)
        self.files_tree.takeTopLevelItem(index)
        
        #----------------------------------------------------------------------
        for path in list(self.items.keys()) :
            if path.split("/")[0] == alias :
                self.items.pop(path)
        
        #----------------------------------------------------------------------
        self.mw.pages_manager.on_file_removed(file)
        
        #----------------------------------------------------------------------
        self.files.remove(file)
        del file
        
        #----------------------------------------------------------------------
        self.mw.combiner.update_calculs()
        
    #==========================================================================
    def obj_from_path(self, path) :
        #----------------------------------------------------------------------
        if type(path) == str : path = path.split("/")
        
        #----------------------------------------------------------------------
        if len(path) == 1 :
            for file in self.files :
                if file.alias == path[0] :
                    return {'element':file}
            return {}
        
        #----------------------------------------------------------------------
        spath = "/".join(path)
        if spath in self.elements.keys() :
            element = self.elements[spath]
            if element.get_fields() is not None : return {}
            return {'element':self.elements[spath]}
            
        #----------------------------------------------------------------------
        _spath = "/".join(path[:-1]) # sans field
        if _spath in self.elements.keys() :
            return {'element':self.elements[_spath], 'field':path[-1]}
        
        #----------------------------------------------------------------------
        return {}
        
    #==========================================================================
    def obj_from_index(self, element_index) :
        #----------------------------------------------------------------------
        for file in self.files :
            element = file.get_element(index=element_index)
            if element is not None : return element
        
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def obj_from_item(self, item) :
        #----------------------------------------------------------------------
        if item is None : return {}
        return self.obj_from_path(item.path)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Files_TreeItem(TreeWidgetItem) :
    
    #==========================================================================
    def __init__(self, *args, **kwargs) :
        self.plottable = kwargs.pop('plottable', False)
        TreeWidgetItem.__init__(self, *args, **kwargs)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Files_Tree(TreeWidget) :
    
    #==========================================================================
    def __init__(self, fm) :
        #----------------------------------------------------------------------
        self.fm = fm
        
        #----------------------------------------------------------------------
        TreeWidget.__init__(self)
        
        #----------------------------------------------------------------------
        self.layout_search = QHBoxLayout()
        self.le_search = QLineEdit()
        self.le_search.setToolTip('Recherche dans les items (chemin)\n";" pour plusieurs champs')
        self.le_search.setPlaceholderText('Recherche')
        self.layout_search.addWidget(self.le_search)
        self.le_search.textChanged.connect(self.update_visible)
        #----------------------------------------------------------------------
        self.but_nuls = get_button('null', checkable=True, checked=True, tooltip='Afficher les matrices nulles')
        self.layout_search.addWidget(self.but_nuls)
        self.but_nuls.clicked.connect(self.update_visible)
        #----------------------------------------------------------------------
        self.but_csts = get_button('constant', checkable=True, checked=True, tooltip='Afficher les matrices constantes')
        self.layout_search.addWidget(self.but_csts)
        self.but_csts.clicked.connect(self.update_visible)
        #----------------------------------------------------------------------
        self.but_case = get_button('casse', checkable=True, checked=False, tooltip='Respecter la casse')
        self.layout_search.addWidget(self.but_case)
        self.but_case.clicked.connect(self.update_visible)
        #----------------------------------------------------------------------
        but_clear = get_button('clear', tooltip='Vider le champ')
        self.layout_search.addWidget(but_clear)
        but_clear.clicked.connect(lambda e:self.le_search.setText(''))
        
        #----------------------------------------------------------------------
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.drag = None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
    #==========================================================================
    def add_file(self, file) :
        #----------------------------------------------------------------------
        but_regroup = get_button('regroup')
        but_ungroup = get_button('ungroup')
        
        self.fm.items[file.alias] = item = Files_TreeItem(self, [file.alias], label=file.alias, icon=file.icon, expanded=False, widgets=[but_regroup,but_ungroup])
        self.fm.items[file.alias].setExpanded(True)
        
        but_regroup.clicked.connect(lambda e,item=item : item.collapse_childs())
        but_ungroup.clicked.connect(lambda e,item=item : item.expand_childs())
        
        #----------------------------------------------------------------------
        self.update_file(file)
        
        #----------------------------------------------------------------------
        self.resizeColumnToContents(0)
    
    #==========================================================================
    def update_file(self, file) :
        #----------------------------------------------------------------------
        states = {key:item.isExpanded() for key,item in self.fm.items.items()}
        
        #----------------------------------------------------------------------
        for spath in list(self.fm.items.keys()) :
            if spath.startswith(file.alias+'/') :
                self.fm.items.pop(spath)
                if spath in self.fm.elements :
                    self.fm.elements.pop(spath)
                
        #----------------------------------------------------------------------
        self.fm.items[file.alias].takeChildren()
        
        #----------------------------------------------------------------------
        for element in file.elements :
            if element.icon is None :
                continue # config
            
            #------------------------------------------------------------------
            fields = element.get_fields()
            # epath = "/".join([file.alias]+element.path)
            
            path = [file.alias]
            spath = "/".join(path)
            
            #------------------------------------------------------------------
            for s,step in enumerate(element.path) :
                parent = self.fm.items[spath]
                path.append(step)
                spath = "/".join(path)
                if spath in self.fm.items.keys() : continue
                label     = element.label if s == len(element.path)-1 else step
                plottable = s == len(element.path)-(1 if fields is None else 0)
                icon      = element.icon if plottable else 'folder'                
                
                widgets = []
                if not plottable :
                    but_regroup = get_button('regroup')
                    but_ungroup = get_button('ungroup')
                    widgets = [but_regroup,but_ungroup]
                
                self.fm.items[spath] = item = Files_TreeItem(self, path.copy(), parent=parent, label=label, icon=icon, plottable=plottable, widgets=widgets)
                self.fm.items[spath].setExpanded(states.get(spath,False))
                
                if not plottable :
                    but_regroup.clicked.connect(lambda e,item=item : item.collapse_childs())
                    but_ungroup.clicked.connect(lambda e,item=item : item.expand_childs())
                
            #------------------------------------------------------------------
            if fields is not None :
                for field in fields :
                    _path = path+[field]
                    _spath = "/".join(_path)
                    self.fm.items[_spath] = Files_TreeItem(self, _path.copy(), parent=self.fm.items[spath], label=field, icon=element.get_field_icon(field), plottable=True)
                    self.fm.items[_spath].setExpanded(states.get(_spath,False))
                
            #------------------------------------------------------------------
            self.fm.elements["/".join([file.alias]+element.path)] = element
            
        #----------------------------------------------------------------------
        self.resizeColumnToContents(0)
        
        self.update_visible()
        
    #==========================================================================
    def remove_file_element(self, element) :
        #----------------------------------------------------------------------
        file = element.file
        file.remove_element(element, logs=True)
        self.update_file(file)
        
    #==========================================================================
    def on_right_click(self, event) :
        #----------------------------------------------------------------------
        item = self.itemAt(event)
        d_obj = self.fm.obj_from_item(item)
        obj = d_obj.get('element')
        field = d_obj.get('field')
         
        #----------------------------------------------------------------------
        menu = QMenu(self.fm.mw)
        
        #----------------------------------------------------------------------
        if isinstance(obj, File) :
            menu.addAction(get_icon('info'), 'Afficher les détails').triggered.connect(obj.details)
            menu.addAction(get_icon('open'), "Ouvrir l'emplacement").triggered.connect(lambda e,dirpath=os.path.dirname(obj.nc_path) : os.startfile(dirpath))
            menu.addAction(get_icon('close'), 'Décharger le fichier').triggered.connect(lambda e,alias=obj.alias : self.fm.remove_file(alias))
            
        #----------------------------------------------------------------------
        elif isinstance(obj, Element) :
            menu.addAction(get_icon('info'), 'Afficher les détails').triggered.connect(lambda e:obj.details(field=field))
            
            if obj.get_attribute(Element.ATTR_COMPUTED, False) :
                menu.addAction(get_icon('close'), 'Supprimer').triggered.connect(lambda e,element=obj:self.remove_file_element(element))
            
        #----------------------------------------------------------------------
        menu.exec_(QCursor.pos())
        
    #==========================================================================
    def update_visible(self) :
        #----------------------------------------------------------------------
        text = self.le_search.text()
        is_text = text != ''
        is_nuls = self.but_nuls.isChecked()
        is_csts = self.but_csts.isChecked()
        is_case = self.but_case.isChecked()
        if not is_case : text = text.upper()
        
        #----------------------------------------------------------------------
        texts = text.split(";")
        
        # TODO : option pour chercher dans le chemin ou juste dans le label
        for item in self.items :
            vmin,vmax = None,None
            if item.plottable :
                d_obj = self.fm.obj_from_item(item)
                element = d_obj.get('element')
                field = d_obj.get('field')
                eclass = type(element).__name__
                if eclass == 'Matrix' : vmin,vmax = element.get_range(field)
            
            hidden = False
            
            if not hidden and is_text :
                test = "/".join(item.path)
                if not is_case : test = test.upper()
                
                found = False
                for _text in texts :
                    if _text in test :
                        found = True
                        break
                if not found : hidden = True
            
            if not hidden and vmin is not None and not is_nuls and vmin == 0.0 and vmax == 0.0 : hidden = True
            if not hidden and vmin is not None and not is_csts and vmin == vmax and vmin != 0.0 : hidden = True
                
            item.setHidden(hidden)
            
    #==========================================================================
    def dragEnterEvent(self, event) :
        #----------------------------------------------------------------------
        filepath = self.get_dropped_filepath(event)
        if filepath is not None :
            event.acceptProposedAction()
            event.setDropAction(Qt.LinkAction)
            
    #==========================================================================
    def dragMoveEvent(self, event) :
        filepath = self.get_dropped_filepath(event)
        if filepath is not None :
            event.acceptProposedAction()
            event.setDropAction(Qt.LinkAction)
                
    #==========================================================================
    def dropEvent(self, event) :
        #----------------------------------------------------------------------
        filepath = self.get_dropped_filepath(event)
        if filepath is not None :
            self.fm.load_file(filepath)
            
    #==========================================================================
    def get_dropped_filepath(self, event) :
        #----------------------------------------------------------------------
        if not event.mimeData().hasUrls() : return None
        urls = event.mimeData().urls()
        if len(urls) == 0 : return None
        
        #----------------------------------------------------------------------
        filepath = urls[0].toLocalFile()
        if filepath.endswith('.nc') : return filepath
        return None
        
    #==========================================================================
    def startDrag(self, supportedActions) :
        #----------------------------------------------------------------------
        item = self.currentItem()
        if not item : return
        
        #----------------------------------------------------------------------
        self.drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText("/".join(item.path))
        self.drag.setMimeData(mime_data)
        self.drag.exec_(Qt.CopyAction)
        
    #==========================================================================
    def get_selected_objects(self) :
        #----------------------------------------------------------------------
        objs = []
        for item in self.selectedItems() :
            if not item.plottable : continue
            d_obj = self.fm.obj_from_item(item)
            if not isinstance(d_obj['element'], Element) : continue
            objs.append(d_obj)
        #----------------------------------------------------------------------
        return objs
        
    #==========================================================================
    def get_selected_items(self) :
        #----------------------------------------------------------------------
        return self.selectedItems()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

