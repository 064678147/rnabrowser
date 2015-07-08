#!/usr/bin/python
#clean up code (useThresholdFlag is nonsensical)
#fix views, etc.
import os
import cgi
import tempfile
import string
import efp, efpXML, efpConfig, efpService, efpDb
import re
import operator
# Asher
import SecurityCheck

#testing_efp = open("output/testing_efpWeb.txt", "w")
form = cgi.FieldStorage(keep_blank_values=1)

error = 0
errorStrings = []
alertStrings = []
testalertStrings = []
orthologStrings = {}
alignOrthologs = {}
lowAlert = 0
sdAlert = 0
maxdict = {}


img = None
imgMap = {}
imgFilename = {}
tableFile = {}
views = []

#CGI_INPUTS = {
   #dataSource: "dataSource",
   #primaryGene: "primaryGene",
   #secondaryGene: "secondaryGene",
   #mode: "modeInput",
   #useThreshold: "override",
   #grey_low: "modeMask_low",
   #grey_stddev: "modeMask_stddev",
   #primaryProbeset: "primaryProbeset",
   #secondaryProbeset: "secondaryProbeset",
#}
# Retrieve cgi inputs
dataSource    = form.getvalue("dataSource")
primaryGene   = form.getvalue("primaryGene")
secondaryGene = form.getvalue("secondaryGene")
thresholdIn   = form.getvalue("threshold")
mode          = form.getvalue("modeInput")
useThreshold  = form.getvalue("override")
grey_low      = form.getvalue("modeMask_low")
grey_stddev   = form.getvalue("modeMask_stddev")
#orthoListOn   = form.getvalue("orthoListOn")
ncbi_gi	      = form.getvalue("ncbi_gi")
primaryProbeset   = form.getvalue("primaryProbeset")
secondaryProbeset = form.getvalue("secondaryProbeset")
gene_alias1    = form.getvalue("gene_alias1")
gene_alias2    = form.getvalue("gene_alias2")
agi1_preselected = form.getvalue("agi1")
agi2_preselected = form.getvalue("agi2")
webservice_gene1 = None
webservice_gene2 = None
gene1 = None


# Asher
for key in form:
   SecurityCheck.checkXSS(form[key].value)

# Default gene id
if primaryGene == None:
   if ncbi_gi != None:
      primaryGene = ncbi_gi
      errorStr = 'The requested NCBI gi "%s" doesn\'t correspond to a given AGI.<br>' % ncbi_gi
      errorStrings.append(errorStr)
   else:
      primaryGene = efpConfig.GENE_ID_DEFAULT1
if secondaryGene == None:
   secondaryGene = efpConfig.GENE_ID_DEFAULT2

primaryGene = primaryGene.strip()
secondaryGene = secondaryGene.strip()

#for item in [useThreshold, gene_alias1, gene_alias2]:
   #if item != 'on':
      #item == None
if useThreshold == "" or useThreshold == "None":
   useThreshold = None

if (gene_alias1 == "" or gene_alias1 == "None"):
   gene_alias1 = None
if (gene_alias2 == "" or gene_alias2 == "None"):
   gene_alias2 = None

# set orthoListOn to off
orthoListOn = "0"

# Try Entered Threshold; if fails or threshold not checked use default threshold
if useThreshold != None:
   try:
      threshold = float(thresholdIn) # Convert str to float
   except:
      # Threshold string was malformed
      error = 1
      errorStr = 'Invalid Threshold Value "%s"<br>' % thresholdIn
      errorStrings.append(errorStr)
      useThreshold = None
if useThreshold == None and thresholdIn == None:
   # assign a default value for first calls
   if mode == "Relative" or mode == "Compare":
      threshold = 2.0
   else:	#Absolute or none
      threshold = 500
   firstCall = 1
else:
   threshold = float(thresholdIn)
   firstCall = 0

if dataSource == None:
   dataSource = efpConfig.defaultDataSource
# Serialize data from XML file into a Specimen object
spec = efp.Specimen()
xmlName = "%s/%s.xml" % (efpConfig.dataDir, dataSource)
spec.load(xmlName)


# Right now the browser only has one view - "all"
# In the future, there should be a drop down menu letting users
# choose multiple views

defaultImgFilename = "%s/%s_image.png" % (efpConfig.dataDir, dataSource)
if mode == None:
   # If no mode is selected (99% of the time this means the user just arrived
   # at the page), just show them a color map
   # Set Developmental_Map as default DataSource
   if dataSource == None:
      dataSource = efpConfig.defaultDataSource

