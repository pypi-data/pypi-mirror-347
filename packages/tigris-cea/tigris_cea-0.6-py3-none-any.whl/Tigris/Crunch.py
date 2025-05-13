# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
import numpy as np
import random
from itertools import product
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
import matplotlib as mpl
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Vector, Mesh
from Element_Matrix import Matrix
from Element_Cuboids import Cuboid
from Calcul import Calcul, Calcul_Convertor
from utils import get_now
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tofloat(s, default=None) :
    #--------------------------------------------------------------------------
    try : return float(s)
    except : pass
    
    #--------------------------------------------------------------------------
    if '-' in s and len(s.split('-')[1]) == 3 :
        i = s.index('-')
        s = s[:i]+'E'+s[i:]
        return tofloat(s)
    
    #--------------------------------------------------------------------------
    return default
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Crunch(Calcul) :
    
    #==========================================================================
    CODE      = 'crunch'
    #--------------------------------------------------------------------------
    ATTR_INPUTPATH = 'INPUT_PATH'
    #--------------------------------------------------------------------------
    STATIAL_OUTPUTS = ["area","conc","gas","gases","mineralpercent","molmineral","pH","porosity","rate","saturation","tortuosity","totcon","TotMineral","totmineral","velocity","volume","weightpercent"]
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        Calcul.__init__(self, Crunch.CODE)
        
        #----------------------------------------------------------------------
        self.zones   = None
        self.results = None
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - zones".ljust(Element.DETAILS_ALIGN,' ')+": {} matériaux".format(len(self.zones.keys())))
        print("   - résultats".ljust(Element.DETAILS_ALIGN,' ')+": {} variables".format(len(self.results)))
        
    #==========================================================================
    def _load(self) :
        #----------------------------------------------------------------------
        self.zones  = {}
        self.results = []
        
        #----------------------------------------------------------------------
        for e in self.elements :
            if   e.path[0] == Calcul.ZONES_NAME   : self.zones[e.label] = e
            elif e.path[0] == Calcul.RESULTS_NAME : self.results.append(e)
        
        #----------------------------------------------------------------------
        for zlabel,zone in self.zones.items() :
            zone.configure(value=zone.get_attribute('zone_index'))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Crunch_Convertor(Calcul_Convertor) :

    #==========================================================================
    def __init__(self, **opts) :
        #----------------------------------------------------------------------
        Calcul_Convertor.__init__(self, **opts)
        
        #----------------------------------------------------------------------
        self.zones   = None
        self.results = None
        
        #----------------------------------------------------------------------
        self.convert(**opts)
        
    #==========================================================================
    def _convert(self, **opts) :
        """
        input_path, name
        [nc_path]
        """
        
        #----------------------------------------------------------------------
        print("> Conversion d'un calcul {} :".format(Calcul.CODE_NAMES[Crunch.CODE]))
        
        #----------------------------------------------------------------------
        if 'input_path' not in opts.keys() :
            raise Exception("paramètre 'input_path' manquant")
        
        #----------------------------------------------------------------------
        self.input_path = opts.get('input_path')
        self.name = opts.get('name', os.path.basename(".".join(self.input_path.split(".")[:-1])))
        self.dirpath = os.path.dirname(self.input_path)
        #----------------------------------------------------------------------
        kwargs = {}
        kwargs[Calcul.ATTR_CODE]      = Crunch.CODE
        kwargs[Calcul.ATTR_CALCUL]    = self.name
        kwargs[Calcul.ATTR_POSTDATE]  = get_now(fmt='%d/%m/%Y %H:%M')
        kwargs[Calcul.ATTR_DIRPATH]   = self.dirpath
        #----------------------------------------------------------------------
        kwargs[Crunch.ATTR_INPUTPATH] = self.input_path
        #----------------------------------------------------------------------
        self.config = Element(path=[Calcul.CONFIG_NAME], label='config', **kwargs)
        
        #----------------------------------------------------------------------
        self.read_input()
        self.configure_grid()
        self.configure_zones()
        self.configure_results()
        
    #==========================================================================
    def read_input(self) :
        #----------------------------------------------------------------------
        print("   - lecture des fichiers d'entrée ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        self.input_lines = None
        
        #----------------------------------------------------------------------
        if not os.path.exists(self.input_path) :
            raise Exception("fichier '{}' introuvable".format(os.path.basename(self.input_path)))
            
        #----------------------------------------------------------------------
        self.input_lines = {}
        self.input_lines['raw'] = [] # lignes brutes
        self.input_lines['origin'] = [] # fichier et ligne
        self.input_lines['key_word'] = [] # mot clé
        
        #----------------------------------------------------------------------
        inname = os.path.basename(self.input_path)
        file = open(self.input_path, 'r')
        kw = None
        #----------------------------------------------------------------------
        for l,line in enumerate(file) :
            #------------------------------------------------------------------
            line = line.strip()
                
            #------------------------------------------------------------------
            if line == "" : continue
            if line[0] == "!" : continue
            
            #------------------------------------------------------------------
            if   line == 'END'                : kw = None ; continue
            elif line == 'OUTPUT'             : kw = 'output' ; continue
            elif line == 'DISCRETIZATION'     : kw = 'grid' ; continue
            elif line == 'INITIAL_CONDITIONS' : kw = 'zones' ; continue
            
            #------------------------------------------------------------------
            self.input_lines['raw'].append(line)
            self.input_lines['origin'].append((inname, l+1))
            self.input_lines['key_word'].append(kw)
            
        #----------------------------------------------------------------------
        print('OK ({} lignes)'.format(len(self.input_lines['raw'])))
        
    #==========================================================================
    def configure_grid(self) :
        #----------------------------------------------------------------------
        print("   - préparation du maillage ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'grid']
        
        #----------------------------------------------------------------------
        edges = {dim:[0.0,1.0] for dim in ['X','Y','Z']}
        for l,line in input_llines :
            fields = line.split()
            if   fields[0] == 'xzones' : dim = 'X'
            elif fields[0] == 'yzones' : dim = 'Y'
            elif fields[0] == 'zzones' : dim = 'Z'
            else :
                raise Exception("le champ '{}' n'est pas interprété".format(fields[0]))
            
            #------------------------------------------------------------------
            edges[dim] = [0.0]
            for i in range(1, len(fields), 2) :
                N = int(fields[i])
                dx = float(fields[i+1])
                for n in range(N) : edges[dim].append(round(edges[dim][-1]+dx,5))
                
        #----------------------------------------------------------------------
        Ns = []
        for dim in ['X','Y','Z'] :
            self.meshs[dim] = Mesh(path=[Calcul.COORD_NAME, dim],
                                   dimension=dim,
                                   edges=edges[dim])
            Ns.append(len(edges[dim])-1)
            
        #----------------------------------------------------------------------
        print('OK')
        print("      - maillage  : {} x {} x {} = {} mailles".format(*Ns, np.prod(Ns)))
        
    #==========================================================================
    def configure_zones(self) :
        #----------------------------------------------------------------------
        print("   - préparation des matériaux ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        self.zones = {}
        
        #----------------------------------------------------------------------
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        zi = 0
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'zones']
        for l,line in input_llines :
            fields = line.split()
            
            name = fields[0]
            indices = []
            for field in fields[1:] :
                if '-' not in field : continue
                indices += [int(i)-1 for i in field.split("-")]
            
            indices += [0] * (len(self.meshs.keys())*2-len(indices))
            
            i0,i1,j0,j1,k0,k1 = indices
            
            x0 = self.meshs['X'].edges[i0]
            x1 = self.meshs['X'].edges[i1+1]
            y0 = self.meshs['Y'].edges[j0]
            y1 = self.meshs['Y'].edges[j1+1]
            z0 = self.meshs['Z'].edges[k0]
            z1 = self.meshs['Z'].edges[k1+1]
            
            NX,NY,NZ = self.meshs['X'].N, self.meshs['Y'].N, self.meshs['Z'].N
            
            si  = [name for name,i in [('i0',i0),('j0',j0),('k0',k0)] if i < 0]
            si += [name for name,i,m in [('i1',i1,NX),('j1',j1,NY),('k1',k1,NZ)] if i > m-1]
            if len(si) > 0 :
                raise Exception("fichier {}, ligne {} : indice{plu} {li} invalide{plu}".format(*self.input_lines['origin'][l], plu='s' if len(si) > 1 else '', li=','.join(si)))
                
            #------------------------------------------------------------------
            self.zones[name] = Cuboid(path        = [Calcul.ZONES_NAME,name],
                                      dimensions  = ['X','Y','Z'],
                                      coordinates = (x0,x1,y0,y1,z0,z1),
                                      indices     = (i0,i1,j0,j1,k0,k1),
                                      axes_paths  = axes_paths,
                                      zone_index  = zi+1)
            zi += 1
            
        #----------------------------------------------------------------------
        cmap = mpl.colormaps['gist_rainbow']
        norm = mpl.colors.Normalize(vmin=0, vmax=len(self.zones.keys())-1)
        colors = [mpl.colors.rgb2hex(cmap(norm(zone.get_attribute('zone_index')-1))) for zone in self.zones.values()]
        random.seed(25072020)
        #----------------------------------------------------------------------
        for zone in self.zones.values() :
            zone.set_style(edge_color = 'black',
                           edge_width = 0.5,
                           face_color = colors[zone.get_attribute('zone_index')-1],
                           line_width = 1.0,
                           line_color = colors[zone.get_attribute('zone_index')-1],
                           )
            
        #----------------------------------------------------------------------
        print("OK")
    
    #==========================================================================
    def configure_results(self) :
        #----------------------------------------------------------------------
        print("   - préparation des fichiers de sortie :")
        self.results = []
        
        self.configure_results_speciations()
        self.configure_results_spatials()
        
    #==========================================================================
    def configure_results_speciations(self) :
        #----------------------------------------------------------------------
        print("      - fichiers 'speciation' ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        _fnames = {}
        for fname in os.listdir(os.path.dirname(self.input_path)) :
            if not fname.startswith('speciation') : continue
            if not fname.endswith('.out') : continue
            findex = int(fname.replace('speciation','').replace('.out',''))
            _fnames[findex] = fname
        fnames = [fname for i,fname in sorted(_fnames.items(), key=lambda e:e[0])]
        
        #----------------------------------------------------------------------
        steps = []
        steps.append('General')
        steps.append('Primary Concentrations')
        steps.append('Concentrations_1')
        steps.append('Concentrations_2')
        steps.append('Partial pressure')
        steps.append('Saturation state')
        
        #----------------------------------------------------------------------
        times = []
        data = {}
        data_fields = {step:[] for step in range(len(steps))} # [step] = [key]
        
        #----------------------------------------------------------------------
        for t,fname in enumerate(fnames) :
            path = os.path.join(os.path.dirname(self.input_path), fname)
            
            file = open(path, 'r')
            step = None
            l = -1
            for line in file :
                l += 1
                line = line.strip()
            
                if l == 0 :
                    time = float(line.strip().split()[-1])
                    times.append(time)
                    continue
                
                #--------------------------------------------------------------
                if line == '' : continue
                
                #--------------------------------------------------------------
                if line.startswith('------> GRID LOCATION:') :
                    fields = line.split(':')
                    i = int(fields[1].strip())-1
                    j = int(fields[2].strip())-1
                    k = int(fields[3].strip())-1
                    step = 0
                    
                    if (i,j,k,t) not in data.keys() :
                        data[(i,j,k,t)] = {i:{} for i in range(len(steps))}
                        
                    continue
                #--------------------------------------------------------------
                elif line == "Total Aqueous Concentrations of Primary Species" :
                    step = 1
                    for skip in range(3) : file.readline() ; l += 1
                    continue
                #--------------------------------------------------------------
                elif line == "Concentrations of Individual Species, Exchangers, and Surface Complexes" :
                    for skip in range(2) : file.readline() ; l += 1
                    line = file.readline().strip() ; l += 1
                    if "Concentration" in line : step = 2
                    else : step = 3
                    file.readline() ; l += 1
                    continue
                #--------------------------------------------------------------
                elif line == "****** Partial pressure of gases (bars) *****" :
                    step = 4
                    continue
                #--------------------------------------------------------------
                elif line == "***** Saturation state of minerals (log[Q/K] *****" :
                    step = 5
                    continue
                #--------------------------------------------------------------
                elif line == '**************************************************************' :
                    step = None
                    continue
                
                #--------------------------------------------------------------
                if step == 2 and "Log" in line :
                    step = 3
                    file.readline() ; l += 1
                    continue
                
                #--------------------------------------------------------------
                if step is None : continue
                
                #--------------------------------------------------------------
                if step == 0 : fields = [f.strip() for f in line.split('=')]
                else : fields = [f.strip() for f in line.split()]
                
                key = fields[0]
                if   step in [0,1,4,5] : values = [tofloat(fields[1])]
                elif step in [2,3]     : values = [tofloat(field) for field in fields[1:6]]
                
                if key not in data_fields[step] : data_fields[step].append(key)
                data[(i,j,k,t)][step][key] = values
        
            file.close()
            
        #----------------------------------------------------------------------
        self.vects['T'] = Vector(path=[Calcul.COORD_NAME,'T'],
                                 dimension='T',
                                 values=times)
        
        #----------------------------------------------------------------------
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        axes_paths['T'] = self.vects['T'].path
        
        #----------------------------------------------------------------------
        NX = self.meshs['X'].N
        NY = self.meshs['Y'].N
        NZ = self.meshs['Z'].N
        NT = self.vects['T'].N
        
        NV = 0
        #----------------------------------------------------------------------
        for step in range(len(steps)) :
            fields = data_fields[step]
            NF = len(fields)
            NV += NF
            
            M = np.full((NX,NY,NZ,NT,NF), np.nan)
            
            #------------------------------------------------------------------
            if step in [2,3] :
                if step == 2 : columns = ['Log_Molality','Log_Activity','Molality','Concentration','Activity']
                else         : columns = ['Log_Molality','Log_Activity','Molality','Activity','Activity_Coef']
                
                for c,column in enumerate(columns) :
                    
                    for i,j,k,t in data.keys() :
                        for f,field in enumerate(data[i,j,k,t][step].keys()) :
                            M[i,j,k,t,f] = data[i,j,k,t][step][field][c]
                            
                    path = [Calcul.RESULTS_NAME, "Speciation", steps[step], column]
                    matrix = Matrix(path       = path,
                                    label      = column,
                                    dimensions = ['X','Y','Z','T',Matrix.FIELDS_NAME],
                                    axes_paths = axes_paths,
                                    fields     = fields,
                                    M          = M,
                                    )
                    self.results.append(matrix)
                
            #------------------------------------------------------------------
            else :
                for i,j,k,t in data.keys() :
                    for f,field in enumerate(data[i,j,k,t][step].keys()) :
                        M[i,j,k,t,f] = data[i,j,k,t][step][field][0]
                        
                path = [Calcul.RESULTS_NAME, "Speciation", steps[step]]
                matrix = Matrix(path       = path,
                                label      = steps[step],
                                dimensions = ['X','Y','Z','T',Matrix.FIELDS_NAME],
                                axes_paths = axes_paths,
                                fields     = fields,
                                M          = M,
                                )
                self.results.append(matrix)
    
        #----------------------------------------------------------------------
        print("OK ({} fichiers, {} variables)".format(NT,NV))
        
    #==========================================================================
    def configure_results_spatials(self) :
        #----------------------------------------------------------------------
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        axes_paths['T'] = self.vects['T'].path
        
        NX = self.meshs['X'].N
        NY = self.meshs['Y'].N
        NZ = self.meshs['Z'].N
        NT = self.vects['T'].N
        
        NM = NX*NY*NZ
            
        #----------------------------------------------------------------------
        for out in Crunch.STATIAL_OUTPUTS :
            print("      - fichiers '{}' ... ".format(out), end="", flush=True)
            
            #------------------------------------------------------------------
            _fnames = {}
            for fname in os.listdir(os.path.dirname(self.input_path)) :
                if not fname.startswith(out) : continue
                if not fname.endswith('.out') : continue
                index_str = fname.replace(out,'').replace('.out','')
                try : findex = int(index_str)
                except : continue
                _fnames[findex] = fname
            fnames = [fname for i,fname in sorted(_fnames.items(), key=lambda e:e[0])]
            
            #------------------------------------------------------------------
            if len(fnames) == 0 :
                print("aucun fichier")
                continue
            
            #------------------------------------------------------------------
            if len(fnames) != NT :
                print("Echec : nombre de fichiers incorrect ({} au lieu de {})".format(len(fnames), NT))
                continue
            
            #------------------------------------------------------------------
            variables = None
            M = None
            
            #------------------------------------------------------------------
            I = list(product(list(range(NX)), list(range(NY)), list(range(NZ)))) # TODO : vérifier l'ordre d'écriture
            
            #------------------------------------------------------------------
            for t,fname in enumerate(fnames) :
                path = os.path.join(os.path.dirname(self.input_path), fname)
                
                values = []
                
                _variables = None
                
                #--------------------------------------------------------------
                file = open(path, 'r')
                
                for l,line in enumerate(file) :
                    fields = line.strip().split()
                    if l == 0 : 
                        time = float(fields[-1])
                        if time != self.vects['T'].values[t] :
                            raise Exception("le temps du fichier '{}' devrait être".format(self.vects['T'].values[t]))
                        
                        continue
                    
                    #----------------------------------------------------------
                    if line.startswith('#') : continue
                    
                    #----------------------------------------------------------
                    if _variables is None :
                        if fields[0] == 'Distance' : _variables = fields.copy()
                        else :
                            if len(fields) == 2 : _variables = ['Distance',out]
                            else : _variables = ['Distance'] + ["{}_{}".format(out,i+1) for i in range(len(fields)-1)]
                            
                        NF = len(_variables)
                        if M is None : M = np.full((NX,NY,NZ,NT,NF), np.nan)
                        if variables is None : variables = _variables.copy()
                        elif variables is not None and variables != _variables : raise Exception("les variables ne sont pas idendiques")
                        
                        if fields[0] == 'Distance' : continue
                    
                    #----------------------------------------------------------
                    try : values += [float(v) for v in fields]
                    except : print("ECHEC", fname, l, line)
                
                #--------------------------------------------------------------
                file.close()
                
                #--------------------------------------------------------------
                _M = np.array(values).reshape((NM,NF))
                for m in range(NM) :
                    i,j,k = I[m]
                    M[i,j,k,t,:] = _M[i,:]
                
            #------------------------------------------------------------------        
            path = [Calcul.RESULTS_NAME, "Spatials", out]
            matrix = Matrix(path       = path,
                            label      = out,
                            dimensions = ['X','Y','Z','T',Matrix.FIELDS_NAME],
                            axes_paths = axes_paths,
                            fields     = variables,
                            M          = M,
                            )
            self.results.append(matrix)
            
            #------------------------------------------------------------------
            print("OK ({} fichiers, {} variables)".format(NT,NF))
            
    #==========================================================================
    
    
    #==========================================================================
    #---- *** SAVE TO NC ***
    #==========================================================================
    def _save(self, ds) :
        #----------------------------------------------------------------------
        if self.zones is not None :
            print("   - matériaux ... ", end="", flush=True)
            for zone in self.zones.values() : zone.save(ds)
            print("OK")
            
        #----------------------------------------------------------------------
        if self.results is not None :
            print("   - résultats ... ", end="", flush=True)
            for result in self.results : result.save(ds)
            print("OK")
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** PROGRAM ***
#------------------------------------------------------------------------------
if __name__ == '__main__' :
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Crunch/Problem-eauCO2-UNIX-REFERENCE/eauCO2.in"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Crunch/son68-essai/son68-essai.in"
    
    if len(sys.argv) > 1 :
        input_path = sys.argv[1]
        
        conv = Crunch_Convertor(input_path=input_path)
        print(conv.nc_path)
    
    # else :
    #     input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Crunch/CB_son68_ep-tous-poles-ssespsec-ssphasesec-1m3-SV7636-surf_const-verif-v2020/son68-touspoles.in"
    #     conv = Crunch_Convertor(input_path=input_path, name='test')
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
