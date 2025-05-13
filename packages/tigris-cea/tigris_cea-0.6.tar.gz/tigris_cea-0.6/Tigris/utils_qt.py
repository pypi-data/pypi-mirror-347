# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
#------------------------------------------------------------------------------
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QEvent, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QFont
from PyQt5.QtWidgets import QApplication, QSplitter, QSplitterHandle, QTreeWidget, QTreeWidgetItem, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QPushButton, QLineEdit, QSpinBox, QCheckBox, QLabel, QComboBox
#------------------------------------------------------------------------------
from Style_Dialog import Style_Dialog
from utils import get_icon_path
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** RESIZABLE GRID WITH SPLITTERS ***
#==============================================================================
class Splitter(QSplitter) :
    
    #==========================================================================
    resized = pyqtSignal()
    INDEX = 1
    
    #==========================================================================
    def __init__(self, orientation, **kwargs) :
        #----------------------------------------------------------------------
        self.index = Splitter.INDEX
        Splitter.INDEX += 1
        
        #----------------------------------------------------------------------
        QSplitter.__init__(self, orientation, **kwargs)
    
    #==========================================================================
    def __repr__(self) :
        return "Splitter({})".format(self.index)
        
    #==========================================================================
    def createHandle(self) :
        #----------------------------------------------------------------------
        return SplitterHandle(self.orientation(), self, self.count())
        
    #==========================================================================
    def set_weights(self, weights) :
        #----------------------------------------------------------------------
        self.weights = weights.copy()
        
    #==========================================================================
    def get_weights(self) :
        #----------------------------------------------------------------------
        if not hasattr(self, 'weights') : return [1]*self.count()
        return self.weights.copy()
        
    #==========================================================================
    def resizeEvent(self, event) :
        #----------------------------------------------------------------------
        super().resizeEvent(event)
        
        #----------------------------------------------------------------------
        self.resized.emit()
        
    #==========================================================================
    def reset_handle(self, index) :
        #----------------------------------------------------------------------
        if   self.orientation() == Qt.Vertical   : S = self.height()
        elif self.orientation() == Qt.Horizontal : S = self.width()
        #----------------------------------------------------------------------
        W = self.get_weights()
        N = sum(W)
        S -= (N-1)*5
        D = S/N
        #----------------------------------------------------------------------
        w = sum(W[:index])
        pos = int(w*D + (w-1)*5)
        self.moveSplitter(pos, index)
        #----------------------------------------------------------------------
        return pos
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SplitterHandle(QSplitterHandle) :
    
    #==========================================================================
    doubleclicked = pyqtSignal(int)
    
    #==========================================================================
    def __init__(self, orientation, splitter, index) :
        #----------------------------------------------------------------------
        self.splitter = splitter
        QSplitterHandle.__init__(self, orientation, self.splitter)
        self.position = None

    #==========================================================================
    def get_pos(self) :
        #----------------------------------------------------------------------
        geom = self.geometry()
        if   self.orientation() == Qt.Vertical   : return geom.y()
        elif self.orientation() == Qt.Horizontal : return geom.x()
    
    #==========================================================================
    def mouseDoubleClickEvent(self, event) :
        #----------------------------------------------------------------------
        index = None
        for _index in range(self.splitter.count()) :
            if self == self.splitter.handle(_index) :
                index = _index
                break
        
        #----------------------------------------------------------------------
        self.doubleclicked.emit(index)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ResizableGrid :
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        self.widgets = []
        self.splitters = []
        self.splitters_sync = []
        self.handle_positions = {}
        
    #==========================================================================
    def reset(self) :
        #----------------------------------------------------------------------
        self.widgets = []
        self.reset_splitters()
        
    #==========================================================================
    def reset_splitters(self) :
        #----------------------------------------------------------------------
        for sp in self.splitters : sp.deleteLater()
        self.splitters = []
        self.splitters_sync = []
        
    #==========================================================================
    def add_widget(self, widget, r0,c0,r1,c1) :
        #----------------------------------------------------------------------
        self.widgets.append((widget, r0,c0,r1,c1))
        
    #==========================================================================
    def get_widget_position(self, widget) :
        #----------------------------------------------------------------------
        for e,(_widget,r0,c0,r1,c1) in enumerate(self.widgets) :
            if widget == _widget :
                return r0,c0,r1,c1
        #----------------------------------------------------------------------
        return None,None,None,None
            
    #==========================================================================
    def replace_widget(self, old_widget, new_widget) :
        #----------------------------------------------------------------------
        for e,(widget,r0,c0,r1,c1) in enumerate(self.widgets) :
            if widget == old_widget :
                self.widgets[e] = (new_widget,r0,c0,r1,c1)
                break
        
        #----------------------------------------------------------------------
        parent = old_widget.parent()
        if isinstance(parent, QSplitter) :
            index = parent.indexOf(old_widget)
            parent.replaceWidget(index, new_widget)
        #----------------------------------------------------------------------
        else :
            raise Exception("le widget à remplacer n'est pas dans un QSplitter")
            
    #==========================================================================
    def add_to_layout(self, layout) :
        #----------------------------------------------------------------------
        self.reset_splitters()
        
        #----------------------------------------------------------------------
        self.NR = self.NC = 0
        widgets = []
        for e,(widget, r0,c0,r1,c1) in enumerate(self.widgets) :
            widgets.append({'widget':widget, 'index':e+1, 'key':(r0,c0,r1,c1), 'children':[]})
            self.NR = max([self.NR, r1+1])
            self.NC = max([self.NC, c1+1])
        
        #----------------------------------------------------------------------
        new_e = len(widgets)+1
        placed_widgets = []
        
        #----------------------------------------------------------------------
        merged = True
        while True :
            if merged is False :
                raise Exception("le découpage de la grille a échoué")
                # break
            
            merged = False
            
            #------------------------------------------------------------------
            for w0,wid0 in enumerate(widgets) : # boucle sur les widgets à tester
                v_wids = [w0]
                h_wids = [w0]
                
                #--------------------------------------------------------------
                for _w,_wid in enumerate(widgets) : # recherche des widgets alignés
                    _r0,_c0,_r1,_c1 = _wid['key']
                    if _w not in h_wids :
                        r0,c0,r1,c1 = widgets[h_wids[-1]]['key']
                        if c0 == _c0 and c1 == _c1 and _r0 == r1+1 :
                            h_wids.append(_w)
                    if _w not in v_wids :
                        r0,c0,r1,c1 = widgets[v_wids[-1]]['key']
                        if r0 == _r0 and r1 == _r1 and _c0 == c1+1 :
                            v_wids.append(_w)
                
                #--------------------------------------------------------------
                splitter = None
                if len(h_wids) > 1 : # alignement v^
                    splitter = Splitter(Qt.Vertical)
                    wids = h_wids
                    for index,h_wid in enumerate(h_wids[1:], start=1) :
                        self.splitters_sync.append((splitter, widgets[h_wid]['key'][0], None, index))
                elif len(v_wids) > 1 : # alignement <->
                    splitter = Splitter(Qt.Horizontal)
                    wids = v_wids
                    for index,v_wid in enumerate(v_wids[1:], start=1) :
                        self.splitters_sync.append((splitter, None, widgets[v_wid]['key'][1], index))
                    
                #--------------------------------------------------------------
                if splitter is not None :
                    self.splitters.append(splitter)
                    splitter.splitterMoved.connect(lambda pos,index,splitter=splitter : self.on_splitterMoved(splitter, pos, index))
                    
                    r0,c0,r1,c1 = widgets[wids[0]]['key']
                    _r0,_c0,_r1,_c1 = widgets[wids[-1]]['key']
                    new_widget = {'widget':splitter, 'index':new_e, 'key':(r0,c0,_r1,_c1), 'children':[]} # caractéristiques du splitter en tant que nouveau widget
                    widgets.append(new_widget)
                    new_e += 1
                    merged = True
                    
                    for w in wids : # ajout des widgets fusionnés dans l'ordre
                        splitter.addWidget(widgets[w]['widget'])
                        new_widget['children'].append(widgets[w]['index'])
                        
                    for w in sorted(wids, reverse=True) : # suppression dans la liste des widgets à tester, donc ordre inverse
                        placed_widgets.append(widgets.pop(w))
                        
                    for index in range(splitter.count()) :
                        splitter.handle(index).doubleclicked.connect(lambda index,splitter=splitter : splitter.reset_handle(index))
                        
                #--------------------------------------------------------------
                if merged : break # on reprend du début si on a réussi à fusionner le widget testé
        
            #------------------------------------------------------------------
            if len(widgets) == 1 : # s'il ne reste qu'un widget, il ne peut pas être fusionné, c'est celui qu'on met dans le layout de la page
                break
            
        #----------------------------------------------------------------------
        splitter = Splitter(Qt.Horizontal)
        splitter.addWidget(widgets[-1]['widget'])
        placed_widgets.append(widgets[-1])
        layout.addWidget(splitter)
        splitter.resized.connect(self.on_resize)
        self.splitters.append(splitter)
        
        #----------------------------------------------------------------------
        for pw in sorted(placed_widgets, key=lambda e:e['index'], reverse=True) : # le tri permet de traiter les plus gros widgets d'abord (clairement pas certain que ce soit important)
            if type(pw['widget']).__name__ != 'Splitter' : continue
            splitter = pw['widget']
            weights = []
            for index,e_child in enumerate(pw['children']) : # calcul théorique de la taille de chaque sous-widget
                child = [w for w in placed_widgets if w['index'] == e_child][0]
                if   splitter.orientation() == Qt.Vertical   : weights.append(child['key'][3]-child['key'][1]+1)
                elif splitter.orientation() == Qt.Horizontal : weights.append(child['key'][2]-child['key'][0]+1)
            splitter.set_weights(weights)
            
        #----------------------------------------------------------------------
        self.reset_sizes()
            
    #==========================================================================
    def reset_sizes(self) :
        #----------------------------------------------------------------------
        for splitter in self.splitters :
            N = splitter.count()
            if N == 1 : continue
            if   splitter.orientation() == Qt.Vertical   : S = splitter.geometry().height()
            elif splitter.orientation() == Qt.Horizontal : S = splitter.geometry().width()
            weights = splitter.get_weights()
            D = (S - (N-1)*5) / N
            sizes = []
            for i in range(splitter.count()) :
                w = weights[i]
                sizes.append(int(w*D + (w-1)*5))
            splitter.setSizes(sizes)
    
    #==========================================================================
    def on_resize(self) :
        #----------------------------------------------------------------------
        for splitter,c,r,index in self.splitters_sync :
            pos = splitter.handle(index).get_pos()
            self.on_splitterMoved(splitter, pos, index)
            
    #==========================================================================
    def on_splitterMoved(self, splitter1, pos, index1) :
        #----------------------------------------------------------------------
        r1,c1 = None,None
        for splitter2,r2,c2,index2 in self.splitters_sync : # recherche de la ligne ou colonne pour la synchro
            if splitter1 == splitter2 and index1 == index2 :
                r1,c1 = r2,c2
                break
        
        #----------------------------------------------------------------------
        for splitter2,r2,c2,index2 in self.splitters_sync : # recherche des autres handles à synchroniser
            if splitter1 == splitter2 and index1 == index2 : continue
            if r1 is not None and (r2 is None or r2 != r1) : continue
            if c1 is not None and (c2 is None or c2 != c1) : continue
            splitter2.blockSignals(True)
            splitter2.moveSplitter(pos, index2)
            splitter2.blockSignals(False)
        
        #----------------------------------------------------------------------
        for S in self.splitters :
            for I in range(S.count()) :
                pos = S.handle(I).get_pos()
                if S == splitter1 and I == index1 : continue
                if (S.index,I) not in self.handle_positions.keys() : continue # pas encore sauvegardé
                if self.handle_positions[(S.index,I)] == pos : continue # pas de déplacement
                self.handle_positions[(S.index,I)] = pos # sauvegarde
                self.on_splitterMoved(S, pos, I)
                
        #----------------------------------------------------------------------
        self.handle_positions = {}
        for S in self.splitters :
            for I in range(S.count()) :
                self.handle_positions[(S.index,I)] = S.handle(I).get_pos()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** TREE ***