else:  
#if mode != None:  #None means just arrived       
###-----------------------------------"all" view-------------------------------------------------------------------------------------------------------------------------------
   for name, view in spec.getViews().iteritems():
      if (dataSource == "Developmental_Map_At-TAX" or dataSource == "Abiotic_Stress_At-TAX"):
         AtTAX = 1
      else:
         AtTAX = 0

      if AtTAX == 1:
         if name == 'Tiling':
            result = efpDb.checkAtTAX(primaryGene)
            if (result == None):
               error = 1
               errorStrings.append("Primary AtTAX gene not found.")
            else:
               primaryGene = result
         if mode == 'Compare' and name == 'Tiling':
            result = efpDb.checkAtTAX(secondaryGene)
            if (result == None):
               error = 1
               errorStrings.append("Secondary AtTAX gene not found.")
            else:
               secondaryGene = result
         if name == 'ATH1':
            result = efpDb.checkATH1(primaryGene)
            if (result == None):
               continue
            else: 
               primaryGene = result
         if mode == 'Compare' and name == 'ATH1':
            result = efpDb.checkATH1(secondaryGene)
            if (result == None):
               continue
            else:
               secondaryGene = result

      # If either of these probe IDs are None (bad inputs), then we just
      # spit out the default image again


      gene1 = view.createGene(primaryGene, probesetId=primaryProbeset, geneAlias=gene_alias1)
      g1 = gene1
      if (agi1_preselected is not None):
         if (len(agi1_preselected) != 0):
            gene1.geneId = agi1_preselected
      gene2 = view.createGene(secondaryGene, probesetId=secondaryProbeset, geneAlias=gene_alias2)
      if (agi2_preselected is not None):
         if (len(agi2_preselected) != 0):
            gene2.geneId = agi2_preselected
      gene1.setQueryGene(primaryGene)
      gene2.setQueryGene(secondaryGene)
      if AtTAX == 1 and name == 'Tiling':
         gene1.setAtTAXId(primaryGene)
      if AtTAX == 1 and mode == 'Compare' and name == 'Tiling':
         gene2.setAtTAXId(secondaryGene)
      gene1 = view.alterGene(gene1)
      gene2 = view.alterGene(gene2)
      webservice_gene1 = view.alterWebserviceGene(gene1)
      webservice_gene2 = view.alterWebserviceGene(gene2)
      if AtTAX == 0 and (gene1.getGeneId() is None or gene1.getProbeSetId() is None):
         if (gene1.getAlias() is not None):
            errorStr = 'The requested Primary gene / probeset ID "%s" for gene alias "%s" cannot be found in %s datasource. Try the At-TAX datasources.' % (gene1.getGeneId(), gene1.getAlias(), view.dbGroup)
         else:
            errorStr = 'The requested Primary gene / probeset ID "%s" cannot be found in %s datasource. Try the At-TAX datasources. ' % (primaryGene, view.dbGroup)
         error = 1
         errorStrings.append(errorStr)
      elif AtTAX == 0 and (mode == 'Compare' and gene2.probesetId is None):
         if (gene2.getAlias() is not None):
            errorStr = 'The requested Secondary gene / probeset ID "%s" for gene alias "%s" cannot be found in %s datasource Try the At-TAX datasources. <br>' % (gene2.getGeneId(), gene2.getAlias(), view.dbGroup)
         else:      
            errorStr = 'The requested Secondary gene / probeset ID "%s" cannot be found in %s datasource. Try the At-TAX datasources. <br>' % (secondaryGene, view.dbGroup)
         error = 1
         errorStrings.append(errorStr)
      elif primaryGene == secondaryGene and mode == 'Compare':
         error = 1
         errorStr = 'The requested Secondary gene / probeset ID "%s" must be different than the Primary ID<br>' % secondaryGene
         errorStrings.append(errorStr)
         viewMaxSignal = 2.0
      else:
         if mode == 'Absolute':
            if useThreshold:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2,sdAlert) = view.renderAbsolute(gene1, threshold, grey_mask=grey_stddev)
            else:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2,sdAlert) = view.renderAbsolute(gene1, grey_mask=grey_stddev)
               
         elif mode == 'Relative':
            if useThreshold:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2,lowAlert) = view.renderRelative(gene1, threshold, grey_mask=grey_low)
            else:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2,lowAlert) = view.renderRelative(gene1, grey_mask=grey_low)
         elif mode == 'Compare':    
            if useThreshold:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2) = view.renderComparison(gene1, gene2, threshold)
            else:
               (img,viewMaxSignal,viewMaxSignal1,viewMaxSignal2) = view.renderComparison(gene1, gene2)
         # find the max signal across all datasources and provide a link to that datasource
         if AtTAX == 1 and name == 'Tiling':
            maxSignalInDatasource = 0
            maxDatasource = "None"
         else:
            (maxSignalInDatasource, maxDatasource) = view.getMaxInDatasource(gene1)

         maxSignalInDatasource = round(maxSignalInDatasource,2)

         # maxDatasource = re.sub("_"," ", maxDatasource)
         #if maxSignalInDatasource == 0 and maxDatasource == "None":
            #pass
         #else:
            #alertStr = "For %s data, this probe set reaches its maximum expression level (expression potential) of <b>%s</b> in the <b>%s</b> data source." % (view.dbGroup, maxSignalInDatasource, maxDatasource)
            #alertStrings.append(alertStr)
            
         maxdict = view.getMaxInDatasourceDict(gene1)
         # alert the user that the scale has changed if no threshold is set
         if useThreshold == None and firstCall != 1:
            if viewMaxSignal != threshold:
               alertStr = ""
            else:
               useThresholdFlag = "on"
               thresholdLevelSuggested = maxSignalInDatasource
               if mode == 'Relative':
                  thresholdLevelSuggested = 4
               if mode == 'Compare':
                  thresholdLevelSuggested = 4
               alertStr = "For %s data, note the maximum signal value has increased to %s from %s. Use the <a href='efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s'>Signal Threshold option to keep it constant at %s</a>, or enter a value in the Signal Threshold box, such as <a href='efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s'>%s</a>. The same colour scheme will then be applied across all views.<br>" % (view.dbGroup, viewMaxSignal, threshold, dataSource, mode, gene1.geneId, gene2.geneId, useThresholdFlag, threshold, grey_low, grey_stddev, threshold, dataSource, mode, gene1.geneId, gene2.geneId, useThresholdFlag, thresholdLevelSuggested, grey_low, grey_stddev, thresholdLevelSuggested)
               alertStrings.append(alertStr)
            threshold = viewMaxSignal
         elif useThreshold == None and firstCall == 1:
            threshold = viewMaxSignal

         # alert the user if SD filter or low filter should be activated
         if grey_stddev != "on" and sdAlert == 1 and mode == 'Absolute':
            grey_stddev_flag = "on"
            if useThreshold == None:
               useThreshold = ""
            alertStr = "Some samples exhibit high standard deviations for replicates. You can use <a href='efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s'>standard deviation filtering</a> to mask those with a deviation greater than half their expression value.<br>" % (dataSource, mode, gene1.geneId, gene2.geneId, useThreshold, threshold, grey_low, grey_stddev_flag)
            alertStrings.append(alertStr)
         # alert the user if SD filter or low filter should be activated
         if grey_low != "on" and lowAlert == 1 and mode == 'Relative':
            grey_low_flag = "on"
            if useThreshold == None:
               useThreshold = ""
            alertStr = "Some sample ratios were calculated with low values that exhibit higher variation, potentially leading to ratios that are not a good reflection of the biology. You can <a href='efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s'>low filter below 20 units</a> to mask these.<br>" % (dataSource, mode, gene1.geneId, gene2.geneId, useThreshold, threshold, grey_low_flag, grey_stddev)
            alertStrings.append(alertStr)

         # Otherwise, we render and display the option

         imgMap[view.name] = view.getImageMap(mode, gene1, gene2, useThreshold, threshold, dataSource, grey_low, grey_stddev)
      if img != None:
         imgFilename[view.name] = view.drawImage(mode, maxSignalInDatasource, viewMaxSignal1, viewMaxSignal2, gene1, gene2, img)
         #Create a table of Expression Values and save it in a temporary file
         expTable = view.table
         tableFile[view.name] = tempfile.mkstemp(suffix='.html', prefix='efp-', dir='output')
         os.system("chmod 644 " + tableFile[view.name][1])
         tf = open(tableFile[view.name][1], 'w')
         tf.write(expTable)
         tf.close()
         chartFile = tableFile[view.name][1].replace(".html", ".png")
         view.saveChart(chartFile, mode)
         views.append(view.name)

