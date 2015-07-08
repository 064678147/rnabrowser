'''
Created on Nov 24, 2009

@author: rtbreit
'''

DB_HOST = 'localhost'           # hostname of MySQL database server
DB_USER = 'efp_user'            # username for database access
DB_PASSWD = 'efp_user'          # password for database access
DB_ANNO = 'rice_annotations_lookup'  # database name for annotations lookup
DB_ORTHO = 'ortholog_db'		# ortholog DB

# lookup table for gene annotation
DB_ANNO_TABLE = 'loc_annotation'
DB_ANNO_GENEID_COL = 'loc'
DB_ORTHO_LOOKUP_TABLE = 'rice_maize_lookup'
DB_ORTHO_GENEID_COL = 'rice_id'
# lookup table for probeset id
DB_LOOKUP_TABLE = 'at_loc_lookup'
DB_LOOKUP_GENEID_COL = 'loc'

# lookup tables for ncbi ids
DB_NCBI_GENE_TABLE = None
DB_NCBI_PROT_TABLE = None
DB_NCBI_GENEID_COL = None

#Check Y-AXIS message
Y_AXIS = {}
Y_AXIS['rice_mas'] = "GCOS expression signal (TGT=100, Bkg=20)"
Y_AXIS['rice_rma'] = "RMA expression signal"
#Y_AXIS['rice_leaf_gradient'] = "RPKM expression signal"
#Y_AXIS['rice_maize_comparison'] = "RPKM expression signal"

#Check if lookup exists
LOOKUP = {}
#LOOKUP['rice_leaf_gradient'] = "0"
#LOOKUP['rice_maize_comparison'] = "0"
LOOKUP['rice_mas'] = "1"
LOOKUP['ricestigma_mas'] = "1"
LOOKUP['riceanoxia_mas'] = "1"
LOOKUP['ricestress_mas'] = "1"
LOOKUP['rice_rma'] = "1"
LOOKUP['ricestigma_rma'] = "1"
LOOKUP['riceanoxia_rma'] = "1"
LOOKUP['ricestress_rma'] = "1"

# initial gene ids when start page is loaded
GENE_ID_DEFAULT1 = 'LOC_Os01g01080'
GENE_ID_DEFAULT2 = 'LOC_Os06g10770'

# the little graph on the tga image has a scale
# such that 1 unit is x pixels for different ranges on the x-axis of the graph
# the GRAPH_SCAL_UNIT consists of value pairs: upper end of range and scale unit
# so ((1000, 0.031), (10000, 0.003222), (1000000, 0.00031)) means:
# use 0.031 as scale unit for 0 < signal < 1000
# use 0.003222 as scale unit for 1000 < signal < 10000
# use 0.00031 as scale unit for 10000 < signal < 1000000
# see also efp.drawImage()
GRAPH_SCALE_UNIT = {}
# the default values are used if for the given data source no special values are defined
# GRAPH_SCALE_UNIT["default"] = ((0.06, 16) (0.006, 73), (0.0006, 130))
GRAPH_SCALE_UNIT["rice_mas"] = [(1000, 0.06), (10000, 0.006), (100000, 0.0006)]
GRAPH_SCALE_UNIT["ricestigma_mas"] = [(1000, 0.08), (10000, 0.008), (10000, 0.0008)]
GRAPH_SCALE_UNIT["riceanoxia_mas"] = [(1000, 0.06), (10000, 0.006), (100000, 0.0006)]
GRAPH_SCALE_UNIT["ricestress_mas"] = [(1000, 0.09), (10000, 0.009), (100000, 0.0009)]
#GRAPH_SCALE_UNIT["rice_leaf_gradient"] = [(10, 5), (100, 0.05), (1000, 0.005), (10000, 0.0005), (100000, 0.00005) ]
#GRAPH_SCALE_UNIT["rice_maize_comparison"] = [(10, 5), (100, 0.05), (1000, 0.005), (10000, 0.0005), (100000, 0.00005) ]
GRAPH_SCALE_UNIT["rice_rma"] = [(1000, 10)]
GRAPH_SCALE_UNIT["ricestigma_rma"] = [(1000, 10)]
GRAPH_SCALE_UNIT["riceanoxia_rma"] = [(1000, 13)]
GRAPH_SCALE_UNIT["ricestress_rma"] = [(1000, 15)]

# define additional header text for individual data sources
# you can use key 'default' for each not individually defined
datasourceHeader = {}
datasourceHeader['default'] = ''

# define additional footer text for individual data sources
# you can use key 'default' for each not individually defined
datasourceFooter = {}
datasourceFooter['default'] = ''