#==============================================================================
class TreeWidget(QTreeWidget) :
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        QTreeWidget.__init__(self)
        
        #----------------------------------------------------------------------
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setIndentation(15)
        self.setIconSize(QSize(16, 16))
        
        #----------------------------------------------------------------------
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_right_click)
        
        #----------------------------------------------------------------------
        self.itemCollapsed.connect(lambda item:item.collapse_childs())
        
        #----------------------------------------------------------------------
        # if search :
        #     self.layout_search = QHBoxLayout()
            
        #     self.le_search = QLineEdit()
        #     self.le_search.setToolTip('Recherche dans les items (chemin)\n";" pour plusieurs champs')
        #     self.le_search.setPlaceholderText('Recherche')
        #     self.layout_search.addWidget(self.le_search)
        #     self.le_search.textChanged.connect(self.update_search)
            
        #     self.but_case = get_button('casse', checkable=True, checked=False, tooltip='Respecter la casse')
        #     self.layout_search.addWidget(self.but_case)
        #     self.but_case.clicked.connect(lambda e,le=self.le_search:self.update_search(text=le.text()))
            
        #     but_clear = get_button('clear', tooltip='Vider le champ')
        #     self.layout_search.addWidget(but_clear)
        #     but_clear.clicked.connect(lambda e:self.update_search(text=None))
            
        #----------------------------------------------------------------------
        self.items = []
        self.update_items()
        
    #==========================================================================
    def on_right_click(self, event) :
        #----------------------------------------------------------------------
        pass
    
    #==========================================================================
    def get_item(self, path) :
        for item in self.items :
            if item.path == path : return item
        return None
        
    #==========================================================================
    def expand_to_item(self, path) :
        #----------------------------------------------------------------------
        item = self.get_item(path)
        
        #----------------------------------------------------------------------        
        p = item
        while True :
            if p is None : break
            p.setExpanded(True)
            p = p.parent
        
    #==========================================================================
    def update_items(self) :
        #----------------------------------------------------------------------
        self.save_expanded_state()
        self.items = []
        self.clear()
        
        #----------------------------------------------------------------------
        self._update_items()
        self.set_expanded_state()
    
    #==========================================================================
    def _update_items(self) :
        #----------------------------------------------------------------------
        pass
    
    #==========================================================================
    def save_expanded_state(self) :
        #----------------------------------------------------------------------
        self.states = {"/".join(item.path):item.isExpanded() for item in self.items}
        
    #==========================================================================
    def set_expanded_state(self) :
        #----------------------------------------------------------------------
        for item in self.items :
            spath = "/".join(item.path)
            if spath in self.states :
                item.setExpanded(self.states[spath])
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TreeWidgetItem(QTreeWidgetItem) :
    
    #==========================================================================
    def __init__(self, tree, path, **kwargs) :
        #----------------------------------------------------------------------
        self.tree = tree
        self.path = path
        self.parent = kwargs.pop('parent',None)
        self.label  = kwargs.pop('label',None)
        self.main_widget = kwargs.pop('main_widget',None)
        #----------------------------------------------------------------------
        checkable = kwargs.pop('checkable',False)
        checked   = kwargs.pop('checked',False)
        icon      = kwargs.pop('icon',None)
        expanded  = kwargs.pop('expanded',False)
        widgets   = kwargs.pop('widgets',[])
        weights   = kwargs.pop('weights',None)
        
        #----------------------------------------------------------------------
        self.opts = kwargs.copy()
        
        #----------------------------------------------------------------------
        if self.label is None : self.label = self.path[-1]
        
        #----------------------------------------------------------------------
        QTreeWidgetItem.__init__(self, [''])
        
        #----------------------------------------------------------------------
        if self.parent is None or self.parent == self.tree :
            self.is_top_level = True
            self.tree.addTopLevelItem(self)
        else :
            self.is_top_level = False
            self.parent.addChild(self)
            
        #----------------------------------------------------------------------
        self.main_frame = QFrame()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(2)
        self.main_frame.setLayout(self.main_layout)
        self.tree.setItemWidget(self, 0, self.main_frame)
        
        #----------------------------------------------------------------------
        self.widgets = []
        if self.main_widget is None :
            if checkable :
                self.main_widget = QCheckBox(self.label)
                self.main_widget.setChecked(checked)
            else :
                self.main_widget = QLabel(self.label)
        #----------------------------------------------------------------------
        self.main_layout.addWidget(self.main_widget)
        self.widgets.append(self.main_widget)
        
        #----------------------------------------------------------------------
        if len(widgets) == 0 :
            self.main_layout.addStretch()
        #----------------------------------------------------------------------
        else :
            if weights is None : self.main_layout.addStretch()
            else : self.main_layout.setStretch(0, 0)
            for w,widget in enumerate(widgets) :
                self.widgets.append(widget)
                self.main_layout.addWidget(widget)
                if weights is not None :
                    self.main_layout.setStretch(w+1, weights[w])
            
        #----------------------------------------------------------------------
        if icon is not None :
            self.setIcon(0, get_icon(icon, (16,16)))
        
        #----------------------------------------------------------------------
        self.setExpanded(expanded)
        
        #----------------------------------------------------------------------
        self.tree.items.append(self)
        
    #==========================================================================
    def collapse_childs(self) :
        #----------------------------------------------------------------------
        self.setExpanded(False)
        for i in range(self.childCount()) :
            self.child(i).collapse_childs()
        
    #==========================================================================
    def expand_childs(self) :
        #----------------------------------------------------------------------
        self.setExpanded(True)
        for i in range(self.childCount()) :
            self.child(i).expand_childs()
        
    #==========================================================================
    def setDisabled(self, state) :
        #----------------------------------------------------------------------
        for w in self.widgets :
            w.setEnabled(not state)
            
        #----------------------------------------------------------------------
        QTreeWidgetItem.setDisabled(self, state)
        
    #==========================================================================
    def setHidden(self, state) :
        #----------------------------------------------------------------------
        QTreeWidgetItem.setHidden(self, state)
        
        #----------------------------------------------------------------------
        if not self.is_top_level :
            if not state and self.parent.isHidden() : # item visible, alors parent aussi
                self.parent.setHidden(False)
                
            elif state :
                self.parent.check_hidden_now()
                
    #==========================================================================
    def check_hidden_now(self) :
        #----------------------------------------------------------------------
        if self.isHidden() :
            return
        
        #----------------------------------------------------------------------
        hidden = True
        for i in range(self.childCount()) :
            if not self.child(i).isHidden() :
                hidden = False
                break
        if hidden :
            self.setHidden(True)
                
    #==========================================================================
    def align_children(self) :
        #----------------------------------------------------------------------
        widgets = []
        for i in range(self.childCount()) :
            widgets.append(self.child(i).main_widget)
            
        Wmax = max([w.sizeHint().width() for w in widgets])+8
        for w in widgets :
            w.setMinimumWidth(Wmax)
            w.setMaximumWidth(Wmax)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** UI ELEMENTS ***