###-------------------------------------------------------HTML codes----------------------------------------------------------------------------------------------------------------------

print 'Content-Type: text/html\n'
print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
print '<html>'
print '<head>'
print '  <title>%s eFP Browser</title>' % efpConfig.spec_names[efpConfig.species]
print '  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">'
print '  <meta name="keywords" content="%s, genomics, expression profiling, mRNA-seq, Affymetrix, microarray, protein-protein interactions, protein structure, polymorphism, subcellular localization, proteomics, poplar, rice, Medicago, barley, transcriptomics, proteomics, bioinformatics, data analysis, data visualization, AtGenExpress, PopGenExpress, cis-element prediction, coexpression analysis, Venn selection, molecular biology">' % efpConfig.spec_names[efpConfig.species]
print '  <link rel="stylesheet" type="text/css" href="efp.css"/>'
print '  <link rel="stylesheet" type="text/css" href="domcollapse.css"/>'
print '  <link rel="stylesheet" type="text/css" href="jquery-ui.css">'
print '  <link rel="stylesheet" type="text/css" href="jquery-1.8.3.js">'
print '  <link rel="stylesheet" type="text/css" href="jquery-ui.js">'
print '  <script src="jquery.min.js"></script>'
print '  <script src="jquery-ui.min.js"></script>'
print '  <script>'
print '		jQuery(function() {'
print '             	        jQuery("#g1").autocomplete({'
print '		                source: "get_alias.pl",'
print '                		minLength: 2,'
print '		                select: function(event, ui) {'
print '                		    $("#g1").val(ui.item.label);'
print '				    $("#agi1").val(ui.item.id);'
print '                		}'
print '        		});'
print '             	        jQuery("#g2").autocomplete({'
print '		                source: "get_alias.pl",'
print '                		minLength: 2,'
print '		                select: function(event, ui) {'
print '                		    $("#g2").val(ui.item.label);'
print '				    $("#agi2").val(ui.item.id);'
print '                		}'
print '        		});'