# regular expression for check of gene id input
inputRegEx = "(LOC_Os[0-9]{2}g[0-9]{5})|(((AFFX|AFFX-Os)(-|_)(Ubiquitin|Actin|Cyph|Gapdh|BioB|BioC|BioDn|CreX|DapX|LysX|PheX|ThrX|TrpnX|ef1a|gapdh)(-|_)(3|5|M)_(at|x_at|s_at))|(AFFX-OS-(18SrRNA|25SrRNA|5.8SrRNA)_(s_at|at))|(AFFX-Mgr-(actin|ef1a|gapdh)-(3|5|M))_(at|x_at|s_at)|(AFFX-r2-Tag(A|B|C|D|E|F|G|H)_at)|(AFFX-r2-Tag(IN|I|J|O|Q)-(3|5|M)_at)|((AFFX|AFFX-Os)-r2-(Bs|Ec|P1)-(dap|lys|phe|thr|bioB|bioC|bioD|cre)-(3|5|M)(_|_x_|_s_)at)|(Os|OsAffx)\.[0-9]{1,5}\.[0-9]{1}\.(S1|A1|S2)_(at|x_at|s_at|a_at))"

# default thresholds
minThreshold_Compare = 0.6  # Minimum color threshold for comparison is 0.6, giving us [-0.6, 0.6] on the color legend
minThreshold_Relative = 0.6 # Minimum color threshold for median is 0.6, giving us [-0.6, 0.6] on the color legend ~ 1.5-Fold
minThreshold_Absolute = 10  # Minimum color threshold for max is 10, giving us [0, 10] on the color legend

# coordinates where to write gene id, probeset id and gene alias into image
GENE_ID1_POS = (0, 30)
GENE_ID2_POS = (0, 45)
GENE_PROBESET1_POS = (150, 30)
GENE_PROBESET2_POS = (150, 45)
GENE_ALIAS1_POS = (0, 0)
GENE_ALIAS2_POS = (0, 0)
GENE_ORTHO1_POS = (0,285)
defaultDataSource = 'rice_mas'
dataDir = 'data_rice'

dbGroupDefault = 'group1'
# list of datasources in same group to find max signal 
groupDatasource = {}
#groupDatasource["group1"] = ['rice_mas', 'rice_rma', 'rice_leaf_gradient', 'rice_maize_comparison']
groupDatasource["group1"] = ['rice_mas', 'rice_rma']

# mapping of xml files to show datasource name
groupDatasourceName = {}
#groupDatasourceName["group1"] = {'rice_mas':'rice_mas or ricestigma_mas or ricestress_mas', 'rice_rma':'rice_rma or ricestigma_rma or ricestress_rma', 'rice_leaf_gradient':'rice_leaf_gradient', 'rice_maize_comparison':'rice_maize_comparison'}
groupDatasourceName["group1"] = {'rice_mas':'rice_mas or ricestigma_mas or ricestress_mas', 'rice_rma':'rice_rma or ricestigma_rma or ricestress_rma'}

# ortholog configuration
# list of species where orthologs should be tried to retrieve (names must be the same as in ortholog db)
ortholog_species = ('POP', 'TAIR8', 'MEDV3', 'RICE', 'BARLEY', 'SOYBEAN')

efpLink = {}
efpLink['POP'] = "http://bar.utoronto.ca/efp_poplar/cgi-bin/efpWeb.cgi?dataSource=Poplar&primaryGene=%s&modeInput=Absolute"
efpLink['TAIR8'] = "http://bar.utoronto.ca/efp_arabidopsis/cgi-bin/efpWeb.cgi?dataSource=Developmental_Map&primaryGene=%s&modeInput=Absolute"
efpLink['MEDV3'] = "http://bar.utoronto.ca/efp_medicago/cgi-bin/efpWeb.cgi?dataSource=medicago_mas&primaryGene=%s&modeInput=Absolute"
efpLink['SOYBEAN'] = "http://bar.utoronto.ca/efp_soybean/cgi-bin/efpWeb.cgi?dataSource=soybean&primaryGene=%s&modeInput=Absolute"
efpLink['RICE'] = "http://bar.utoronto.ca/efp_rice/cgi-bin/efpWeb.cgi?dataSource=rice_mas&primaryGene=%s&modeInput=Absolute"
efpLink['BARLEY'] = "http://bar.utoronto.ca/efp_barley/cgi-bin/efpWeb.cgi?dataSource=barley_mas&primaryGene=%s&modeInput=Absolute"

species = 'RICE'

spec_names = {}
spec_names['POP'] = 'Poplar'
spec_names['TAIR8'] = 'Arabidopsis'
spec_names['MEDV3'] = 'Medicago'
spec_names['SOYBEAN'] = 'Soybean'
spec_names['RICE'] = 'Rice'
spec_names['BARLEY'] = 'Barley'

