'''
Created on Nov 24, 2009

@author: rtbreit
'''

DB_HOST = 'localhost'           # hostname of MySQL database server
DB_USER = 'efp_user'            # username for database access
DB_PASSWD = 'efp_user'          # password for database access
DB_ANNO = 'barley_annotations_lookup'  # database name for annotations lookup
DB_ORTHO = 'ortholog_db'		# ortholog DB

# lookup table for gene annotation
DB_ANNO_TABLE = 'bar_annotation'
DB_ANNO_GENEID_COL = 'bar'

# lookup table for probeset id
DB_LOOKUP_TABLE = 'at_bar_lookup'
DB_LOOKUP_GENEID_COL = 'bar'

# lookup tables for ncbi ids
DB_NCBI_GENE_TABLE = None
DB_NCBI_PROT_TABLE = None
DB_NCBI_GENEID_COL = None

#Check Y-AXIS message
Y_AXIS = {}
Y_AXIS['barley_mas'] = "GCOS expression signal (TGT=100, Bkg=20)"
Y_AXIS['barley_rma'] = "RMA expression signal"

#Check if lookup exists
LOOKUP = {}
LOOKUP['barley_mas'] = 1
LOOKUP['barley_rma'] = 1

# initial gene ids when start page is loaded
GENE_ID_DEFAULT1 = 'Contig3045_at'
GENE_ID_DEFAULT2 = 'Contig19242_at'

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
GRAPH_SCALE_UNIT["barley_mas"] = [(1000, 0.06), (100000, 0.006)]
GRAPH_SCALE_UNIT["barley_rma"] = [(1000, 3.5)]

# define additional header text for individual data sources
# you can use key 'default' for each not individually defined
datasourceHeader = {}
datasourceHeader['default'] = ''

# define additional footer text for individual data sources
# you can use key 'default' for each not individually defined
datasourceFooter = {}
datasourceFooter['default'] = ''

# regular expression for check of gene id input (here agi and probeset id allowed)
inputRegEx = "((^(HM|HV).*)|(^HV.*_at)|([0-9]{4,7})_(Reg|R)_([0-9]{2,4})-([0-9]{4})_at)|([0-9]{4,5}\.AF[0-9]{5}(_|_x_)at)|(A[0-9]{5}\.[0-9]{1}(_|_x_|_s_)at)|(([A-Z]{2}[0-9]{6}|[A-Z]{2}[0-9]{6}\.1)(_|_x_|_s_|_CDS-[0-9]{1,2}_|_CDS-[0-9]{1,2}_s_)at)|(AFFX-(BioB|BioC|BioDn|CreX|DapX|LysX|PheX|ThrX|TrpnX)-(3|5|M)_at)|(AFFX-r2-(Bs|Ec|P1)-(dap|lys|phe|thr|bioB|bioC|bioD|cre)-(3|5|M)(_|_x_|_s_)at)|(ChlorContig[0-9]{1,2}(_|_x_|_s_)at)|(((MitoContig|Contig)[0-9]{1,6})(_|_x_|_s_)at)|(D[0-9]{5}_at)|(Dhn[0-9]{2}\(Morex\)(_|_s_)at)|(E(Ban|Bca|Bed|Bem|Bes|Bma|Bpi|Bro)[0-9]{2}_SQ[0-9]{3}_[A-Z]{1}[0-9]{2}(_|_s_|_x_)at)|(Franka(_|_b_)3pri[0-9]{1,2}(_|_s_|_x_)at)|(H[A-Z]{1}[0-9]{1-4}[A-Z]{1}[0-9]{1,2}[a-z]{1}(_|_x_|_s_)at)|(HVSME[a-z]{1}[0-9]{4}[A-Z]{1}[0-9]{2}(r2|f)(_|_x_|_s_)at)|(HV_CEa[0-9]{4}[A-Z]{1}[0-9]{2}(r2|f)(_|_x_|_s_)at)|(H[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{2}r(_|_x_|_s_)at)|(Mla([0-9]{1,2}|[0-9]{1,2}DH)(_orf_|_div5_|_5pri_|_5pri-|_consrvd_|_3pri12_)(3pri12|3pr|UTR_intron2|UTR_intron1|5pri_end)(_|_x_|_s_)at)|((Mla|Mlk)(_div5|_3pri12)(_|_x_|_s__at))|(S[0-9]{10}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{1}(_|_x_|_s_)at)|((b|rb)(aak|aal|ags|ah|asd)[0-9]{1,2}[a-z]{1}[0-9]{2}(_|_x_|_s_)at)|(([0-9]{4,7})_(Reg|R)_([0-9]{2,4})-([0-9]{4}))|([0-9]{4,5}\.AF[0-9]{5})|(A[0-9]{5}\.[0-9]{1})|([A-Z]{2}[0-9]{6}|[A-Z]{2}[0-9]{6}\.1)|(AFFX-(BioB|BioC|BioDn|CreX|DapX|LysX|PheX|ThrX|TrpnX))|(AFFX-r2-(Bs|Ec|P1)-(dap|lys|phe|thr|bioB|bioC|bioD|cre))|(ChlorContig[0-9]{1,2})|((MitoContig|Contig)[0-9]{1,6})|(D[0-9]{5})|(Dhn[0-9]{2}\(Morex\))|(E(Ban|Bca|Bed|Bem|Bes|Bma|Bpi|Bro)[0-9]{2}_SQ[0-9]{3}_[A-Z]{1}[0-9]{2})|(Franka(_|_b_)3pri[0-9]{1,2})|(H[A-Z]{1}[0-9]{1-4}[A-Z]{1}[0-9]{1,2}[a-z]{1})|(HVSME[a-z]{1}[0-9]{4}[A-Z]{1}[0-9]{2}(r2|f))|(HV_CEa[0-9]{4}[A-Z]{1}[0-9]{2}(r2|f))|(H[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{2}r)|(Mla([0-9]{1,2}|[0-9]{1,2}DH)(_orf_|_div5_|_5pri_|_5pri-|_consrvd_|_3pri12_)(3pri12|3pr|UTR_intron2|UTR_intron1|5pri_end))|((Mla|Mlk)(_div5|_3pri12))|(S[0-9]{10}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{1})|((b|rb)(aak|aal|ags|ah|asd)[0-9]{1,2}[a-z]{1}[0-9]{2}|(^(HO))"