print '		 });'
print '</script>'

print '<script>'
print ' 	jQuery(document).ready(function() {'
print '			jQuery("#go").on("click", function() {'
print '				var geneName1 = jQuery("#g1").val();'
print '				var geneName2 = jQuery("#g2").val();'
print '				var modeInput = jQuery("#modeInput").val();'
print '				geneName_exists(geneName1, geneName2, modeInput, function(data){});'
print '			});'

print '			function geneName_exists(geneName1, geneName2, mode, callback) {'
print '				var inputVal = jQuery("#g1").val();'
print '				var regex = "%s";' % efpConfig.inputRegEx
print '				$.ajax({'
print '					url: "check_alias.pl",'
print '					data: { "gene1" : geneName1, "gene2" : geneName2, "modeInput" : mode },'
print '					type: "post",'
print '					dataType: "json",'
print '					success: function(data) {'
print '						callback(data);'
print '						if (data == 1) {'
print '							if (!(geneName1.match(regex)))'
print '							{'
print '								$("#gene_alias1").val(geneName1);'
print '							}'
print '							if ( (mode == "Compare") && (!(geneName2.match(regex))))' 
print '							{'
print '								$("#gene_alias2").val(geneName2);'
print '							}'
print '							jQuery("#efpForm").submit();'
print '						}'
print '						else if ( (data == 0) && (geneName1.match(regex)))'
print '						{'
print '							jQuery("#efpForm").submit();'
print '						}'
print '						else{'
print '							alert("Invalid Gene Name/Alias");'
print '							return false;'
print '						}'
print '					}'
print '				}).error(function() {'
print '					alert("An error has occurred");'
print '				});'
print '				return false;'
print '			}'
print '		});'
print '</script>'

print '  <script type="text/javascript" src="efp.js"></script>'
print '  <script type="text/javascript">'
print '    regId = /%s/i;' % efpConfig.inputRegEx
print '  </script>'
print '  <script type="text/javascript" src="domcollapse.js"></script>'
print '    <script type="text/javascript" src="popup.js"></script>'
print '</head>'

print '<body><form action="efpWeb.cgi" name="efpForm" id="efpForm" method="POST">'
print '<table width="1000" border="0" align="center" cellspacing="1" cellpadding="0">'
print '<tr><td>'
print '<tr><td><div style="position:relative;"><iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.facebook.com%2Fpages%2FBio-Array-Resource%2F110947168947400&amp;layout=button_count&amp;show_faces=false&amp;width=220&amp;action=like&amp;font&amp;colorscheme=light&amp;height=21" scrolling="no" frameborder="0" style="position:absolute; border:none; overflow:hidden; right:0px; width:100px; height:21px; top:22px;"allowTransparency="true">&nbsp;</iframe></div>'
print "<h1><a href='http://bar.utoronto.ca'><img src='http://bar.utoronto.ca/bbc_logo_small.gif' alt='To the Bio-Analytic Resource Homepage' border=0 align=absmiddle></a>&nbsp;<img src='http://bar.utoronto.ca/bar_logo.gif' alt='The Bio-Analytic Resource' border=0 align=absmiddle>&nbsp;<img src='http://bar.utoronto.ca/images/eFP_logo_large.png' align=absmiddle border=0>&nbsp;%s eFP Browser" % efpConfig.spec_names[efpConfig.species]
print "<br><img src='http://bar.utoronto.ca/images/green_line.gif' width=98% alt='' height='6px' border=0></h1>"

print '</td></tr>'
print '<tr><td align="middle">'
print '    <table>'
print '      <tr align = "center"><th>Data Source</th>'
print '      <th>Mode'
print '<input type="checkbox" name="modeMask_stddev" title="In Absolute Mode, check to mask samples that exhibit a standard deviation of more than 50 percent of the signal value" '
if grey_stddev == "on":
   print 'checked'
print ' value="on" />'
print '<input type="checkbox" name="modeMask_low" title="In Relative Mode, check to mask the use of low expression values in ratio calculations" '
if grey_low == "on":
   print 'checked'
