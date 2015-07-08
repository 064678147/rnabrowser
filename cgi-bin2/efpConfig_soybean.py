'''
Created on Nov 24, 2009

@author: rtbreit
'''

DB_HOST = 'localhost'           # hostname of MySQL database server
DB_USER = 'efp_user'            # username for database access
DB_PASSWD = 'efp_user'          # password for database access
DB_ANNO = 'soybean_annotations_lookup'  # database name for annotations lookup
DB_ORTHO = 'ortholog_db'		# ortholog DB

# lookup table for gene annotation
DB_ANNO_TABLE = 'gmax_annotation'
DB_ANNO_GENEID_COL = 'gmax'

# lookup table for probeset id
DB_LOOKUP_TABLE = None
DB_LOOKUP_GENEID_COL = None

# lookup tables for ncbi ids
DB_NCBI_GENE_TABLE = None
DB_NCBI_PROT_TABLE = None
DB_NCBI_GENEID_COL = None

#Check Y-AXIS message
Y_AXIS = {}
Y_AXIS['soybean'] = "RPKM expression signal"
Y_AXIS['soybean_severin'] = "RPKM expression signal"


#Check if lookup exists
LOOKUP = {}

# initial gene ids when start page is loaded
GENE_ID_DEFAULT1 = 'Glyma06g47400'
GENE_ID_DEFAULT2 = 'Glyma06g47390'

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
#GRAPH_SCALE_UNIT["default"] = [(10, 5), (100, 0.5), (1000, 0.05), (10000, 0.005)]
GRAPH_SCALE_UNIT["soybean"] = [(10, 5), (100, 0.5), (1000, 0.05), (10000, 0.005)]
GRAPH_SCALE_UNIT["soybean_severin"] = [(10, 3), (100, 0.3), (1000, 0.03), (10000, 0.003), (100000, 0.0003)]

# define additional header text for individual data sources
# you can use key 'default' for each not individually defined
datasourceHeader = {}
datasourceHeader['default'] = ''

# define additional footer text for individual data sources
# you can use key 'default' for each not individually defined
datasourceFooter = {}
datasourceFooter['default'] = ''

# regular expression for check of gene id input
inputRegEx = "(^Glyma)"

# default thresholds
minThreshold_Compare = 0.6  # Minimum color threshold for comparison is 0.6, giving us [-0.6, 0.6] on the color legend
minThreshold_Relative = 0.6 # Minimum color threshold for median is 0.6, giving us [-0.6, 0.6] on the color legend ~ 1.5-Fold
minThreshold_Absolute = 10  # Minimum color threshold for max is 10, giving us [0, 10] on the color legend

# coordinates where to write gene id, probeset id and gene alias into image
GENE_ID1_POS = (100, 30)
GENE_ID2_POS = (370, 30)
GENE_PROBESET1_POS = (250, 30)
GENE_PROBESET2_POS = (490, 30)
GENE_ALIAS1_POS = (0, 0)
GENE_ALIAS2_POS = (0, 0)

defaultDataSource = 'soybean'
dataDir = 'data_soybean'

dbGroupDefault = 'group1'
# list of datasources in same group to find max signal 
groupDatasource = {}
groupDatasource["group1"] = ['soybean', 'soybean_severin']

# mapping of xml files to show datasource name
groupDatasourceName = {}
groupDatasourceName["group1"] = {'soybean':'Soybean', 'soybean_severin':'soybean_severin'}

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

species = 'SOYBEAN'

spec_names = {}
spec_names['POP'] = 'Poplar'
spec_names['TAIR8'] = 'Arabidopsis'
spec_names['MEDV3'] = 'Medicago'
spec_names['SOYBEAN'] = 'Soybean'
spec_names['RICE'] = 'Rice'
spec_names['BARLEY'] = 'Barley'
