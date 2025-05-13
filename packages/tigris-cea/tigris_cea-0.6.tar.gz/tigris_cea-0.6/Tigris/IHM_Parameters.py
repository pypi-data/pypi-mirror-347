# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from PyQt5.QtWidgets import QLabel, QSpinBox, QMenu, QFrame, QVBoxLayout
from PyQt5.QtGui import QCursor
#------------------------------------------------------------------------------
from Graph_Style import Graph_Style
from utils_qt import TreeWidget, TreeWidgetItem
from utils_qt import get_button, get_spin, get_style, MyLineEdit, get_combo, get_icon
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Parameters_Manager :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        self.mw = mw
        
        #----------------------------------------------------------------------
        self.gtrees = {} # page.index -> Graphs_Tree
        self.etrees = {} # page.index -> Elements_Tree
        self.ftrees = {} # page.index -> Files_Tree
        
        #----------------------------------------------------------------------
        self.mw.pages_manager.tab_widget.page_added.connect(self.on_page_added)
        self.mw.pages_manager.tab_widget.page_removed.connect(self.on_page_removed)
        self.mw.pages_manager.tab_widget.currentChanged.connect(self.on_page_changed)
        
        #----------------------------------------------------------------------
        self.udpate_docks()
        
    #==========================================================================
    def on_page_added(self, index) :
        #----------------------------------------------------------------------
        page = self.mw.pages_manager.get_page(page_index=index)
        
        self.gtrees[index] = gtree = Graphs_Tree(self, page)
        self.mw.stacked_graphs.addWidget(gtree)
        self.mw.stacked_graphs.setCurrentWidget(gtree)
        
        self.etrees[index] = etree = Elements_Tree(self, page)
        self.mw.stacked_elements.addWidget(etree)
        self.mw.stacked_elements.setCurrentWidget(etree)
        
        self.ftrees[index] = ftree = Files_Tree(self, page)
        self.mw.stacked_files.addWidget(ftree)
        self.mw.stacked_files.setCurrentWidget(ftree)
        
        #----------------------------------------------------------------------
        self.udpate_docks()
        
    #==========================================================================
    def on_page_removed(self, index) :
        #----------------------------------------------------------------------
        gtree = self.gtrees[index]
        self.mw.stacked_graphs.removeWidget(gtree)
        gtree.deleteLater()

        #----------------------------------------------------------------------
        etree = self.etrees[index]
        self.mw.stacked_elements.removeWidget(etree)
        etree.deleteLater()

        #----------------------------------------------------------------------
        ftree = self.ftrees[index]
        self.mw.stacked_files.removeWidget(ftree)
        ftree.deleteLater()
        
        #----------------------------------------------------------------------
        self.udpate_docks()
        
    #==========================================================================
    def udpate_docks(self) :
        #----------------------------------------------------------------------
        # pass
        self.mw.dock_elements.setVisible(not self.mw.action_combiner.isChecked() and self.mw.stacked_elements.count()>0)
        self.mw.dock_graphs.setVisible(not self.mw.action_combiner.isChecked() and self.mw.stacked_graphs.count()>0)
        
    #==========================================================================
    def on_page_changed(self, tab_index) :
        #----------------------------------------------------------------------
        page = self.mw.pages_manager.get_page(tab_index=tab_index)
        if page is None : return
        if page.index not in self.gtrees : return
        
        #----------------------------------------------------------------------
        self.mw.stacked_graphs.setCurrentWidget(self.gtrees[page.index])
        self.mw.stacked_elements.setCurrentWidget(self.etrees[page.index])
        self.mw.stacked_files.setCurrentWidget(self.ftrees[page.index])
        
    #==========================================================================
    def update_items(self, page) :
        #----------------------------------------------------------------------
        self.gtrees[page.index].update_items()
        self.ftrees[page.index].update_items()
        self.etrees[page.index].update_items()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graphs_Tree(TreeWidget) :
    
    #==========================================================================
    def __init__(self, manager, page) :
        #----------------------------------------------------------------------
        self.manager = manager
        self.page = page
        
        #----------------------------------------------------------------------
        TreeWidget.__init__(self)
    
    #==========================================================================
    def _update_items(self) :
        #----------------------------------------------------------------------
        self.clear()
        if self.page.graphs is None : return
        
        #----------------------------------------------------------------------
        for graph in self.page.graphs :
            gc = graph.graph_config
            gs = graph.style
            
            #------------------------------------------------------------------
            if gc.gtype == '1D' : icon = gc.dimensions[0]
            else                : icon = gc.gtype
            
            #------------------------------------------------------------------
            graph_item = TreeWidgetItem(self, [graph.name], icon=icon, expanded=True)
            
            
            #---- figure title ------------------------------------------------
            le_title_text = MyLineEdit(gs.get('title.text'), gs.get('title.default_text'))
            le_title_text.editingFinished.connect(lambda gs=gs, k='title.text', le=le_title_text : gs.set(k,le.text() if le.text() != '' else le.placeholderText()))
            but_title_style = get_button('style_font')
            but_title_style.clicked.connect(lambda e, gs=gs, k='title.style', text=gs.get('title.text'), engine=graph.engine : gs.set(k, get_style(engine, gs.get(k), preview_text=text)))
            item_title = TreeWidgetItem(self, [graph.name, 'title'], label='Titre', parent=graph_item, checkable=True, checked=gs.get('title.is_active'), widgets=[le_title_text, but_title_style], weights=[1,0])
            item_title.main_widget.clicked.connect(lambda v, gs=gs, k='title.is_active' : gs.set(k,v))
            
            #---- legende -----------------------------------------------------
            co_legend_pos = get_combo(Graph_Style.get_options('legend.pos'), text=gs.get('legend.pos'))
            co_legend_pos.currentTextChanged.connect(lambda v,gs=gs, k='legend.pos' : gs.set(k,v))
            item_legend = TreeWidgetItem(self, [graph.name, 'legend'], label='Légende', parent=graph_item, checkable=True, checked=gs.get('legend.is_active'), widgets=[co_legend_pos], weights=[1])
            item_legend.main_widget.clicked.connect(lambda v, gs=gs, k='legend.is_active' : gs.set(k,v))
                
            #---- grid --------------------------------------------------------
            if graph.engine == 'MPL' :
                but_grid_style = get_button('style_line')
                but_grid_style.clicked.connect(lambda e, gs=gs, k='grid.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k))))
                item_grid = TreeWidgetItem(self, [graph.name, 'grid'], label='Grille', parent=graph_item, checkable=True, checked=gs.get('grid.is_active'), widgets=[but_grid_style])
                item_grid.main_widget.clicked.connect(lambda v, gs=gs, k='grid.is_active' : gs.set(k,v))
                
                
            #---- axis --------------------------------------------------------
            if   graph.engine == 'MPL' : _axis = ['xaxis','yaxis']
            elif graph.engine == 'VTK' : _axis = ['xaxis','yaxis','zaxis']
            #------------------------------------------------------------------
            axes_item = TreeWidgetItem(self, [graph.name, 'Axes'], label='Axes', parent=graph_item, checkable=True, checked=gs.get('axes.is_active'))
            axes_item.main_widget.clicked.connect(lambda v, gs=gs, k='axes.is_active' : gs.set(k,v))
            #------------------------------------------------------------------
            for axis in _axis :
                axis_item = TreeWidgetItem(self, [graph.name, axis], label=gs.get(axis+".name"), parent=axes_item, checkable=True, checked=gs.get(axis+'.is_active'))
                axis_item.main_widget.clicked.connect(lambda v, gs=gs, k=axis+'.is_active' : gs.set(k,v))
                #--------------------------------------------------------------
                le_title_text = MyLineEdit(gs.get(axis+'.title.text'), gs.get(axis+'.title.default_text'))
                le_title_text.editingFinished.connect(lambda gs=gs, k=axis+'.title.text', le=le_title_text : gs.set(k,le.text() if le.text() != '' else le.placeholderText()))
                but_title_style = get_button('style_font')
                but_title_style.clicked.connect(lambda e, gs=gs, k=axis+'.title.style', text=gs.get(axis+'.title.text'), engine=graph.engine : gs.set(k, get_style(engine, gs.get(k), preview_text=text)))
                item_title = TreeWidgetItem(self, [graph.name, axis, 'title'], label='Titre', parent=axis_item, checkable=True, checked=gs.get(axis+'.title.is_active'), widgets=[le_title_text, but_title_style], weights=[1,0])
                item_title.main_widget.clicked.connect(lambda v, gs=gs, k=axis+'.title.is_active' : gs.set(k,v))
                #--------------------------------------------------------------
                co_ticks_format = get_combo(Graph_Style.get_options('ticks.format'), text=gs.get(axis+'.ticks.format'))
                co_ticks_format.currentTextChanged.connect(lambda v,gs=gs, k=axis+'.ticks.format' : gs.set(k,v))
                sp_ticks_decimals = QSpinBox()
                sp_ticks_decimals.setSuffix('   ')
                sp_ticks_decimals.setRange(0,9)
                sp_ticks_decimals.setValue(gs.get(axis+'.ticks.decimals'))
                sp_ticks_decimals.valueChanged.connect(lambda v,gs=gs, k=axis+'.ticks.decimals' : gs.set(k,v))
                but_ticks_style = get_button('style_font')
                but_ticks_style.clicked.connect(lambda e, gs=gs, k=axis+'.ticks.style', text=gs.get(axis+'.ticks.text'), engine=graph.engine : gs.set(k, get_style(engine, gs.get(k), preview_text=text)))
                item_ticks = TreeWidgetItem(self, [graph.name, axis, 'ticks'], label='Ticks', parent=axis_item, checkable=True, checked=gs.get(axis+'.ticks.is_active'), widgets=[co_ticks_format, sp_ticks_decimals, but_ticks_style], weights=[1,0,0])
                item_ticks.main_widget.clicked.connect(lambda v, gs=gs, k=axis+'.ticks.is_active' : gs.set(k,v))
                #--------------------------------------------------------------
                but_line_style = get_button('style_line')
                but_line_style.clicked.connect(lambda e, gs=gs, k=axis+'.line.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k))))
                item_line = TreeWidgetItem(self, [graph.name, axis, 'line'], label='Ligne', parent=axis_item, checkable=True, checked=gs.get(axis+'.line.is_active'), widgets=[but_line_style])
                item_line.main_widget.clicked.connect(lambda v, gs=gs, k=axis+'.line.is_active' : gs.set(k,v))
                
                
                #---- range ---------------------------------------------------
                if gs.has(axis+'.min.is_active') :
                    vmin,vmax = gs.get(axis+'.min.text'),gs.get(axis+'.max.text')
                    
                    le_vmin_text = MyLineEdit(gs.get(axis+'.min.text'), vmin)
                    le_vmin_text.editingFinished.connect(lambda le=le_vmin_text,k=axis+'.min.text',gs=gs : gs.set(k,le.text()))
                    item_vmin = TreeWidgetItem(self, [graph.name, axis, 'range', 'min'], label='Min', parent=axis_item, checkable=True, checked=gs.get(axis+'.min.is_active'), widgets=[le_vmin_text], weights=[1])
                    item_vmin.main_widget.clicked.connect(lambda v,k=axis+'.min.is_active',gs=gs : gs.set(k,v))
                    
                    le_vmax_text = MyLineEdit(gs.get(axis+'.max.text'), vmax)
                    le_vmax_text.editingFinished.connect(lambda le=le_vmax_text,k=axis+'.max.text',gs=gs : gs.set(k,le.text()))
                    item_vmax = TreeWidgetItem(self, [graph.name, axis, 'range', 'max'], label='Max', parent=axis_item, checkable=True, checked=gs.get(axis+'.max.is_active'), widgets=[le_vmax_text], weights=[1])
                    item_vmax.main_widget.clicked.connect(lambda v,k=axis+'.max.is_active',gs=gs : gs.set(k,v))
                    
                #--------------------------------------------------------------
                axis_item.align_children()
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Elements_Tree(TreeWidget) :
    
    #==========================================================================
    def __init__(self, manager, page) :
        #----------------------------------------------------------------------
        self.manager = manager
        self.page = page
        self.positions = {} # [(ge.index,dim)] = indice
        
        #----------------------------------------------------------------------
        TreeWidget.__init__(self)
    
    #==========================================================================
    def on_right_click(self, event) :
        #----------------------------------------------------------------------
        item = self.itemAt(event)
        if item is None : return
        
        ge = item.opts.get('graph_element',None)
        
        if ge is not None :
            
            menu = QMenu(self.manager.mw)
            
            menu.addAction(get_icon('info'), 'Afficher les détails').triggered.connect(lambda e,element=ge.element, field=ge.opts.get('field',None):element.details(field=field))
            
            if ge.style.has('slice.is_active') :
                menu_slice = QMenu("Ajouter une slice", self.manager.mw)
                menu_slice.setIcon(get_icon('slice'))
                for plan in ['XY','XZ','YZ'] :
                    menu_slice.addAction(get_icon('slice'), 'Plan {}'.format(plan)).triggered.connect(lambda e,plan=plan : ge.add_slice(plan=plan))
                    menu.addMenu(menu_slice)
                    
            menu.exec_(QCursor.pos())
        
    #==========================================================================
    def _update_items(self) :
        #----------------------------------------------------------------------
        self.clear()
        if self.page.graphs is None : return
        
        #----------------------------------------------------------------------
        self.pos_spins = {}
        self.slice_spins = {}
        
        #----------------------------------------------------------------------
        for graph in self.page.graphs :
            if len(graph.graph_elements) == 0 : continue
            gc = graph.graph_config
            gclass = type(graph).__name__
            
            #------------------------------------------------------------------
            if gc.gtype == '1D' : icon = gc.dimensions[0]
            else                : icon = gc.gtype
            
            #------------------------------------------------------------------
            graph_item = TreeWidgetItem(self, [graph.name], icon=icon, expanded=True)
            
            #------------------------------------------------------------------
            for _g,ge in enumerate(graph.graph_elements) :
                gs = ge.style
                pclass = None if ge.plotted is None else type(ge.plotted.plotted).__name__
                eclass = type(ge.element).__name__
                if gs.has('slice.is_active') == True and gclass != 'Graph_VTK' : continue
                
                
                #---- element -------------------------------------------------
                widgets = []
                
                z_frame = QFrame()
                z_box = QVBoxLayout()
                z_box.setContentsMargins(0,0,0,0)
                z_box.setSpacing(0)
                but_zup = get_button('move_up', vsize=9)
                but_zdown = get_button('move_down', vsize=9)
                but_zup.clicked.connect(lambda e, ge=ge, d='up' : ge.graph.move_element(ge, d))
                but_zdown.clicked.connect(lambda e, ge=ge, d='down' : ge.graph.move_element(ge, d))
                but_zup.setEnabled(_g > 0)
                but_zdown.setEnabled(_g < len(graph.graph_elements)-1)
                z_box.addWidget(but_zup)
                z_box.addWidget(but_zdown)
                z_frame.setLayout(z_box)
                widgets.append(z_frame)
                
                #---- highlight -----------------------------------------------
                if gs.has('highlight.is_active') :
                    but_highlight = get_button('highlight', checkable=True, checked=gs.get('highlight.is_active'))
                    but_highlight.clicked.connect(lambda v,k='highlight.is_active',gs=gs : gs.set(k,v))
                    widgets.append(but_highlight)
                    
                #---- inspector -----------------------------------------------
                if gs.has('inspector.is_active') :
                    but_inspector = get_button('scan', checkable=True, checked=gs.get('inspector.is_active'))
                    but_inspector.clicked.connect(lambda v,k='inspector.is_active',gs=gs : gs.set(k,v))
                    widgets.append(but_inspector)
                    
                #---- hidden --------------------------------------------------
                but_hide = get_button('hidden', checkable=True, checked=not gs.get('element.is_active'), checked_icon='visible')
                but_hide.clicked.connect(lambda v,k='element.is_active',gs=gs : gs.set(k,not v))
                widgets.append(but_hide)
                
                #---- close ---------------------------------------------------
                but_remove = get_button('close')
                but_remove.clicked.connect(lambda e,graph=graph,ge=ge : graph.remove_element(ge))
                widgets.append(but_remove)
                
                #--------------------------------------------------------------
                item_element = TreeWidgetItem(self, [graph.name, ge.label], parent=graph_item, icon=ge.get_icon(), widgets=widgets, graph_element=ge)
                
                
                #---- slice ---------------------------------------------------
                if gs.get('slice.is_active') == True :
                    dim = {'XY':'Z', 'XZ':'Y', 'YZ':'X'}[gs.get('slice.plan')]
                    N = ge.element.get_dim_size(dim)
                    I = gs.get('slice.position')
                    spin = get_spin(I, 1, N, timer=True)
                    label = QLabel(dim+'='+' -> '.join(["{:.5G}".format(v) for v in ge.element.get_dim_value(dim,I-1)]))
                    spin.valueChanged.connect(lambda I,ge=ge,dim=dim,label=label : label.setText(dim+'='+' -> '.join(["{:.5G}".format(v) for v in ge.element.get_dim_value(dim,I-1)])))
                    spin.changed.connect(lambda I,gs=gs : gs.set('slice.position',I-1))
                    TreeWidgetItem(self, [graph.name, ge.label, 'slice'], parent=item_element, main_widget=spin, icon=dim, widgets=[label], weights=[1])
                    
                
                #---- position ------------------------------------------------
                if len(ge.element.get_dimensions()) > 0 :
                    pos_item = TreeWidgetItem(self, [graph.name, ge.label, 'sync'], label='Synchroniser', parent=item_element, checkable=True, checked=gs.get('sync.is_active'))
                    pos_item.main_widget.clicked.connect(lambda v,k='sync.is_active',gs=gs : gs.set(k,v))
                    for dim in ge.element.get_dimensions() :
                        N = ge.element.get_dim_size(dim)
                        is_edge = ge.element.is_dim_edge(dim)
                        I = self.positions.get((ge.index,dim),0)+1
                        
                        self.pos_spins[(ge.index,dim)] = spin = get_spin(I, 1, N, timer=True)
                        
                        if is_edge :
                            label = QLabel(dim+'='+' -> '.join(["{:.5G}".format(v) for v in ge.element.get_dim_value(dim,I-1)]))
                            spin.valueChanged.connect(lambda I,ge=ge,dim=dim,label=label : label.setText(dim+'='+' -> '.join(["{:.5G}".format(v) for v in ge.element.get_dim_value(dim,I-1)])))
                        else :
                            label = QLabel(dim+'='+"{:.5G}".format(ge.element.get_dim_value(dim,I-1)))
                            spin.valueChanged.connect(lambda I,ge=ge,dim=dim,label=label : label.setText(dim+'='+"{:.5G}".format(ge.element.get_dim_value(dim,I-1))))
                        
                        dim_item = TreeWidgetItem(self, [graph.name, ge.label, 'sync', dim], parent=pos_item, main_widget=spin, icon=dim, widgets=[label], weights=[1])
                        
                        if dim in gc.dimensions :
                            dim_item.setDisabled(True)
                        else :
                            spin.changed.connect(lambda I,ge=ge,dim=dim : self.position_changed(ge, dim, I-1))
                            pos_item.main_widget.clicked.connect(lambda v,ge=ge,item=dim_item,dim=dim : self.get_item(item.path).setDisabled(v and ge.element.file.get_dim_size(dim) is not None))
                            pos_item.main_widget.clicked.connect(lambda e,spin=spin,ge=ge,dim=dim : self.position_changed(ge, dim, spin.value()-1))
                            dim_item.setDisabled(gs.get('sync.is_active') and ge.element.file.get_dim_size(dim) is not None)
                        
                    #--------------------------------------------------------------
                    if len(self.pos_spins.values()) > 0 :
                        w = max([spin.sizeHint().width()+5 for spin in self.pos_spins.values()])
                        for spin in self.pos_spins.values() : spin.setMinimumWidth(w)
        
                #---- legend --------------------------------------------------
                if not ge.is_linked() :
                    default = gs.get('legend.default_text')
                    if eclass == 'Matrix' and ge.opts.get('field') is not None : default = ge.element.label + "_" + ge.opts['field']
                    le_legend_text = MyLineEdit(gs.get('legend.text'), default)
                    le_legend_text.editingFinished.connect(lambda le=le_legend_text,k='legend.text',gs=gs : gs.set(k,le.text() if le.text() != '' else le.placeholderText()))
                    item_legend = TreeWidgetItem(self, [graph.name, ge.label, 'legend'], label='Légende', parent=item_element, checkable=True, checked=gs.get('legend.is_active'), widgets=[le_legend_text], weights=[1])
                #--------------------------------------------------------------
                else : item_legend = TreeWidgetItem(self, [graph.name, ge.label, 'legend'], label='Légende', parent=item_element, checkable=True, checked=gs.get('legend.is_active'))
                item_legend.main_widget.clicked.connect(lambda v,k='legend.is_active',gs=gs : gs.set(k,v))
                
                #---- range ---------------------------------------------------
                if ge.cbar is not None :
                    vmin,vmax = ge.element.get_range(ge.opts.get('field'))
                    _vmin,_vmax = gs.get('range.min.text'),gs.get('range.max.text')
                    if _vmin == '' : gs.set('range.min.text',str(vmin))
                    if _vmax == '' : gs.set('range.max.text',str(vmax))
                    
                    le_vmin_text = MyLineEdit(gs.get('range.min.text'), "{:.5E}".format(vmin))
                    le_vmin_text.editingFinished.connect(lambda le=le_vmin_text,k='range.min.text',gs=gs : gs.set(k,le.text()))
                    # but_hide_min = get_button('hidden', checkable=True, checked=gs.get('range.min.hide'), checked_icon='visible')
                    # but_hide_min.clicked.connect(lambda v,k='range.min.hide',gs=gs : gs.set(k,v))
                    item_vmin = TreeWidgetItem(self, [graph.name, ge.label, 'range', 'min'], label='Min', parent=item_element, checkable=True, checked=gs.get('range.min.is_active'), widgets=[le_vmin_text], weights=[1,0])
                    item_vmin.main_widget.clicked.connect(lambda v,k='range.min.is_active',gs=gs : gs.set(k,v))
                    
                    le_vmax_text = MyLineEdit(gs.get('range.max.text'), "{:.5E}".format(vmax))
                    le_vmax_text.editingFinished.connect(lambda le=le_vmax_text,k='range.max.text',gs=gs : gs.set(k,le.text()))
                    # but_hide_max = get_button('hidden', checkable=True, checked=gs.get('range.max.hide'), checked_icon='visible')
                    # but_hide_max.clicked.connect(lambda v,k='range.max.hide',gs=gs : gs.set(k,v))
                    item_vmax = TreeWidgetItem(self, [graph.name, ge.label, 'range', 'max'], label='Max', parent=item_element, checkable=True, checked=gs.get('range.max.is_active'), widgets=[le_vmax_text], weights=[1,0])
                    item_vmax.main_widget.clicked.connect(lambda v,k='range.max.is_active',gs=gs : gs.set(k,v))
                
                #---- fill ----------------------------------------------------
                if gs.has('fill.is_active') :
                    but_fill_style = get_button('style_fill')
                    but_fill_style.clicked.connect(lambda e, gs=gs, k='fill.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k))))
                    item_fill = TreeWidgetItem(self, [graph.name, ge.label, 'fill'], label='Remplissage', parent=item_element, checkable=True, checked=gs.get('fill.is_active'), widgets=[but_fill_style])
                    item_fill.main_widget.clicked.connect(lambda v, gs=gs, k='fill.is_active' : gs.set(k,v))
                    
                #---- line ----------------------------------------------------
                if gs.has('line.is_active') :
                    but_line_style = get_button('style_line')
                    but_line_style.clicked.connect(lambda e, gs=gs, k='line.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k))))
                    item_line = TreeWidgetItem(self, [graph.name, ge.label, 'line'], label='Ligne', parent=item_element, checkable=True, checked=gs.get('line.is_active'), widgets=[but_line_style])
                    item_line.main_widget.clicked.connect(lambda v, gs=gs, k='line.is_active' : gs.set(k,v))
                
                #---- border --------------------------------------------------
                if gs.has('border.is_active') :
                    but_border_style = get_button('style_line')
                    but_border_style.clicked.connect(lambda e, gs=gs, k='border.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k))))
                    item_border = TreeWidgetItem(self, [graph.name, ge.label, 'border'], label='Bordure', parent=item_element, checkable=True, checked=gs.get('border.is_active'), widgets=[but_border_style])
                    item_border.main_widget.clicked.connect(lambda v, gs=gs, k='border.is_active' : gs.set(k,v))
                
                #---- mark ----------------------------------------------------
                if gs.has('mark.is_active') and pclass != 'LineCollection' :
                    but_mark_style = get_button('style_marker')
                    but_mark_style.clicked.connect(lambda e, gs=gs, k='mark.style', engine=graph.engine : gs.set(k, get_style(engine, gs.get(k), skips=['mark_alpha'] if gs.get('line.is_active') else [])))
                    item_mark = TreeWidgetItem(self, [graph.name, ge.label, 'mark'], label='Marqueur', parent=item_element, checkable=True, checked=gs.get('mark.is_active'), widgets=[but_mark_style])
                    item_mark.main_widget.clicked.connect(lambda v, gs=gs, k='mark.is_active' : gs.set(k,v))
                
                #--------------------------------------------------------------
                item_element.align_children()
                
    #==========================================================================
    def position_changed(self, ge, dim, indice) :
        #----------------------------------------------------------------------
        self.positions[(ge.index,dim)] = indice
        
        #----------------------------------------------------------------------
        ge.style.add_change('sync.is_active')
        ge.update_style() # -> update_plotted
        ge.graph.update_legend()
        ge.graph.rescale(ignore_autoscale=False, redraw=False)
        ge.graph.redraw()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Files_Tree(TreeWidget) :
    
    #==========================================================================
    def __init__(self, manager, page) :
        #----------------------------------------------------------------------
        self.manager = manager
        self.page = page
        self.positions = {} # [ge.index][dim] = indice
        
        #----------------------------------------------------------------------
        TreeWidget.__init__(self)
    
    #==========================================================================
    def _update_items(self) :
        #----------------------------------------------------------------------
        self.clear()
        if self.page.graphs is None : return
        
        #----------------------------------------------------------------------
        files = []
        
        #----------------------------------------------------------------------
        for graph in self.page.graphs :
            for ge in graph.graph_elements :
                file = ge.element.file
                if file in files : continue
                files.append(file)
        
        #----------------------------------------------------------------------
        for file in files :
            file_item = TreeWidgetItem(self, [file.name], icon=file.icon, expanded=True)
            
            #---- position ----------------------------------------------------
            dims = []
            active_dims = []
            for graph in self.page.graphs :
                for ge in graph.graph_elements :
                    for dim in ge.element.get_dimensions() :
                        if dim not in dims : dims.append(dim)
                        if dim not in graph.graph_config.dimensions : active_dims.append(dim)
            #------------------------------------------------------------------
            spins = []
            for dim in dims :
                N = file.get_dim_size(dim)
                if N is None : continue
                I = self.positions.get((file.index,dim),0)+1
                is_edge = file.is_dim_edge(dim)
                if is_edge : label = QLabel(dim+'='+' -> '.join(["{:.5G}".format(v) for v in file.get_dim_value(dim,I-1)]))
                else : label = QLabel(dim+'='+"{:.5G}".format(file.get_dim_value(dim,I-1)))
                
                spin = get_spin(I, 1, N, timer=True)
                spins.append(spin)
                dim_item = TreeWidgetItem(self, [file.name, dim], parent=file_item, main_widget=spin, icon=dim, widgets=[label], weights=[1])
                
                if is_edge : spin.valueChanged.connect(lambda I,file=file,dim=dim,label=label : label.setText(dim+"="+' -> '.join(["{:.5G}".format(v) for v in file.get_dim_value(dim,I-1)])))
                else : spin.valueChanged.connect(lambda I,file=file,dim=dim,label=label : label.setText(dim+'='+"{:.5G}".format(file.get_dim_value(dim,I-1))))
                
                spin.changed.connect(lambda I,file_index=file.index,dim=dim : self.position_changed(file_index, dim, I-1))
                dim_item.setDisabled(dim not in active_dims)
                
            #------------------------------------------------------------------
            if len(spins) > 0 :
                w = max([spin.sizeHint().width()+5 for spin in spins])
                for spin in spins : spin.setMinimumWidth(w)
            
    #==========================================================================
    def position_changed(self, file_index, dim, indice) :
        #----------------------------------------------------------------------
        self.positions[(file_index, dim)] = indice
        
        #----------------------------------------------------------------------
        for graph in self.page.graphs :
            for ge in graph.graph_elements :
                ge.element.load_axes()
                
                VI = ge.element.vect_indices
                
                if VI is not None and dim in VI.keys() :
                    _indice = VI[dim][indice]
                    etree = self.manager.etrees[self.page.index]
                    etree.position_changed(ge, dim, _indice)
                    e_spin = etree.pos_spins[(ge.index,dim)]
                    e_spin.setValue(_indice+1)
                    e_spin.emit_changed()
                else :
                    ge.style.add_change('sync.is_active')
                    ge.update_style() # -> update_plotted
            
            graph.update_legend()
            graph.rescale(ignore_autoscale=False, redraw=False)
            graph.redraw()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