print ' value="on" />'
print '</th><th>Primary Gene ID</th><th>Secondary Gene ID</th>'
print '      <th id="t1">Signal Threshold<input type="checkbox" name="override" title="Check to enable threshold" onclick="checkboxClicked(this.form)" '
if useThreshold == "on":
   print 'checked'
print       ' value="on" />'
print '</th><th></th></tr>'
print '      <tr><td>'

# Help Link
print '      <img src="http://bar.utoronto.ca/affydb/help.gif" border=0 align="top" alt="Click here for instructions in a new window" onClick="HelpWin = window.open(\'http://bar.utoronto.ca/affydb/BAR_instructions.html#efp\', \'HelpWindow\', \'width=600,height=300,scrollbars,resizable=yes\'); HelpWin.focus();">&nbsp;'

# Build drop down list of Data Sources
if mode == None:
   print '<select name="dataSource" onchange="location.href=\'efpWeb.cgi?dataSource=\' + this.options[this.selectedIndex].value ;">'
elif useThreshold == None:
   thresholdSwitch = ""
   print '      <select name="dataSource" onchange="location.href=\'efpWeb.cgi?dataSource=\' + this.options[this.selectedIndex].value + \'&modeInput=%s&primaryGene=%s&secondaryGene=%s&primaryProbeset=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s&gene_alias1=%s&gene_alias2=%s&agi1=%s&agi2=%s\' ;">' %(mode, primaryGene, secondaryGene, gene1.getProbeSetId(), thresholdSwitch, threshold, grey_low, grey_stddev, gene1.getAlias(), gene2.getAlias(), agi1_preselected, agi2_preselected)
else:
   print '      <select name="dataSource" onchange="location.href=\'efpWeb.cgi?dataSource=\' + this.options[this.selectedIndex].value + \'&modeInput=%s&primaryGene=%s&secondaryGene=%s&primaryProbeset=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s&gene_alias1=%s&gene_alias2=%s&agi1=%s&agi2=%s\' ;">' %(mode, primaryGene, secondaryGene, gene1.getProbeSetId(), useThreshold, threshold, grey_low, grey_stddev, gene1.getAlias(), gene2.getAlias(), agi1_preselected, agi2_preselected)

xML = efpXML.findXML(efpConfig.dataDir)
for x in sorted(xML):
   print '    <option value="%s"' % x
   # To preserve modes between form submits
   if dataSource == x:
      print 'selected'
   xText = string.replace(x,'_',' ')
   print '>%s</option>' % xText
print '      </select></td>'
# xML = None
# reload(efpXML)

# Build drop down list of modes
if mode == None:
   print '      <td><select selected="Absolute" name="modeInput" id="modeInput" onchange="changeMode(this.form)">' 
else:
   print '		 <td><select selected="Absolute" name="modeInput" id="modeInput" onchange="location.href=\'efpWeb.cgi?dataSource=%s&modeInput=\' + this.options[this.selectedIndex].text + \'&primaryGene=%s&secondaryGene=%s&primaryProbeset=%s&modeMask_low=%s&modeMask_stddev=%s&gene_alias1=%s&gene_alias2=%s&agi1=%s&agi2=%s\' ">' %(dataSource, primaryGene, secondaryGene, gene1.getProbeSetId(), grey_low, grey_stddev, gene1.getAlias(), gene2.getAlias(), agi1_preselected, agi2_preselected)

# Preserve mode between form submits. If the user selected 'Compare' as his/her
# mode, when the page reloads, the list should still have 'Compare' selected.
if mode == 'Relative':
   print '    <option value="Absolute">Absolute</option>'
   print '    <option value="Relative" selected>Relative</option>'
   print '    <option value="Compare">Compare</option>'
elif mode == 'Compare':
   print '    <option value="Absolute">Absolute</option>'
   print '    <option value="Relative">Relative</option>'
   print '    <option value="Compare" selected>Compare</option>'
else: # Default (Absolute)
   print '    <option value="Absolute" selected>Absolute</option>'
   print '    <option value="Relative">Relative</option>'
   print '    <option value="Compare">Compare</option>'

print '      </select></td><td>'
print '      <input type="text" id="g1" name="primaryGene" value="%s" size=17" onkeypress="if (event.keyCode == 13) document.getElementById(\'go\').click()"/></td><td>' % primaryGene
print '	     <input type=hidden name="agi1" id="agi1" value=\"\">'
print '	     <input type=hidden name="agi2" id="agi2" value=\"\">'
print '      <input type="text" id="g2" name="secondaryGene" size=17 value="%s" onkeypress="if (event.keyCode == 13) document.getElementById(\'go\').click()"' % secondaryGene
if mode != 'Compare':
   print 'disabled'
print '      /></td><td>'
print '      <input type="text" id="t0" name="threshold" value="%s" onkeypress="if (event.keyCode == 13) document.getElementById(\'go\').click()"' % threshold
if useThreshold == None: 
   print 'disabled'