#==============================================================================
class LogsWidget(QTextEdit) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        self.mw = mw
        
        #----------------------------------------------------------------------
        QTextEdit.__init__(self)
        
        #----------------------------------------------------------------------
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        font = QFont("Courier New", 10)
        self.setFont(font)
        
    #==========================================================================
    def redirect(self) :
        #----------------------------------------------------------------------
        sys.stdout = self
        
    #==========================================================================
    def write(self, text) :
        #----------------------------------------------------------------------
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        
        #----------------------------------------------------------------------
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
    #==========================================================================
    def flush(self) :
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyLineEdit(QLineEdit) :
    
    #==========================================================================
    def __init__(self, text, placeholderText='') :
        #----------------------------------------------------------------------
        QLineEdit.__init__(self, text)
        self.setPlaceholderText(placeholderText)
        
        #----------------------------------------------------------------------
        self.textChanged.connect(self.on_edit)
        self.editingFinished.connect(self.on_editing_finished)
        
    #==========================================================================
    def on_edit(self) :
        #----------------------------------------------------------------------
        font = self.font()
        font.setItalic(True)
        self.setFont(font)
        
    #==========================================================================
    def on_editing_finished(self) :
        #----------------------------------------------------------------------
        font = self.font()
        font.setItalic(False)
        self.setFont(font)
        
        if self.text() == '' :
            self.blockSignals(True)
            self.setText(self.placeholderText())
            self.blockSignals(False)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MySpinBox(QSpinBox) :
    
    #==========================================================================
    # edited = pyqtSignal(int)
    changed = pyqtSignal(int)
    
    #==========================================================================
    def __init__(self, value, vmin, vmax, timer=False) :
        #----------------------------------------------------------------------
        QSpinBox.__init__(self)
        
        #----------------------------------------------------------------------
        self.setValue(value)
        self.setRange(vmin,vmax)
        self.setMinimumWidth(44)
        
        #----------------------------------------------------------------------
        if vmin == 1 :
            self.setSuffix('/{:.3G}'.format(vmax))
        
        self.valueChanged.connect(self.on_edit)
        self.installEventFilter(self)
        
        #----------------------------------------------------------------------
        if timer :
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.emit_changed)
            self.valueChanged.connect(self.on_value_changed)
            
        else :
            self.valueChanged.connect(self.emit_changed)
            
    #==========================================================================
    def on_edit(self) :
        #----------------------------------------------------------------------
        font = self.font()
        font.setItalic(True)
        self.setFont(font)
        
    #==========================================================================
    def eventFilter(self, source, event) :
        if (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return) :
            self.timer.stop()
            self.emit_changed()
            return True
        return super().eventFilter(source, event)
    
    #==========================================================================
    def on_editing_finished(self) :
        #----------------------------------------------------------------------
        self.timer.stop()
        font = self.font()
        font.setItalic(False)
        self.setFont(font)
        #----------------------------------------------------------------------
        self.changed.emit(self.value())
            
    #==========================================================================
    def on_value_changed(self) :
        #----------------------------------------------------------------------
        self.on_edit()
        self.timer.stop()
        self.timer.start(200)
            
    #==========================================================================
    def emit_changed(self) :
        #----------------------------------------------------------------------
        self.timer.stop()
        
        font = self.font()
        font.setItalic(False)
        self.setFont(font)
        
        self.changed.emit(self.value())
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** UI FUCNTIONS ***
#==============================================================================
def get_line(orientation) :
    line = QFrame()
    if   orientation == Qt.Horizontal : line.setFrameShape(QFrame.HLine)
    elif orientation == Qt.Vertical   : line.setFrameShape(QFrame.VLine)
    line.setFrameShadow(QFrame.Sunken)
    return line
    
