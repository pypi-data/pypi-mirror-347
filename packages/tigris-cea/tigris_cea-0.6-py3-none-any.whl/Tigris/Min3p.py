# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import numpy as np
import datetime
from itertools import product
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Vector, Mesh
from Element_Matrix import Matrix
from Calcul import Calcul, Calcul_Convertor
from utils import get_temp_path, get_now
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Min3p(Calcul) :
    
    #==========================================================================
    CODE      = 'min3p'
    #--------------------------------------------------------------------------
    ATTR_INPUTPATH = 'INPUT_PATH'
    #--------------------------------------------------------------------------
    OUTPUTS_DESCRIPTIONS = {}
    OUTPUTS_DESCRIPTIONS['aqt']   = "Record of the spatial distribution of all component concentrations before batch reactions"
    OUTPUTS_DESCRIPTIONS['cbt']   = "Charge balance output for multicomponent diffusion (MCD)"
    OUTPUTS_DESCRIPTIONS['ebal']  = "System energy balance"
    OUTPUTS_DESCRIPTIONS['ebalc'] = "Energy balance contributions"
    OUTPUTS_DESCRIPTIONS['ebale'] = "Energy balance error"
    OUTPUTS_DESCRIPTIONS['evap']  = "Climate output"
    OUTPUTS_DESCRIPTIONS['gbac']  = "Acticity coefficient for primary and secondary aqueous species at output location x"
    OUTPUTS_DESCRIPTIONS['gbb']   = "Surface species at output location x"
    OUTPUTS_DESCRIPTIONS['gbc']   = "Aqueous species concentrations at output location x"
    OUTPUTS_DESCRIPTIONS['gbd']   = "Mineral dissolution-precipitation rates at output location x"
    OUTPUTS_DESCRIPTIONS['gbg']   = "Partial gas pressures at output location x"
    OUTPUTS_DESCRIPTIONS['gbgr']  = "Degassing rates at output location x"
    OUTPUTS_DESCRIPTIONS['gbi']   = "Reaction rates of intra-aqueous kinetic reactions at output location x"
    OUTPUTS_DESCRIPTIONS['gbis']  = "Isotope data at output location x"
    OUTPUTS_DESCRIPTIONS['gbm']   = "Master variables (pH, pe, Eh, ionic strength, alkalinity, temperature) at output location x"
    OUTPUTS_DESCRIPTIONS['gbp']   = "???" # TODO
    OUTPUTS_DESCRIPTIONS['gbs']   = "Mineral saturation indices at output location x"
    OUTPUTS_DESCRIPTIONS['gbt']   = "Total aqueous component concentrations at output location x"
    OUTPUTS_DESCRIPTIONS['gbv']   = "Mineral volume fractions at output location x"
    OUTPUTS_DESCRIPTIONS['gbx']   = "Saturation indices of excluded minerals at output location x"
    OUTPUTS_DESCRIPTIONS['gmf']   = "Total flux of each aqueous component for multicomponent diffusion (MCD)"
    OUTPUTS_DESCRIPTIONS['gsac']  = "Acticity coefficient for primary and secondary aqueous species at output time x"
    OUTPUTS_DESCRIPTIONS['gsb']   = "Surface species at output time x"
    OUTPUTS_DESCRIPTIONS['gsc']   = "Aqueous species concentrations at output time x"
    OUTPUTS_DESCRIPTIONS['gsd']   = "Mineral dissolution-precipitation rates at output time x"
    OUTPUTS_DESCRIPTIONS['gsg']   = "Partial gas pressures at output time level x"
    OUTPUTS_DESCRIPTIONS['gsgr']  = "Degassing rates at output time x"
    OUTPUTS_DESCRIPTIONS['gsi']   = "Reaction rates of intra-aqueous kinetic reactions at output time x"
    OUTPUTS_DESCRIPTIONS['gsis']  = "Isotope data at output time x"
    OUTPUTS_DESCRIPTIONS['gsm']   = "Master variables (pH, pe, Eh, ionic strength, alkalinity, temperature) at output time x"
    OUTPUTS_DESCRIPTIONS['gsp']   = "Hydraulic head, pressure head, water and gas saturations, moisture and gas contents at output time x"
    OUTPUTS_DESCRIPTIONS['gss']   = "Mineral saturation indices at output time x"
    OUTPUTS_DESCRIPTIONS['gst']   = "Total aqueous component concentrations at output time x"
    OUTPUTS_DESCRIPTIONS['gsv']   = "Mineral volume fractions at output time x"
    OUTPUTS_DESCRIPTIONS['gsx']   = "Saturation indices of excluded minerals at output time x"
    OUTPUTS_DESCRIPTIONS['hyc']   = "Initial hydraulic conductivity distribution"
    OUTPUTS_DESCRIPTIONS['lbac']  = "Acticity coefficient for primary and secondary aqueous species"
    OUTPUTS_DESCRIPTIONS['lbb']   = "Surface species"
    OUTPUTS_DESCRIPTIONS['lbc']   = "Aqueous species concentrations"
    OUTPUTS_DESCRIPTIONS['lbd']   = "Mineral dissolution-precipitation rates"
    OUTPUTS_DESCRIPTIONS['lbg']   = "Partial gas pressures"
    OUTPUTS_DESCRIPTIONS['lbgr']  = "Degassing rates"
    OUTPUTS_DESCRIPTIONS['lbi']   = "Reaction rates of intra-aqueous kinetic reactions"
    OUTPUTS_DESCRIPTIONS['lbm']   = "Master variables (pH, pe, Eh, ionic strength, alkalinity,temperature)"
    OUTPUTS_DESCRIPTIONS['lbs']   = "Mineral saturation indices"
    OUTPUTS_DESCRIPTIONS['lbt']   = "Total aqueous component"
    OUTPUTS_DESCRIPTIONS['lbv']   = "Mineral volume fractions"
    OUTPUTS_DESCRIPTIONS['lbx']   = "Saturation indices of excluded minerals"
    OUTPUTS_DESCRIPTIONS['mac']   = "Mass balance (in moles/d) for the xth aqueous component"
    OUTPUTS_DESCRIPTIONS['mae']   = "Mass balance error (in moles) for the xth aqueous component"
    OUTPUTS_DESCRIPTIONS['mas']   = "Total mass (in moles) of all aqueous components"
    OUTPUTS_DESCRIPTIONS['mgc']   = "Mass flux"
    OUTPUTS_DESCRIPTIONS['mgs']   = "Total mass (in moles) of all gases"
    OUTPUTS_DESCRIPTIONS['mmc']   = "Mass balance (in moles/d) for the xth mineral component"
    OUTPUTS_DESCRIPTIONS['mms']   = "Total mass (in moles) of all mineral components"
    OUTPUTS_DESCRIPTIONS['mss']   = "Total mass (in moles) of all sorbed species"
    OUTPUTS_DESCRIPTIONS['mvc']   = "Mass balance in total flux"
    OUTPUTS_DESCRIPTIONS['mve']   = "Mass balance errors"
    OUTPUTS_DESCRIPTIONS['mvs']   = "Mass balance files of liquid"
    OUTPUTS_DESCRIPTIONS['vel']   = "Interfacial velocities at output time x"
    
    #--------------------------------------------------------------------------
    OUTPUTS_DIMENSIONS = {}
    for ext in ['aqt','hyc']                                     : OUTPUTS_DIMENSIONS[ext] = ('XC','YC','ZC')
    for ext in ['gsc','gsd','gsg','gsm','gsp','gss','gst','gsv'] : OUTPUTS_DIMENSIONS[ext] = ('XC','YC','ZC','T_spatial')
    for ext in ['gbc','gbd','gbg','gbm','gbs','gbt','gbv','gbp'] : OUTPUTS_DIMENSIONS[ext] = ('T_transient',) # TODO : GBP ?
    for ext in ['mac','mae']                                     : OUTPUTS_DIMENSIONS[ext] = ('Component','T_simulation',)
    for ext in ['mmc']                                           : OUTPUTS_DIMENSIONS[ext] = ('Mineral','T_simulation',)
    for ext in ['mas','mgc','mgs','mms','mvc','mve','mvs']       : OUTPUTS_DIMENSIONS[ext] = ('T_simulation',)
    for ext in ['vel']                                           : OUTPUTS_DIMENSIONS[ext] = ('XE','YE','ZE','T_spatial')
    #--------------------------------------------------------------------------
    OUTPUTS_VARIABLES = {}
    OUTPUTS_VARIABLES['mac'] = []
    OUTPUTS_VARIABLES['mac'].append(("time"           , "time [years]"))
    OUTPUTS_VARIABLES['mac'].append(("influx"         , "mass influx [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("outflux"        , "mass outflux [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("storage"        , "change in storage [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("oxred"          , "source/sink from oxidation/reduction reactns [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("aqueous"        , "source/sink from intra-aqueous reactns [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("mineral"        , "source/sink from mineral phase [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("gas"            , "source/sink from gas phase [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("influx_gas"     , "mass influx (gas phase) [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("outflux_gas"    , "mass outflux (gas phase) [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("storage_gas"    , "change in storage (gas phase) [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("loss"           , "mass loss - degassing [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("sorbed"         , "source/sink from sorbed phase [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("root_uptake"    , "source/sink from root uptake [mol/d]"))
    OUTPUTS_VARIABLES['mac'].append(("influx_tot"     , "total mass influx [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("outflux_tot"    , "total mass outflux [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("storage_tot"    , "total change in storage [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("oxred_tot"      , "total source/sink from oxidation/reduction reactns [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("aqueous_tot"    , "total source/sink from intra-aqueous reactns [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("mineral_tot"    , "total source/sink from mineral phase [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("gas_tot"        , "total source/sink from gas phase [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("influx_gas_tot" , "total mass influx (gas phase) [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("outflux_gas_tot", "total mass outflux (gas phase) [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("storage_gas_tot", "total change in storage (gas phase) [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("loss_tot"       , "total mass loss - degassing [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("sorbed_tot"     , "total source/sink from sorbed phase [mol/elapsed time]"))
    OUTPUTS_VARIABLES['mac'].append(("root_uptake_tot", "total source/sink from root uptake [mol/elapsed time]"))
    
    OUTPUTS_VARIABLES['mae'] = []
    OUTPUTS_VARIABLES['mae'].append(("time"                     , "time [years]"))
    OUTPUTS_VARIABLES['mae'].append(("absolute_error"           , "absolute mass balance error [mol]"))
    OUTPUTS_VARIABLES['mae'].append(("relative_error"           , "relative mass balance error [% of system mass]"))
    OUTPUTS_VARIABLES['mae'].append(("absolute_cumulative_error", "absolute cumulative mass balance error [mol] "))
    OUTPUTS_VARIABLES['mae'].append(("relative_cumulative_error", "relative cumulative mass balance error [% of system mass]"))
    
    OUTPUTS_VARIABLES['mmc'] = []
    OUTPUTS_VARIABLES['mmc'].append(("time"                 , "time [years]"))
    OUTPUTS_VARIABLES['mmc'].append(("storage"              , "change in storage [mol/d]"))
    OUTPUTS_VARIABLES['mmc'].append(("aqueous"              , "source/sink - aqueous phase [mol/d]"))
    OUTPUTS_VARIABLES['mmc'].append(("contribution"         , "total contribution [mol]"))
    OUTPUTS_VARIABLES['mmc'].append(("aqueous_parallel"     , "source/sink - aqueous phase parallel reaction pathways [mol/d]"))
    OUTPUTS_VARIABLES['mmc'].append(("contribution_parallel", "total contribution parallel reaction pathways [mol/d]"))
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        Calcul.__init__(self, Min3p.CODE)
        
        #----------------------------------------------------------------------
        self.results = None
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        extensions = []
        for e in self.results :
            ext = e.get_attribute('extension') 
            if ext not in extensions : extensions.append(ext)
        print("   - résultats".ljust(Calcul.DETAILS_ALIGN,' ')+": {} extensions ({})".format(len(extensions), ",".join(extensions)))
        
    #==========================================================================
    def _load(self) :
        #----------------------------------------------------------------------
        self.results = []
        
        #----------------------------------------------------------------------
        for e in self.elements :
            if e.path[0] == Calcul.RESULTS_NAME : self.results.append(e)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Min3p_Convertor(Calcul_Convertor) :

    
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
        print("> Conversion d'un calcul {} :".format(Calcul.CODE_NAMES[Min3p.CODE]))
        
        #----------------------------------------------------------------------
        if 'input_path' not in opts.keys() :
            raise Exception("paramètre 'input_path' manquant")
        
        #----------------------------------------------------------------------
        self.input_path = opts.get('input_path')
        self.name = opts.get('name', os.path.basename(".".join(self.input_path.split(".")[:-1])))
        self.dirpath = os.path.dirname(self.input_path)
        #----------------------------------------------------------------------
        kwargs = {}
        kwargs[Calcul.ATTR_CODE]     = Min3p.CODE
        kwargs[Calcul.ATTR_CALCUL]   = self.name
        kwargs[Calcul.ATTR_POSTDATE] = get_now(fmt='%d/%m/%Y %H:%M')
        kwargs[Calcul.ATTR_DIRPATH]  = self.dirpath
        #----------------------------------------------------------------------
        kwargs[Min3p.ATTR_INPUTPATH] = self.input_path
        #----------------------------------------------------------------------
        self.config = Element(path=[Calcul.CONFIG_NAME], label='config', **kwargs)
        
        #----------------------------------------------------------------------
        self.read_inputs()
        self.configure_coords()
        self.configure_results()
        self.configure_times()
        
    #==========================================================================
    def read_inputs(self) :
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
        file = open(self.input_path, 'r')
        inname = os.path.basename(self.input_path)
        kw = None
        #----------------------------------------------------------------------
        for l,line in enumerate(file) :
            #------------------------------------------------------------------
            line = line.strip()
            
            #------------------------------------------------------------------
            if line == "" : continue
            if line[0] == "!" : continue
            if ';' in line : line = line[:line.index(';')].strip()
            
            #------------------------------------------------------------------
            # if "global control parameters"          in line : kw = "section1" ; continue
            if "spatial discretization"             in line : kw = "section3" ; continue
            # if "time step control - global system"  in line : kw = "section4" ; continue
            if "output of spatial data"             in line : kw = "section8a" ; continue
            if "output of transient data"           in line : kw = "section8b" ; continue
            if "'physical parameters - porous medium'" in line : kw = "section9" ; continue
            #------------------------------------------------------------------
            if "output control"    in line : kw = None
            if "coordinate output" in line : kw = None
            if "'done'"            in line : kw = None
            
            #------------------------------------------------------------------
            self.input_lines['raw'].append(line)
            self.input_lines['origin'].append((inname, l+1))
            self.input_lines['key_word'].append(kw)
            
        #----------------------------------------------------------------------
        print('OK ({} lignes)'.format(len(self.input_lines['raw'])))
        
    #==========================================================================
    def configure_coords(self) :
        #----------------------------------------------------------------------
        print("   - préparation des coordonnées ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'section3']

        #----------------------------------------------------------------------
        lines = []
        full_cell = False
        for l,line in input_llines :
            if 'full cells' in line : full_cell = True
            else : lines.append(line)
            
        #----------------------------------------------------------------------
        N_tot = 1
        for dim in ['X','Y','Z'] :
            edges = [] # coord du point (edge)
            Nz = int(lines.pop(0)) # nombre de zones
            for zi in range(Nz) :
                N = int(lines.pop(0)) # nombre de mailles
                vmin,vmax = [round(float(field.strip().replace("d","e")),5) for field in lines.pop(0).split()]
                dv = round(float((vmax-vmin)/float(N)),5)
                
                if len(edges) == 0 : edges.append(vmin)
                if edges[-1] != vmin :
                    l = input_llines[len(input_llines)-len(lines)-1][0]
                    raise Exception("fichier {}, ligne {} : non-continuité des coordonnées ({} -> {})".format(*self.input_lines['origin'][l], edges[-1], vmin))
                    
                for n in range(N) :
                    edges.append(round(edges[-1]+dv,5))
                
            #------------------------------------------------------------------
            if len(edges) == 0 : edges = [0.0,1.0]
            
            #------------------------------------------------------------------
            self.meshs[dim] = Mesh(path=[Calcul.COORD_NAME, dim],
                                    dimension=dim,
                                    edges=edges)
            
            #------------------------------------------------------------------
            if not full_cell :
                self.meshs[dim].centers[0] = self.meshs[dim].edges[0]
                self.meshs[dim].centers[-1] = self.meshs[dim].edges[-1]
            
            N_tot *= self.meshs[dim].N
            
        #----------------------------------------------------------------------
        Ns = [self.meshs[dim].N for dim in ['X','Y','Z']]
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'section8a']
        T_spatial = [0.0] + [float(field.replace('d','e')) for field in " ".join([line[1] for line in input_llines[1:]]).split()]
        self.vects['T_spatial'] = Vector(path=[Calcul.COORD_NAME,'T_spatial'],
                                         dimension='T',
                                         values=T_spatial)
            
        #----------------------------------------------------------------------
        print('OK')
        print("      - maillage  : {} x {} x {} = {} mailles".format(*Ns, np.prod(Ns)))
        print("      - spatial   : {} instant(s)".format(self.vects['T_spatial'].N))
        
    #==========================================================================
    def configure_results(self) :
        #----------------------------------------------------------------------
        print("   - préparation des fichiers de sortie :")
        self.results = []
        
        #----------------------------------------------------------------------
        root_name = ".".join(os.path.basename(self.input_path).split(".")[:-1])+"_"
        files_by_ext = {}
        for fname in os.listdir(self.dirpath) :
            if not fname.startswith(root_name) : continue
            ext = fname.split(".")[-1]
            dimensions  = Min3p.OUTPUTS_DIMENSIONS.get(ext, None)
            
            if dimensions is None :
                continue
        
            if ext not in files_by_ext.keys() : files_by_ext[ext] = []
            files_by_ext[ext].append(fname)
            
        #----------------------------------------------------------------------
        NX = self.meshs['X'].N
        NY = self.meshs['Y'].N
        NZ = self.meshs['Z'].N
        
        #----------------------------------------------------------------------
        C_KJI = np.array(list(product(range(NZ),range(NY),range(NX))))
        IC,JC,KC = C_KJI[:,2], C_KJI[:,1], C_KJI[:,0] # indices de lecture des coordonnées (centers) dans les fichiers X,Y,Z
        
        #----------------------------------------------------------------------
        E_I = range(1,NX-1+1) if NX > 1 else range(1)
        E_J = range(1,NY-1+1) if NY > 1 else range(1)
        E_K = range(1,NZ-1+1) if NZ > 1 else range(1)
        E_KJI = np.array(list(product(E_K,E_J,E_I)))
        IE,JE,KE = E_KJI[:,2], E_KJI[:,1], E_KJI[:,0] # indices de lecture des coordonnées (edges) dans les fichiers X,Y,Z
        
        #----------------------------------------------------------------------
        for ext,fnames in sorted(files_by_ext.items()) :
            
            dimensions = Min3p.OUTPUTS_DIMENSIONS.get(ext, None)
            print("      - extension '{}' : {} fichier(s)".format(ext, len(fnames)), dimensions)
            
            #---- XC,YC,ZC ----------------------------------------------------
            if dimensions == ('XC','YC','ZC') : # 1 seul fichier
                filepath = os.path.join(self.dirpath, fnames[0])
                file = open(filepath, 'r')
                file.readline()
                variables = Min3p_Convertor.read_variables(file.readline())
                file.close()
                
                H = variables[3:]
                axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
                sizes      = {dim:self.meshs[dim].N for dim in ['X','Y','Z']}
                sizes['FIELDS'] = len(H)
                matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext],
                                label       = ext,
                                dimensions  = ['X','Y','Z','FIELDS'],
                                axes_paths  = axes_paths,
                                sizes       = sizes,
                                fields      = H,
                                extension   = ext,
                                description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                )
                
                matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                
                T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                for l in range(len(T)) : matrix.M[IC[l],JC[l],KC[l],:] = T[l,3:]
                self.results.append(matrix)
                
            #---- XC,YC,ZC,T_spatial ---------------------------------------
            if dimensions == ('XC','YC','ZC','T_spatial') :
                fname_by_suffix = {int(fname.replace(root_name,"").replace("."+ext,"")):fname for fname in fnames}
                
                axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
                axes_paths['T'] = self.vects['T_spatial'].path
                
                sizes = {dim:self.meshs[dim].N for dim in ['X','Y','Z']}
                sizes['T'] = self.vects['T_spatial'].N
                
                matrix = None
                variables = None
                for t,fname in sorted(fname_by_suffix.items()) :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    _variables = Min3p_Convertor.read_variables(line2)
                    if variables is None : variables = _variables
                    elif _variables != variables : raise Exception("variables incohérentes")
                    steady_state = "steady state" in line3 # pas de variation dans le temps
                    file.close()
                    
                    if matrix is None :
                        sizes['FIELDS'] = len(variables)-3
                        matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext],
                                        label       = ext,
                                        dimensions  = ['X','Y','Z','T','FIELDS'],
                                        axes_paths  = axes_paths,
                                        sizes       = sizes,
                                        fields      = variables[3:],
                                        extension   = ext,
                                        description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                        )
                        matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    
                    for l in range(len(T)) :
                        if steady_state : matrix.M[IC[l],JC[l],KC[l],:,:] = T[l,3:]
                        else            : matrix.M[IC[l],JC[l],KC[l],t,:] = T[l,3:]
                self.results.append(matrix)
                
            #---- XE,YE,ZE,T_spatial ------------------------------------------
            elif dimensions == ('XE','YE','ZE','T_spatial') :
                fname_by_suffix = {int(fname.replace(root_name,"").replace("."+ext,"")):fname for fname in fnames}
                axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
                axes_paths['T'] = self.vects['T_spatial'].path
                
                sizes = {dim:self.meshs[dim].N+1 for dim in ['X','Y','Z']}
                sizes['T'] = self.vects['T_spatial'].N
                
                matrix = None
                variables = None
                for t,fname in sorted(fname_by_suffix.items()) :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    _variables = Min3p_Convertor.read_variables(line2)
                    if variables is None : variables = _variables
                    elif _variables != variables : raise Exception("variables incohérentes")
                    steady_state = "steady state" in line3 # pas de variation dans le temps
                    file.close()
                    
                    if matrix is None :
                        sizes['FIELDS'] = len(variables)-3
                        matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext],
                                        label       = ext,
                                        dimensions  = ['X','Y','Z','T','FIELDS'],
                                        axes_paths  = axes_paths,
                                        axes_stags  = ['X','Y','Z'],
                                        sizes       = sizes,
                                        fields      = variables[3:],
                                        extension   = ext,
                                        description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                        )
                        matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    for l in range(len(T)) :
                        if steady_state : matrix.M[IE[l],JE[l],KE[l],:,:] = T[l,3:]
                        else            : matrix.M[IE[l],JE[l],KE[l],t,:] = T[l,3:]
                self.results.append(matrix)
                
                
            #---- T_transient -------------------------------------------------
            elif dimensions == ('T_transient',) :
                fname_by_suffix = {int(fname.replace(root_name,"").replace("."+ext,"")):fname for fname in fnames}
                
                for p,fname in sorted(fname_by_suffix.items()) :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    variables = Min3p_Convertor.read_variables(line2)
                    file.close()
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    if T[0,0] != 0.0 : T = np.insert(T, 0, np.full((1,T.shape[1]), np.nan), axis=0) ; T[0,0] = 0.0
                    
                    if 'T_transient' not in self.vects.keys() :
                        self.vects['T_transient'] = Vector(path=[Calcul.COORD_NAME,'T_transient'],
                                                            dimension='T',
                                                            values=T[:,0])
                    
                    axes_paths = {'T':self.vects['T_transient'].path}
                    sizes      = {'T':self.vects['T_transient'].N, 'FIELDS' : len(variables)-1}
                    matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext, "Point{}".format(p)],
                                    label       = "{}_Point{}".format(ext, p),
                                    dimensions  = ['T','FIELDS'],
                                    axes_paths  = axes_paths,
                                    sizes       = sizes,
                                    fields      = variables[1:],
                                    extension   = ext,
                                    description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                    )
                    matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    matrix.M[:] = T[:,1:]
                    self.results.append(matrix)
                    
            
            #---- Component,T_simulation --------------------------------------
            elif dimensions == ('Component','T_simulation',) :
                ext_variables = Min3p.OUTPUTS_VARIABLES.get(ext,None)
                
                for fname in fnames :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    fields3 = line3.split()
                    component = fields3[fields3.index('component')+1]
                    variables = Min3p_Convertor.read_variables(line2)
                    file.close()
                    
                    if ext_variables is not None :
                        variables = [ext_variable[0] for ext_variable in ext_variables]
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    if T[0,0] != 0.0 : T = np.insert(T, 0, np.full((1,T.shape[1]), np.nan), axis=0) ; T[0,0] = 0.0
                    
                    if 'T_simulation' not in self.vects.keys() :
                        self.vects['T_simulation'] = Vector(path=[Calcul.COORD_NAME,'T_simulation'],
                                                             dimension='T',
                                                             values=T[:,0])
                        
                    axes_paths = {'T':self.vects['T_simulation'].path}
                    sizes      = {'T':self.vects['T_simulation'].N, 'FIELDS' : len(variables)-1}
                    matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext, component],
                                    label       = component,
                                    dimensions  = ['T','FIELDS'],
                                    axes_paths  = axes_paths,
                                    sizes       = sizes,
                                    fields      = variables[1:],
                                    extension   = ext,
                                    component   = component,
                                    description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                    )
                    matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    matrix.M[:] = T[:,1:]
                    self.results.append(matrix)
                    
                    
            #---- Mineral,T_simulation --------------------------------------
            elif dimensions == ('Mineral','T_simulation',) :
                
                ext_variables = Min3p.OUTPUTS_VARIABLES.get(ext,None)
                if ext_variables is None :
                    print("sorties non renommées")
                
                for fname in fnames :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    mineral = line3.split('"')[1].split()[-1]
                    variables = Min3p_Convertor.read_variables(line2)
                    file.close()
                    
                    if ext_variables is not None :
                        variables = [ext_variable[0] for ext_variable in ext_variables]
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    if T[0,0] != 0.0 : T = np.insert(T, 0, np.full((1,T.shape[1]), np.nan), axis=0) ; T[0,0] = 0.0
                        
                    if 'T_simulation' not in self.vects.keys() :
                        self.vects['T_simulation'] = Vector(path=[Calcul.COORD_NAME,'T_simulation'],
                                                             dimension='T',
                                                             values=T[:,0])
            
                    axes_paths = {'T':self.vects['T_simulation'].path}
                    sizes      = {'T':self.vects['T_simulation'].N, 'FIELDS' : len(variables)-1}
                    matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext, mineral],
                                    label       = mineral,
                                    dimensions  = ['T','FIELDS'],
                                    axes_paths  = axes_paths,
                                    sizes       = sizes,
                                    fields      = variables[1:],
                                    extension   = ext,
                                    mineral   = mineral,
                                    description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                    )
                    matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    matrix.M[:] = T[:,1:]
                    self.results.append(matrix)
                    
                    
            #---- T_simulation ------------------------------------------------
            elif dimensions == ('T_simulation',) : # 1 seul fichier
                
                for fname in fnames :
                    filepath = os.path.join(self.dirpath, fname)
                    file = open(filepath, 'r')
                    file.readline()
                    line2 = file.readline()
                    line3 = file.readline()
                    
                    fields3 = line3.split()
                    variables = Min3p_Convertor.read_variables(line2)
                    file.close()
                    
                    ext_variables = Min3p.OUTPUTS_VARIABLES.get(ext,None)
                    if ext_variables is not None : variables = [ext_variable[0] for ext_variable in ext_variables]
                    
                    T = np.loadtxt(filepath, delimiter=None, skiprows=3)
                    if T[0,0] != 0.0 : T = np.insert(T, 0, np.full((1,T.shape[1]), np.nan), axis=0) ; T[0,0] = 0.0
                        
                    if 'T_simulation' not in self.vects.keys() :
                        self.vects['T_simulation'] = Vector(path=[Calcul.COORD_NAME,'T_simulation'],
                                                             dimension='T',
                                                             values=T[:,0])
                        
                    axes_paths = {'T':self.vects['T_simulation'].path}
                    sizes      = {'T':self.vects['T_simulation'].N, 'FIELDS' : len(variables)-1}
                    matrix = Matrix(path        = [Calcul.RESULTS_NAME, ext],
                                    label       = ext,
                                    dimensions  = ['T','FIELDS'],
                                    axes_paths  = axes_paths,
                                    sizes       = sizes,
                                    fields      = variables[1:],
                                    extension   = ext,
                                    description = Min3p.OUTPUTS_DESCRIPTIONS.get(ext, None),
                                    )
                    matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                    matrix.M[:] = T[:,1:]
                    self.results.append(matrix)
                    
    #==========================================================================
    def configure_times(self) :
        #----------------------------------------------------------------------
        print("   - préparation des temps ... ", end="", flush=True)
        #----------------------------------------------------------------------
        times = []
        
        for k in ['T_spatial','T_transient','T_simulation'] :
            if k in self.vects.keys() : 
                times += list(self.vects[k].values)
        
        # times += list(self.vects['T_spatial'].values)
        # times += list(self.vects['T_transient'].values)
        # times += list(self.vects['T_simulation'].values)
        times = np.unique(times)
        
        #----------------------------------------------------------------------
        self.vects['T'] = Vector(path=[Calcul.COORD_NAME,'T'],
                                 dimension='T',
                                 values=times)
        
        #----------------------------------------------------------------------
        print("OK")
        
    #==========================================================================
    def read_variables(line) :
        #----------------------------------------------------------------------
        variables = []
        #----------------------------------------------------------------------
        for v in line.replace("variables = ","").replace('"','').split(",") :
            v = v.strip()
            if v.split()[0] == 'time' :
                v = "time"
                variables.append(v)
                continue
            v = v.replace(" ","_")
            v = v.replace("/","_by_")
            v = v.replace("[","(")
            v = v.replace("]",")")
            variables.append(v)
        #----------------------------------------------------------------------
        return variables
        
    #==========================================================================
    
    
    #==========================================================================
    #---- *** SAVE TO NC ***
    #==========================================================================
    def _save(self, ds) :
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
    input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/Benchmark_SergioBea_dtmax2000s/atm_carbon_dtdiv100.dat"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/CERIB_NonReactif_ParamHR62opt/CERIB_NonReactif_ParamHR62opt.dat"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/CERIB_NonReactif_ParamHR62opt_Phases12_1/CERIB_NonReactif_ParamHR62opt_Phases12_1.dat"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/CalculBench_Cas2_TRmailles_32zones_2points__isoT_PasPerm/CalculBench_Cas2_TRmailles_32zones_2points_isoT_PasPerm.dat"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/Test2_MassBalance/Reference_32mailles_MassBalance.dat"
    
    # input_path = r"//lurs/_Unites/DTN/SMTA/LMTE/LMTE_Collaborateurs/Julien_T/Calculs_MIN3P/4-CEMVRombas_HR62opt_TestCourt/ConfigCERIB_SansEnergy_Rombas_HR62opt_ChimieSBea.dat"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/MIN3P/Test_MQ_a2b4.2_Ref/CalculBench_Cas2_TestMQa2b42_Ref.dat"
    
    # nc_path    = os.path.join(os.path.dirname(input_path), os.path.basename(input_path).replace(".inp",".nc"))
    # nc_path    = os.path.join(os.path.dirname(input_path), "test.nc")
    
    conv = Min3p_Convertor(input_path=input_path, name='test')
    
    # nc_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Rombas_HR62opt_ChimieSBea_CarboAtmo_VoileConteneur_100a_MaillageFin.nc"
    # calcul = Min3p()
    # calcul.load(nc_path=nc_path)
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