print '      /></td>'
print '      <td><input type="button" id="go" type="button" name="Go" value="Go"/></td></tr>'
print '    </table>'
print '    </form>'
print '<div class="testing">'
print '</div>'
print '</td></tr>'
print '<tr><td style="text-align:center">'

if error:
   print '    <ul>'
   for row in errorStrings:
      print '<li class="error">%s</li>' % row
   print '    </ul>'

###----------------------print orthologs-------------------------------------------------------------------------------------------------------------------------------------------------
for spec in orthologStrings:
   if len(orthologStrings[spec]) > 0:
      print '<p class="expanded"> Links to %s Orthologs in %s eFP Browser </p>' % (efpConfig.spec_names[spec], efpConfig.spec_names[spec])

      print '<div>'
      print '    <ul>'

      print '<p>Orthologs have been ranked based on Spearman Correlation Coefficient (SCC) value. Values are given for each ortholog.Note that these rankings are to be used at the users discretion, as expression profiles were compared using limited data points.</p>'

      for row in orthologStrings[spec]:
         print '<li>%s</li>'%row
      print '    </ul>'
      print '</div>'

if len(testalertStrings) > 0:
   print '    <ul>'
   for row in testalertStrings:
      print '<li>%s</li>' % row
   print '    </ul>'

# print additional header text if configured for selected data source
if dataSource in efpConfig.datasourceHeader:
   print '%s' % efpConfig.datasourceHeader[dataSource]
elif 'default' in efpConfig.datasourceHeader:
   print '%s' % efpConfig.datasourceHeader['default']

if len(alertStrings) > 0:
   print '    <ul>'
   for row in alertStrings:
      print '<li>%s</li>' % row
   print '    </ul>'
if mode != None:
   ###----------------------check external services-------------------------------------------------------------------------------------------------------------------------------------------------
   # Serialize services data from XML file into a Info object
   info = efpService.Info()
   if (info.load("%s/efp_info.xml" % efpConfig.dataDir) == None):
      print '<table style="margin-left:auto;margin-right:auto"><tr>'
      for name in (info.getServices()):
         service = info.getService(name)
         external = service.getExternal()
         highlight1 = service.checkService(webservice_gene1.webservice_gene)
         highlight2 = None
         if(mode == 'Compare'):
            highlight2 = service.checkService(webservice_gene2.webservice_gene)
         if highlight1 == 'error' or highlight2 == 'error':
            print '<td><img title="connection error for service %s" width="50" height="50" alt="connection error" src="%s/error.png"></td>'% (name, efpConfig.dataDir)
            continue
         elif (highlight1):
            link = service.getLink(webservice_gene1.webservice_gene, gene1.getProbeSetId())
            gene = webservice_gene1.webservice_gene
         elif (highlight2):
            link = service.getLink(webservice_gene2.webservice_gene, gene2.getProbeSetId())
            gene = webservice_gene1.webservice_gene
         else:
            print '<td><img title="No %s data found" width="50" height="50" alt="No %s data found" style="opacity:0.30;filter:alpha(opacity=30);" src="%s/%s"></td>'%(name, name, efpConfig.dataDir, service.icon)
            continue
         if link:
            if external == "true":
               print '<td><a target="_blank" title="%s gene %s" href="%s"><img width="50" height="50" alt="%s gene %s" src="%s/%s"></a></td>'%(name, gene, link, name, gene, efpConfig.dataDir, service.icon)
            else:
               print '<td><a target="_blank" title="%s for gene %s" href="%s"><img width="50" height="50" alt="%s for gene %s" src="%s/%s"></a></td>'%(name, gene, link, name, gene, efpConfig.dataDir, service.icon)
         else:
            print '<td><img target="_blank" title="%s found for gene %s" width="50" height="50" alt="%s found for %s" src="%s/%s"></td>'%(name, gene, name, gene, efpConfig.dataDir, service.icon)
      print '</tr></table>'
      
