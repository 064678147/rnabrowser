'''
Created on Nov 24, 2009

@author: rtbreit
'''

DB_HOST = 'localhost'           # hostname of MySQL database server
DB_USER = 'efp_user'            # username for database access
DB_PASSWD = 'efp_user'          # password for database access
DB_ANNO = 'medicago_annotations_lookup'  # database name for annotations lookup
DB_ORTHO = 'ortholog_db'		# ortholog DB

# lookup table for gene annotation
DB_ANNO_TABLE = 'mtgi_annotation'
DB_ANNO_GENEID_COL = 'mtgi'

# lookup table for probeset id
DB_LOOKUP_TABLE = 'at_mtgi_lookup'
DB_LOOKUP_GENEID_COL = 'mtgi'

# lookup tables for ncbi ids
DB_NCBI_GENE_TABLE = None
DB_NCBI_PROT_TABLE = None
DB_NCBI_GENEID_COL = None

#Check Y-AXIS message
Y_AXIS = {}
Y_AXIS['medicago_mas'] = "GCOS expression signal (TGT=100, Bkg=20)"
Y_AXIS['medicago_rma'] = "RMA expression signal"

#Check if lookup exists
LOOKUP = {}
LOOKUP['medicago_mas'] = 1
LOOKUP['medicago_rma'] = 1

# initial gene ids when start page is loaded
GENE_ID_DEFAULT1 = 'Msa.1002.1.S1_at'
GENE_ID_DEFAULT2 = 'Mtr.9961.1.S1_at'

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
GRAPH_SCALE_UNIT["medicago_mas"] = [(1000, 0.029), (100000, 0.0029)]
GRAPH_SCALE_UNIT["medicago_rma"] = [(1000, 3.5)]

# define additional header text for individual data sources
# you can use key 'default' for each not individually defined
datasourceHeader = {}
datasourceHeader['default'] = ''

# define additional footer text for individual data sources
# you can use key 'default' for each not individually defined
datasourceFooter = {}
datasourceFooter['default'] = ''

# regular expression for check of gene id input (here agi and probeset id allowed)
inputRegEx = "(Medtr\d{1}g\d{6})|(^AC)|(Mtr.\d{4,5}.1.(S1|S1_x|s1|s1_x)_at)|((AFFX-(Bio|Cre|Dap|Lys|Phe|Thr|Trpn)(B|C|Dn|X)-(3|5|M)_at))|(AFFX-(Msa|Mtr)-(actin|gapc|gsta|ubq11|TrpnX)-(3|5|M)_(at|x_at|s_at))|((AFFX-Mtr|AFFX)-r2-(Bs|Ec|P1)-(cre|dap|lys|phe|thr|bioB|bioC|bioD)-(3|5|M)_(at|s_at|x_at))|(AFFX-Mtr-ubq11-(3|5|M)_(at|s_at|x_at))|(AFFX-r2-Tag([A-Z]{1,2})(_at|-3_at|-5_at|-M_at))|((Msa|Mtr|Sme)\..*)"

# default thresholds
minThreshold_Compare = 0.6  # Minimum color threshold for comparison is 0.6, giving us [-0.6, 0.6] on the color legend
minThreshold_Relative = 0.6 # Minimum color threshold for median is 0.6, giving us [-0.6, 0.6] on the color legend ~ 1.5-Fold
minThreshold_Absolute = 10  # Minimum color threshold for max is 10, giving us [0, 10] on the color legend

# coordinates where to write gene id, probeset id and gene alias into image
GENE_ID1_POS = (10, 28)
GENE_ID2_POS = (220, 28)
GENE_PROBESET1_POS = (120, 28)
GENE_PROBESET2_POS = (350, 28)
GENE_ALIAS1_POS = (0, 0)
GENE_ALIAS2_POS = (0, 0)


defaultDataSource = 'medicago_mas'
dataDir = 'data_medicago'
dbGroupDefault = 'group1'


# list of datasources in same group to find max signal 
groupDatasource = {}
groupDatasource["group1"] = ['medicago_mas', 'medicago_rma']

# mapping of xml files to show datasource name
groupDatasourceName = {}
groupDatasourceName["group1"] = {'medicago_mas':'Medicago mas', 'medicago_rma':'Medicago rma'}

# ortholog configuration
# list of species where orthologs should be tried to retrieve (names must be the same as in ortholog db)
ortholog_species = ('POP', 'TAIR8', 'MEDV3', 'RICE', 'BARLEY') #'SOYBEAN'

efpLink = {}
efpLink['POP'] = "http://bar.utoronto.ca/efppop/cgi-bin/efpWeb.cgi?dataSource=Poplar&primaryGene=%s&modeInput=Absolute"
efpLink['TAIR8'] = "http://bar.utoronto.ca/~rpatel/arabidopsis_test_rohan/cgi-bin/efpWeb.cgi?dataSource=Developmental_Map&primaryGene=%s&modeInput=Absolute"
efpLink['MEDV3'] = "http://bar.utoronto.ca/efpmedicago/cgi-bin/efpWeb.cgi?dataSource=medicago_mas&primaryGene=%s&modeInput=Absolute"
efpLink['SOYBEAN'] = "http://bar.utoronto.ca/efpsoybean/cgi-bin/efpWeb.cgi?dataSource=soybean&primaryGene=%s&modeInput=Absolute"
efpLink['RICE'] = "http://bar.utoronto.ca/efprice/cgi-bin/efpWeb.cgi?dataSource=rice_mas&primaryGene=%s&modeInput=Absolute"
efpLink['BARLEY'] = "http://bar.utoronto.ca/efpbarley/cgi-bin/efpWeb.cgi?dataSource=barley_mas&primaryGene=%s&modeInput=Absolute"

species = 'MEDV3'

spec_names = {}
spec_names['POP'] = 'Poplar'
spec_names['TAIR8'] = 'Arabidopsis'
spec_names['MEDV3'] = 'Medicago'
spec_names['SOYBEAN'] = 'Soybean'
spec_names['RICE'] = 'Rice'
spec_names['BARLEY'] = 'Barley'