# default thresholds
minThreshold_Compare = 0.6  # Minimum color threshold for comparison is 0.6, giving us [-0.6, 0.6] on the color legend
minThreshold_Relative = 0.6 # Minimum color threshold for median is 0.6, giving us [-0.6, 0.6] on the color legend ~ 1.5-Fold
minThreshold_Absolute = 10  # Minimum color threshold for max is 10, giving us [0, 10] on the color legend

# coordinates where to write gene id, probeset id and gene alias into image
GENE_ID1_POS = (150, 30)
GENE_ID2_POS = (150, 60)
GENE_PROBESET1_POS = (150, 45)
GENE_PROBESET2_POS = (150, 75)
GENE_ALIAS1_POS = (0, 0)
GENE_ALIAS2_POS = (0, 0)

defaultDataSource = 'barley_mas'
dataDir = 'data_barley'
dbGroupDefault = 'group1'


# list of datasources in same group to find max signal 
groupDatasource = {}
groupDatasource["group1"] = ['barley_mas', 'barley_rma']

# mapping of xml files to show datasource name
groupDatasourceName = {}
groupDatasourceName["group1"] = {'barley_mas':'Barley mas', 'barley_rma':'Barley rma'}

# ortholog configuration
# list of species where orthologs should be tried to retrieve (names must be the same as in ortholog db)
ortholog_species = ('POP', 'TAIR8', 'MEDV3', 'RICE', 'BARLEY') #'SOYBEAN'

efpLink = {}
efpLink['POP'] = "http://bar.utoronto.ca/efppop/cgi-bin/efpWeb.cgi?dataSource=Poplar&primaryGene=%s&modeInput=Absolute"
efpLink['TAIR8'] = "http://bar.utoronto.ca/~rpatel/arabidopsis_test_rohan/cgi-bin/efpWeb.cgi?dataSource=Developmental_Map&primaryGene=%s&modeInput=Absolute"
efpLink['MEDV3'] = "http://bar.utoronto.ca/efpmedicago/cgi-bin/efpWeb.cgi?dataSource=medicago_mas&primaryGene=%s&modeInput=Absolute"
#efpLink['SOYBEAN'] = "http://bar.utoronto.ca/efpsoybean/cgi-bin/efpWeb.cgi?dataSource=soybean&primaryGene=%s&modeInput=Absolute"
efpLink['RICE'] = "http://bar.utoronto.ca/efprice/cgi-bin/efpWeb.cgi?dataSource=rice_mas&primaryGene=%s&modeInput=Absolute"
efpLink['BARLEY'] = "http://bar.utoronto.ca/efpbarley/cgi-bin/efpWeb.cgi?dataSource=barley_mas&primaryGene=%s&modeInput=Absolute"

species = 'BARLEY'

spec_names = {}
spec_names['POP'] = 'Poplar'
spec_names['TAIR8'] = 'Arabidopsis'
spec_names['MEDV3'] = 'Medicago'
#spec_names['SOYBEAN'] = 'Soybean'
spec_names['RICE'] = 'Rice'
spec_names['BARLEY'] = 'Barley'


