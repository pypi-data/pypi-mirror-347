# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import numpy as np
#------------------------------------------------------------------------------
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import cm
import matplotlib.colors as mcolors
import matplotlib.patches as patches
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPixmap, QIcon, QPainter, QPen
from PyQt5.QtWidgets import QDialog, QColorDialog
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Style_Dialog(QDialog) :
    
    #==========================================================================
    def __init__(self, engine, style={}, **kwargs) :
        #----------------------------------------------------------------------
        self.engine = engine
        self.skips = kwargs.pop('skips',[])
        self.style = style.copy()
        
        #----------------------------------------------------------------------
        self.preview_text = kwargs.pop('preview_text','Azerty 1234 !')
        
        #----------------------------------------------------------------------
        QDialog.__init__(self)
        
        #----------------------------------------------------------------------
        self.fonts = {}
        self.fonts['qt'] = QFontDatabase().families()
        self.fonts['MPL'] = sorted(set([f.name for f in fm.fontManager.ttflist]))
        self.fonts['VTK'] = ['Arial','Courier','Times']
        
        #----------------------------------------------------------------------
        self._line_styles = ['Trait plein', 'Tirets', 'Pointillés', 'Tirets-Pointillés']
        self.line_styles  = ['-'          , '--'    , ':'         , '-.'               ]
        
        #----------------------------------------------------------------------
        self._mark_shapes = ['cercle','croix','croix2','carré','carré2','losange','étoile','triangle bas','triangle haut','triangle droite','triangle gauche']
        self.mark_shapes  = ['o'     ,'x'    ,'+'     ,'s'    ,'D'     ,'d'      ,'s'     ,'v'           ,'^'            ,'>'              ,'<'              ]
        
        self.fill_palettes = sorted(plt.colormaps())
        
        #----------------------------------------------------------------------
        self.color_names = {}
        self.color_names['qt'] = {}
        self.color_names['MPL'] = {hexa.lower():name for name,hexa in mcolors.CSS4_COLORS.items()}
        self.color_names['VTK'] = self.color_names['MPL']
        
        #----------------------------------------------------------------------
        self.load_ui()
        
    #==========================================================================
    def load_ui(self) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Style_Dialog.ui"), self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        #----------------------------------------------------------------------
        self.types = []
        if self.load_font() : self.types.append('font')
        if self.load_line() : self.types.append('line')
        if self.load_mark() : self.types.append('mark')
        if self.load_fill() : self.types.append('fill')
        
        #----------------------------------------------------------------------
        self.lb_font_preview.setText(self.preview_text)
        self.bt_valid.clicked.connect(self.on_valid)
        self.bt_cancel.clicked.connect(self.close)
        
        #----------------------------------------------------------------------
        self.resize(500,30)
        self.show()
        
        #----------------------------------------------------------------------
        self.update_font_preview()
        self.update_line_preview()
        self.update_mark_preview()
        self.update_fill_preview()
        
        self.gridLayout.setColumnStretch(0,1)
        self.gridLayout.setColumnStretch(1,0)
        
    #==========================================================================
    
    
    #==========================================================================
    #---- *** FONT ***
    #==========================================================================
    def load_font(self) :
        #----------------------------------------------------------------------
        kws = list(self.style.keys())
        
        #----------------------------------------------------------------------
        is_font = len([k for k in ['font_name','font_size','font_color','font_bold','font_italic'] if k in kws]) > 0
        self.gp_font.setVisible(is_font)
        self.gp_font_preview.setVisible(is_font)
        if not is_font : return False
        
        #----------------------------------------------------------------------
        if 'font_name' in kws :
            self.co_font_name.addItems(self.fonts[self.engine])
            self.co_font_name.currentTextChanged.connect(self.update_font_preview)
            self.co_font_name.setCurrentText(self.style.get('font_name','Arial'))
        else :
            self.lab_font_name.setEnabled(False)
            self.co_font_name.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'font_size' in kws :
            self.sp_font_size.setValue(self.style.get('font_size',12))
            self.sp_font_size.valueChanged.connect(self.update_font_preview)
            if self.engine == 'VTK' : self.sp_font_size.setDecimals(0)
        else :
            self.lab_font_size.setEnabled(False)
            self.sp_font_size.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'font_color' in kws :
            self.le_font_color.setText(self.style.get('font_color','black'))
            self.le_font_color.textChanged.connect(lambda t,le=self.le_font_color : le.setStyleSheet("color:{};".format('black' if self.get_color(le) is not None else 'red')))
            self.le_font_color.textChanged.connect(self.update_font_preview)
            self.bt_font_color.clicked.connect(lambda e,le=self.le_font_color : self.select_color(le))
        else :
            self.lab_font_color.setEnabled(False)
            self.le_font_color.setEnabled(False)
            self.bt_font_color.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'font_bold' in kws :
            self.cb_font_bold.setChecked(self.style.get('font_bold',False))
            self.cb_font_bold.clicked.connect(self.update_font_preview)
        else :
            self.cb_font_bold.setEnabled(False)
        #----------------------------------------------------------------------
        if 'font_italic' in kws :
            self.cb_font_italic.setChecked(self.style.get('font_italic',False))
            self.cb_font_italic.clicked.connect(self.update_font_preview)
        else :
            self.cb_font_bold.setEnabled(False)
        #----------------------------------------------------------------------
        if 'font_bold' not in kws and 'font_italic' not in kws :
            self.lab_font_style.setEnabled(False)
            self.lay_font_style.setEnabled(False)
        
        #----------------------------------------------------------------------
        return True
        
    #==========================================================================
    def update_font_preview(self) :
        #----------------------------------------------------------------------
        if not self.isVisible() : return
        if 'font' not in self.types : return
        
        #----------------------------------------------------------------------
        font = QFont()
        font.setFamily(self.co_font_name.currentText())
        font.setPointSizeF(self.sp_font_size.value())
        font.setBold(self.cb_font_bold.isChecked())
        font.setItalic(self.cb_font_italic.isChecked())
        
        #----------------------------------------------------------------------
        color = self.get_color(self.le_font_color)
        if color is None : color = QColor('black')
        self.lb_font_preview.setFont(font)
        self.lb_font_preview.setStyleSheet("color:{};".format(color.name()))
    
    #==========================================================================
    
    
    #==========================================================================
    #---- *** LINE ***
    #==========================================================================
    def load_line(self) :
        #----------------------------------------------------------------------
        kws = list(self.style.keys())
        
        #----------------------------------------------------------------------
        is_line = len([k for k in ['line_style','line_width','line_color','line_alpha'] if k in kws]) > 0
        self.gp_line.setVisible(is_line)
        self.gp_line_preview.setVisible(is_line)
        if not is_line : return False
        
        #----------------------------------------------------------------------
        fig = Figure(facecolor='#f0f0f0', tight_layout=(0,0,1,1))
        self.line_canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor('#f0f0f0')
        ax.axis('off')
        self.line_plot = ax.plot([0,1,2],[0,0,0])[0]
        self.layout_line_preview.addWidget(self.line_canvas)
        self.line_canvas.setMaximumWidth(200)
        
        #----------------------------------------------------------------------
        if 'line_style' in kws :
            self.co_line_style.clear()
            self.co_line_style.addItems(self._line_styles)
            self.co_line_style.setCurrentIndex(self.line_styles.index(self.style.get('line_style','-')))
            self.co_line_style.currentTextChanged.connect(self.update_line_preview)
        if 'line_style' not in kws or self.engine == 'VTK' :
            self.lab_line_style.setEnabled(False)
            self.co_line_style.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'line_width' in kws :
            self.sp_line_width.setValue(self.style.get('line_width',1))
            self.sp_line_width.valueChanged.connect(self.update_line_preview)
        else :
            self.lab_line_width.setEnabled(False)
            self.sp_line_width.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'line_color' in kws :
            self.le_line_color.setText(self.style.get('line_color','black'))
            self.le_line_color.setPlaceholderText('auto')
            self.le_line_color.textChanged.connect(lambda t,le=self.le_line_color : le.setStyleSheet("color:{};".format('black' if self.get_color(le, allow_auto=True) is not None else 'red')))     
            self.le_line_color.textChanged.connect(self.update_line_preview)
            self.bt_line_color.clicked.connect(lambda e,le=self.le_line_color : self.select_color(le))
        else :
            self.lab_line_color.setEnabled(False)
            self.le_line_color.setEnabled(False)
            self.bt_line_color.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'line_alpha' in kws :
            M = self.sl_line_alpha.maximum()
            self.sl_line_alpha.valueChanged.connect(lambda v,M=M : self.lb_line_alpha.setText('{:.0f}%'.format(v*100/M)))
            self.sl_line_alpha.setValue(int(self.style.get('line_alpha',1.0)*M))
            self.sl_line_alpha.valueChanged.connect(self.update_line_preview)
        else :
            self.lab_line_alpha.setEnabled(False)
            self.sl_line_alpha.setEnabled(False)
            self.lb_line_alpha.setEnabled(False)
            
        #----------------------------------------------------------------------
        return True
            
    #==========================================================================
    def update_line_preview(self) :
        #----------------------------------------------------------------------
        if not self.isVisible() : return
        if 'line' not in self.types : return
        
        #----------------------------------------------------------------------
        line_style = self.line_styles[self.co_line_style.currentIndex()]
        line_width = self.sp_line_width.value()
        line_color = self.get_color(self.le_line_color, engine='MPL')
        line_alpha = self.sl_line_alpha.value()/self.sl_line_alpha.maximum()
        
        #----------------------------------------------------------------------
        self.line_plot.set_linestyle(line_style)
        self.line_plot.set_linewidth(line_width)
        self.line_plot.set_color(line_color)
        self.line_plot.set_alpha(line_alpha)
        
        #----------------------------------------------------------------------
        self.line_canvas.draw()
    
    #==========================================================================
    
    
    #==========================================================================
    #---- *** MARK ***
    #==========================================================================
    def load_mark(self) :
        #----------------------------------------------------------------------
        kws = list(self.style.keys())
                    
        #----------------------------------------------------------------------
        is_mark = len([k for k in ['mark_shape','mark_size','mark_edge_width','mark_edge_color','mark_face_color','mark_alpha'] if k in kws]) > 0
        self.gp_mark.setVisible(is_mark)
        self.gp_mark_preview.setVisible(is_mark)
        if not is_mark : return False
        
        #----------------------------------------------------------------------
        fig = Figure(facecolor='#f0f0f0', tight_layout=(0,0,1,1))
        self.mark_canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor('#f0f0f0')
        ax.axis('off')
        self.mark_plot = ax.plot([0,1,2],[0,0,0], ls='none')[0]
        ax.set_xlim([-0.5,2.5])
        self.layout_mark_preview.addWidget(self.mark_canvas)
        self.mark_canvas.setMaximumWidth(200)
    
        #----------------------------------------------------------------------
        if 'mark_shape' in kws :
            self.co_mark_shape.clear()
            self.co_mark_shape.addItems(self._mark_shapes)
            self.co_mark_shape.setCurrentIndex(self.mark_shapes.index(self.style.get('mark_shape','o')))
            self.co_mark_shape.currentTextChanged.connect(self.update_mark_preview)
        else :
            self.lab_mark_shape.setEnabled(False)
            self.co_mark_shape.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'mark_size' in kws :
            self.sp_mark_size.setValue(self.style.get('mark_size',5))
            self.sp_mark_size.valueChanged.connect(self.update_mark_preview)
        else :
            self.lab_mark_size.setEnabled(False)
            self.sp_mark_size.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'mark_edge_width' in kws :
            self.sp_mark_edge_width.setValue(self.style.get('mark_edge_width',5))
            self.sp_mark_edge_width.valueChanged.connect(self.update_mark_preview)
        else :
            self.lab_mark_edge_width.setEnabled(False)
            self.sp_mark_edge_width.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'mark_edge_color' in kws :
            self.le_mark_edge_color.setText(self.style.get('mark_edge_color','black'))
            self.le_mark_edge_color.setPlaceholderText('auto')
            self.le_mark_edge_color.textChanged.connect(lambda t,le=self.le_mark_edge_color : le.setStyleSheet("color:{};".format('black' if self.get_color(le, allow_auto=True) is not None else 'red')))     
            self.le_mark_edge_color.textChanged.connect(self.update_mark_preview)
            self.bt_mark_edge_color.clicked.connect(lambda e,le=self.le_mark_edge_color : self.select_color(le))
        else :
            self.lab_mark_edge_color.setEnabled(False)
            self.le_mark_edge_color.setEnabled(False)
            self.bt_mark_edge_color.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'mark_face_color' in kws :
            self.le_mark_face_color.setText(self.style.get('mark_face_color','black'))
            self.le_mark_face_color.setPlaceholderText('auto')
            self.le_mark_face_color.textChanged.connect(lambda t,le=self.le_mark_face_color : le.setStyleSheet("color:{};".format('black' if self.get_color(le, allow_auto=True) is not None else 'red')))     
            self.le_mark_face_color.textChanged.connect(self.update_mark_preview)
            self.bt_mark_face_color.clicked.connect(lambda e,le=self.le_mark_face_color : self.select_color(le))
        else :
            self.lab_mark_face_color.setEnabled(False)
            self.le_mark_face_color.setEnabled(False)
            self.bt_mark_face_color.setEnabled(False)
            
        #----------------------------------------------------------------------
        M = self.sl_mark_alpha.maximum()
        self.sl_mark_alpha.setValue(int(self.style.get('mark_alpha',1.0)*M))
        if 'mark_alpha' in kws and 'mark_alpha' not in self.skips :
            self.sl_mark_alpha.valueChanged.connect(lambda v,M=M : self.lb_mark_alpha.setText('{:.0f}%'.format(v*100/M)))
            self.sl_mark_alpha.valueChanged.connect(self.update_mark_preview)
        else :
            self.lab_mark_alpha.setEnabled(False)
            self.sl_mark_alpha.setEnabled(False)
            self.lb_mark_alpha.setEnabled(False)
            
        #----------------------------------------------------------------------
        return True
        
    #==========================================================================
    def update_mark_preview(self) :
        #----------------------------------------------------------------------
        if not self.isVisible() : return
        if 'mark' not in self.types : return
        
        #----------------------------------------------------------------------
        mark_shape      = self.mark_shapes[self.co_mark_shape.currentIndex()]
        mark_size       = self.sp_mark_size.value()
        mark_edge_width = self.sp_mark_edge_width.value()
        mark_edge_color = self.get_color(self.le_mark_edge_color, engine='MPL')
        mark_face_color = self.get_color(self.le_mark_face_color, engine='MPL')
        mark_alpha      = self.sl_mark_alpha.value()/self.sl_mark_alpha.maximum()
            
        self.mark_plot.set_marker(mark_shape)
        self.mark_plot.set_markersize(mark_size)
        self.mark_plot.set_markeredgewidth(mark_edge_width)
        self.mark_plot.set_markeredgecolor(mark_edge_color)
        self.mark_plot.set_markerfacecolor(mark_face_color)
        self.mark_plot.set_alpha(mark_alpha)
        
        #----------------------------------------------------------------------
        self.mark_canvas.draw()
        
    #==========================================================================
    
    
    #==========================================================================
    #---- *** FILL ***
    #==========================================================================
    def load_fill(self) :
        #----------------------------------------------------------------------
        kws = list(self.style.keys())
        
        #----------------------------------------------------------------------
        is_fill = len([k for k in ['fill_color','fill_alpha'] if k in kws]) > 0
        self.gp_fill.setVisible(is_fill)
        self.gp_fill_preview.setVisible(is_fill)
        if not is_fill : return False
        
        #----------------------------------------------------------------------
        fig = Figure(facecolor='#f0f0f0', tight_layout=(0,0,1,1))
        self.fill_canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor('#f0f0f0')
        ax.axis('off')
        self.fill_plot = patches.Rectangle((0, 0), 1, 1, ls='-', edgecolor='black')
        ax.add_patch(self.fill_plot)
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.layout_fill_preview.addWidget(self.fill_canvas)
        self.fill_canvas.setMaximumWidth(200)
            
        #----------------------------------------------------------------------
        if 'fill_palette' in kws :
            self.co_fill_palette.clear()
            
            for cmap_name in self.fill_palettes :
                cmap = cm.get_cmap(cmap_name)
                pixmap = QPixmap(20,20)
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                pen = QPen()
                pen.setWidth(1)
                for i in range(20+1) :
                    pen.setColor(QColor.fromRgbF(*cmap(i/20.0)))
                    painter.setPen(pen)
                    painter.drawLine(i, 5, i, 15)
                painter.end()
                self.co_fill_palette.addItem(QIcon(pixmap), cmap_name)
            
            self.co_fill_palette.setCurrentIndex(self.fill_palettes.index(self.style.get('fill_palette','gist_rainbow')))
            self.co_fill_palette.currentTextChanged.connect(self.update_fill_preview)
            
        else :
            self.lab_fill_palette.setEnabled(False)
            self.co_fill_palette.setEnabled(False)
        
        #----------------------------------------------------------------------
        if 'fill_color' in kws :
            self.le_fill_color.setText(self.style.get('fill_color','auto'))
            self.le_fill_color.setPlaceholderText('auto')
            self.le_fill_color.textChanged.connect(lambda t,le=self.le_fill_color : le.setStyleSheet("color:{};".format('black' if self.get_color(le, allow_auto=True) is not None else 'red')))     
            self.le_fill_color.textChanged.connect(self.update_fill_preview)
            self.bt_fill_color.clicked.connect(lambda e,le=self.le_fill_color : self.select_color(le))
        else :
            self.lab_fill_color.setEnabled(False)
            self.le_fill_color.setEnabled(False)
            self.bt_fill_color.setEnabled(False)
            
        #----------------------------------------------------------------------
        if 'fill_alpha' in kws :
            M = self.sl_fill_alpha.maximum()
            self.sl_fill_alpha.valueChanged.connect(lambda v,M=M : self.lb_fill_alpha.setText('{:.0f}%'.format(v*100/M)))
            self.sl_fill_alpha.setValue(int(self.style.get('fill_alpha',1.0)*M))
            self.sl_fill_alpha.valueChanged.connect(self.update_fill_preview)
        else :
            self.lab_fill_alpha.setEnabled(False)
            self.sl_fill_alpha.setEnabled(False)
            self.lb_fill_alpha.setEnabled(False)
            
        #----------------------------------------------------------------------
        return True
            
    #==========================================================================
    def update_fill_preview(self) :
        #----------------------------------------------------------------------
        if not self.isVisible() : return
        if 'fill' not in self.types : return
        
        kws = list(self.style.keys())
        
        #----------------------------------------------------------------------
        if 'fill_palette' in kws :
            cmap = plt.get_cmap(self.co_fill_palette.currentText())  # Vous pouvez choisir n'importe quelle colormap
            norm = plt.Normalize(0, 1)
            gradient = np.linspace(0, 1, 256).reshape(1, 256)
            gradient_image = cmap(np.vstack((gradient, gradient)))
            self.fill_plot.set_facecolor('none')
            self.fill_plot.axes.imshow(gradient_image, extent=[0, 1.0, 0, 1.0], aspect='auto', cmap=cmap, norm=norm)

        #----------------------------------------------------------------------
        elif 'fill_color' in kws :
            fill_color = self.get_color(self.le_fill_color, engine='MPL')
            self.fill_plot.set_facecolor(fill_color)
        
        #----------------------------------------------------------------------
        fill_alpha = self.sl_fill_alpha.value()/self.sl_fill_alpha.maximum()
        self.fill_plot.set_alpha(fill_alpha)
        
        #----------------------------------------------------------------------
        self.fill_canvas.draw()
    
    #==========================================================================
    
    
    #==========================================================================
    #---- *** COLORS ***
    #==========================================================================
    def get_color(self, le, engine=None, default='black', allow_auto=False) :
        #----------------------------------------------------------------------
        name = le.text()
        if allow_auto :
            if name == 'auto' : return name
            elif name == '' : return le.placeholderText()            
        
        #----------------------------------------------------------------------
        qcolor = QColor(name)
        valid = qcolor.isValid()
        #----------------------------------------------------------------------
        if valid :
            if engine is None : return qcolor
            else : return self.color_names[engine].get(qcolor.name(),qcolor.name())
        #----------------------------------------------------------------------
        else :
            if engine is None : return None
            else              : return default
        
    #==========================================================================
    def select_color(self, le) :
        #----------------------------------------------------------------------
        color = self.get_color(le)
        #----------------------------------------------------------------------
        if color is not None : color = QColorDialog.getColor(color)
        else : color = QColorDialog.getColor()
        #----------------------------------------------------------------------
        if color.isValid() :
            new_name = color.name()
            new_name = self.color_names[self.engine].get(new_name,new_name)
            le.setText(new_name)
    
    #==========================================================================
    def on_color_changed(self, le) :
        #----------------------------------------------------------------------
        color = self.get_color(le, allow_auto=True)
        le.setStyleSheet("color:{};".format('black' if color is not None else 'red'))
    
    #==========================================================================
    
    
    #==========================================================================
    #---- *** VALID ***
    #==========================================================================
    def on_valid(self) :
        #----------------------------------------------------------------------
        kws = list(self.style.keys())
        self.style = {}
        
        #----------------------------------------------------------------------
        if 'font_name'   in kws : self.style['font_name']   = self.co_font_name.currentText()
        if 'font_size'   in kws : self.style['font_size']   = self.sp_font_size.value()
        if 'font_color'  in kws : self.style['font_color']  = self.get_color(self.le_font_color, self.engine, allow_auto=True)
        if 'font_bold'   in kws : self.style['font_bold']   = self.cb_font_bold.isChecked()
        if 'font_italic' in kws : self.style['font_italic'] = self.cb_font_italic.isChecked()
        
        #----------------------------------------------------------------------
        if 'line_style'  in kws : self.style['line_style']  = self.line_styles[self.co_line_style.currentIndex()]
        if 'line_width'  in kws : self.style['line_width']  = self.sp_line_width.value()
        if 'line_color'  in kws : self.style['line_color']  = self.get_color(self.le_line_color, self.engine, allow_auto=True)
        if 'line_alpha'  in kws : self.style['line_alpha']  = self.sl_line_alpha.value()/self.sl_line_alpha.maximum()
        
        #----------------------------------------------------------------------
        if 'mark_shape'      in kws : self.style['mark_shape']      = self.mark_shapes[self.co_mark_shape.currentIndex()]
        if 'mark_size'       in kws : self.style['mark_size']       = self.sp_mark_size.value()
        if 'mark_edge_width' in kws : self.style['mark_edge_width'] = self.sp_mark_edge_width.value()
        if 'mark_edge_color' in kws : self.style['mark_edge_color'] = self.get_color(self.le_mark_edge_color, self.engine, allow_auto=True)
        if 'mark_face_color' in kws : self.style['mark_face_color'] = self.get_color(self.le_mark_face_color, self.engine, allow_auto=True)
        if 'mark_alpha'      in kws : self.style['mark_alpha']      = self.sl_mark_alpha.value()/self.sl_mark_alpha.maximum()
        
        #----------------------------------------------------------------------
        if 'fill_palette' in kws : self.style['fill_palette'] = self.co_fill_palette.currentText()
        if 'fill_color'   in kws : self.style['fill_color']   = self.get_color(self.le_fill_color, self.engine, allow_auto=True)
        if 'fill_alpha'   in kws : self.style['fill_alpha']   = self.sl_fill_alpha.value()/self.sl_fill_alpha.maximum()
        
        #----------------------------------------------------------------------
        self.close()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