#==============================================================================
def get_icon(name, size=None) :
    #--------------------------------------------------------------------------
    path = get_icon_path(name)
    pix = QPixmap(path)
    
    #--------------------------------------------------------------------------
    if size is not None :
        w,h = size
        pix = pix.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
    #--------------------------------------------------------------------------
    return QIcon(pix)
    
#==============================================================================
def get_button(icon, hsize=19, vsize=19, flat=True, checkable=False, checked=False, checked_icon=None, tooltip=None) :
    #--------------------------------------------------------------------------
    but = QPushButton()
    but.setIcon(get_icon(icon))
    but.setMinimumWidth(hsize)
    but.setMaximumWidth(hsize)
    but.setMinimumHeight(vsize)
    but.setMaximumHeight(vsize)
    but.setFlat(flat)
    #--------------------------------------------------------------------------
    if tooltip is not None : but.setToolTip(tooltip)
    #--------------------------------------------------------------------------
    styleSheet = "QPushButton {padding: 0px;}\nQPushButton:pressed {border: 1px solid #09599d; padding: 0px;}"
    if checkable :
        but.setCheckable(True)
        but.setChecked(checked)
        if checked_icon is not None :
            but.setIcon(get_icon(icon if checked else checked_icon))
            but.clicked.connect(lambda v,but=but:but.setIcon(get_icon(icon if v else checked_icon)))
            styleSheet += "\nQPushButton:checked {border: 0px; padding: 0px;}\nQPushButton:checked:pressed {border: 1px solid #09599d; padding: 0px;}"
    #--------------------------------------------------------------------------
    but.setStyleSheet(styleSheet)
    #--------------------------------------------------------------------------
    return but
    