#tabular navigation
if len(maxdict.items()) != 0:
   increment = int(255 / len(maxdict.items()))
   nextColour = 255
   tempkey = sorted(maxdict.items(), key=operator.itemgetter(1))
   #determine font colour and hyperlink
   for i in range(len(tempkey)):
      yiq = ((255*299)+(nextColour*587))/1000
      font = 'black' if yiq > 160 else 'white'
      hreflink = '<a style="text-decoration:none;color:%s" href="efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s">' %(font, tempkey[i][0], mode, gene1.geneId, gene2.geneId, useThreshold, threshold, grey_low, grey_stddev)      
      if nextColour < 17:
         tempkey[i] = tempkey[i] + ("0" + str(hex(nextColour)[-1:]), font, hreflink)
      else:
         tempkey[i] = tempkey[i] + (str(hex(nextColour)[-2:]), font, hreflink)
      if nextColour > increment:
         nextColour -= increment
      else:
         nextColour = 0
   repeated_data = {}
   if useThreshold == None:
      useThreshold = ""
   for counter in range(len(tempkey)):
      if tempkey[counter][0] in efpConfig.REPEAT_DATA:
         output = list(tempkey[counter][:])
         output[0] = output[0] + '_II'
         output[4] = '<a style="text-decoration:none;color:%s" href="efpWeb.cgi?dataSource=%s&modeInput=%s&primaryGene=%s&secondaryGene=%s&override=%s&threshold=%s&modeMask_low=%s&modeMask_stddev=%s">' %(output[3], output[0], mode, gene1.geneId, gene2.geneId, useThreshold, threshold, grey_low, grey_stddev)         
         repeated_data[tempkey[counter][0]] = tuple(output)
   if useThreshold == "":
      useThreshold = None
   for item in efpConfig.REPEAT_DATA:
      for counter in range(len(tempkey)):
         if tempkey[counter][0] == item:
            tempkey.insert(counter + 1, repeated_data[item])
            break
   #for key in form:
      #print "<b>"
      #print key
      #print "</b>"
      #print form.getvalue(key)
   #find the position of the currently selected datasource.
   checkcurrent = 0   
   while checkcurrent < len(tempkey):
      if tempkey[checkcurrent][0] == dataSource:
         break
      else:
         checkcurrent = checkcurrent + 1   
   #find the positions of the second data sources again
   for item in efpConfig.REPEAT_DATA:
      for counter in range(len(tempkey)):
         if tempkey[counter][0] == item + '_II':
            new_item = list(tempkey[counter])
            new_item[0] = "II"
            tempkey[counter] = tuple(new_item)
            
   #append (max) to last item
   print '<table style="width:100;white-space:nowrap;text-align:center;margin-left:auto;margin-right:auto">'
   print '    <tr>'

   #change names to shortened
   shortName = {
      "Natural_Variation": "Nat Var",
      "Lateral_Root_Initiation": "LR Init",
      "Light_Series" : "Light",
      "Guard_Cell": "GC",
      "Developmental_Map": "Dev Map", 
   }

   for i in range(len(tempkey)):
      if tempkey[i][0] in shortName.keys():
         tempkey[i] = list(tempkey[i])
         tempkey[i].append(tempkey[i][0].replace('_', ' '))
         tempkey[i][0] = shortName[tempkey[i][0]]
         tempkey[i] = tuple(tempkey[i])
      else:
         tempkey[i] = list(tempkey[i])
         tempkey[i][0] =  tempkey[i][0].replace('_', ' ')
         tempkey[i].append(tempkey[i][0])
         tempkey[i] = tuple(tempkey[i])
   maxkey = list(tempkey[-1])
   maxkey[0] = maxkey[0] + " (max)"
   maxkey = tuple(maxkey)
   tempkey[-1] = maxkey
   counter = 0
   #selected item print
   while counter < len(tempkey):
      if counter == checkcurrent:
         print '        <td bgcolor="#%s%s%s" rowspan=2><table style="border:1px solid black"><tr><td><span title="%s: %s"><font color="%s" style="font-weight:bold">%s<b><u>%s</u></b></a></font></span></td></tr></table></td>' % (tempkey[counter][2], tempkey[counter][2], tempkey[counter][2], tempkey[counter][5], round(tempkey[counter][1], 2), tempkey[counter][3], tempkey[counter][4], tempkey[counter][0])
      else: 
         print '        <td />'
      counter = counter + 1
   print '    </tr>'
   print '    <tr>'

   #print rest of selections
   counter = 0   
   while counter < len(tempkey):
      if counter == checkcurrent:
         print '     '
      else:   
         print '        <td bgcolor="#%s%s%s"><span title="%s: %s"><font color="%s">%s<u>%s</u></a></font></span></td>' % (tempkey[counter][2], tempkey[counter][2], tempkey[counter][2], tempkey[counter][5], round(tempkey[counter][1], 2), tempkey[counter][3], tempkey[counter][4], tempkey[counter][0].replace('_', ' '))
      counter = counter + 1
   print '    </tr>'
   
   print '</table>'