#==============================================================================
def get_spin(value, vmin, vmax, timer=False) :
    #--------------------------------------------------------------------------
    return MySpinBox(value, vmin, vmax, timer)

#==============================================================================
def get_combo(items, text=None, index=None) :
    #--------------------------------------------------------------------------
    co = QComboBox()
    co.addItems(items)
        
    #--------------------------------------------------------------------------
    if text is not None : co.setCurrentText(text)
    if index is not None : co.setCurrentIndex(index)
    
    #--------------------------------------------------------------------------
    return co

#==============================================================================
def get_style(engine, style={}, **kwargs) :
    #--------------------------------------------------------------------------
    dialog = Style_Dialog(engine, style, **kwargs)
    dialog.exec()
    #--------------------------------------------------------------------------
    return dialog.style

#==============================================================================
def question_box(style, title, text, buttons=[], default=None) :
    #--------------------------------------------------------------------------
    msg = QMessageBox()
    msg.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icons", "icon.png")))
    msg.setWindowTitle(title)
    msg.setIcon({'information' : QMessageBox.Information,
                 'question'    : QMessageBox.Question,
                 'warning'     : QMessageBox.Warning,
                 'critical'    : QMessageBox.Critical,
                 }.get(style,QMessageBox.Information))
    msg.setText(text)
    
    #--------------------------------------------------------------------------
    if default is None : default = buttons[0][0]
    
    #--------------------------------------------------------------------------
    btypes = {'Ok':QMessageBox.Ok, 'Yes':QMessageBox.Yes, 'No':QMessageBox.No, 'Cancel':QMessageBox.Cancel}
    for binfos in reversed(buttons) :
        but = msg.addButton(btypes[binfos[0]])
        but.setText(binfos[1])
        if len(binfos) == 3 :
            but.setIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icons", binfos[2]+".png")))
        if binfos[0] == default :
            msg.setDefaultButton(btypes[binfos[0]])
            msg.setEscapeButton(btypes[binfos[0]])
    
    #--------------------------------------------------------------------------
    rep = msg.exec_()
    _btypes = {v:k for k,v in btypes.items()}
    return _btypes[rep]

#==============================================================================
def clear_layout(layout) :
    #--------------------------------------------------------------------------
    while layout.count() :
        item = layout.takeAt(0)
        widget = item.widget()
        if widget :
            widget.setParent(None)
            widget.deleteLater()
    layout.update()
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