###----------------------print the image-------------------------------------------------------------------------------------------------------------------------------------------------
   view_no = 1
   for view_name in views:
      print '<tr><td style="text-align:center">'
      imgFile = imgFilename[view_name];
      temp_imgPath = imgFilename[view_name].split("/")
      last_element = temp_imgPath[-1]
      match = re.search('^efp', last_element) 
      if match is not None:
         imgFile = 'output/%s'%(last_element)
      print '  <img src="%s" border="0" ' % imgFile
      if view_name in imgMap:
         print 'usemap="#imgmap_%s">'%view_name
         print '%s' % imgMap[view_name]
      else:
         print '>'
      print '</td></tr>'
      # Creates Button and Link to Page for Table of Expression Values
      print '<tr align="center"><td><br>'
      temp_tablePath = tableFile[view_name][1].split("/")
      tableFile_name = 'output/%s'%(temp_tablePath[-1])
   #    print '<input type="button" name="expressiontable" value="Click Here for Table of Expression Values" onclick="location.href=\'%s\'">' % tableFile_name
      print '<input type="button" name="expressiontable" value="Click Here for Table of Expression Values" onclick="resizeIframe(\'ifr%d\', ifr%d);popup(\'table%d\', \'fadein\', \'center\', 0, 1)">&nbsp;&nbsp;' % (view_no, view_no, view_no)
      tableChart_name = tableFile_name.replace(".html", ".png")
      print '<input type="button" name="expressionchart" value="Click Here for Chart of Expression Values" onclick="popup(\'chart%d\', \'fadein\', \'center\', 0, 1)">' % (view_no)
      print '<script type="text/javascript">'
      popup_content = '<span style="color:#000000"><b>For table download right click <a href="%s">here</a> and select "Save Link As ..."</b></span>' % tableFile_name
      popup_content += '<div class="closewin_text">'
      popup_content += '<a href="" onclick="popdown(\\\'table%d\\\');return false;">' % (view_no)
      popup_content += '<span style="color:#000000">[Close]</span></a><br><br>'
      popup_content += '<a href="" onclick="switchPopup(\\\'table%d\\\', \\\'chart%d\\\');return false;">' % (view_no, view_no)
      popup_content += '<span style="color:#000000">[Switch to<br> Chart]</span></a></div>'
      popup_content += '<div class="chart"><iframe id="ifr%d" name="ifr%d" width=900 frameborder=0 src="%s">' % (view_no, view_no, tableFile_name)
      popup_content += 'Your browser doesn\\\'t support iframes. Please use link abvoe to open expression table</iframe></div>'
      popup_width = '1000';
      bg_color = '#FFFFFF';
      print "loadPopup(\'table%d\',\'%s\',\'%s\',%s);" % (view_no, popup_content, bg_color, popup_width)
      popup_content = '<div class="closewin_text">'
      popup_content += '<a href="" onclick="popdown(\\\'chart%d\\\');return false;">' % (view_no)
      popup_content += '<span style="color:#000000">[Close]</span></a><br><br>'
      popup_content += '<a href="" onclick="resizeIframe(\\\'ifr%d\\\', ifr%d);switchPopup(\\\'chart%d\\\', \\\'table%d\\\');return false;">' % (view_no, view_no, view_no, view_no)
      popup_content += '<span style="color:#000000">[Switch to<br>Table]</span></a><br><br>'
      popup_content += '<a href="" onclick="zoomElement(\\\'image%d\\\', 0.1);return false;">' %(view_no)
      popup_content += '<span style="color:#000000">[Zoom +]</span></a><br>'
      popup_content += '<a href="" onclick="zoomElement(\\\'image%d\\\', -0.1);return false;">' %(view_no)
      popup_content += '<span style="color:#000000">[Zoom -]</span></a><br>'
      popup_content += '<a href="" onclick="zoomElement(\\\'image%d\\\', 0);return false;">' % (view_no)
      popup_content += '<span style="color:#000000">[Reset<br>zoom]</span></a></div>'
      popup_content += '<div class="chart"><img id="image%d" height="580px" src="%s"><br></div>' % (view_no, tableChart_name)
      print "loadPopup(\'chart%d\',\'%s\',\'%s\',%s);" % (view_no, popup_content, bg_color, popup_width)
      print "</script>"
      print '<br></td></tr>'
      view_no = view_no + 1
   print '  <tr><td><br><ul>'
   print '  <li>%s was used as the probe set identifier for your primary gene, %s (%s)</li>' % (gene1.getProbeSetId(), gene1.getGeneId(), gene1.getAnnotation())
   if mode == 'Compare':
      print '  <li>%s was used as the probe set identifier for the secondary gene, %s (%s)</li>' % (gene2.getProbeSetId(), gene2.getGeneId(), gene2.getAnnotation())
   print '  </ul>'
   if(dataSource in efpConfig.datasourceFooter):
      print efpConfig.datasourceFooter[dataSource]
   else:
      print efpConfig.datasourceFooter['default']
   print '</td></tr>'
   print '<tr><td><img src="http://bar.utoronto.ca/bbclone/stats_image.php" title="" name="thumbnail" border="0" width="0px" height="0px"></td></tr>'
else:
   print '  <img src="%s" border="0">' % (defaultImgFilename)
print '</table>'
#print '<input type=hidden name="orthoListOn" id="orthoListOn" value=\"0\">'
print '<input type=hidden name="gene_alias1" id="gene_alias1" value=\"\">'
print '<input type=hidden name="gene_alias2" id="gene_alias2" value=\"\">'
print '</body>'

print '</html>'
