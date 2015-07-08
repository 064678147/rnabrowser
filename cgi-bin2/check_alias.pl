#!/usr/bin/perl
# Hardeep Nahal
# January 17 2013
# check_alias.pl
# Backend Perl script that validates whether gene/gene alias is valid. 
# Returns a 0/1 value

use DBI;
use CGI qw/standard/;
use JSON;


#open (TEST, ">output/testing_checkalias.txt");

my $cgiobject = new CGI;
my $primaryGene = $cgiobject->param('gene1');
my $secondaryGene = $cgiobject->param('gene2');
my $modeInput = $cgiobject->param('modeInput');
my $alias = "";
my $result = "";

print "Content-type: text/html\n\n";

$result = checkId($primaryGene);
if ($modeInput eq "Compare")
{
	$result = checkId($secondaryGene);
}
print "$result";

# checkId
# @Input: $gene: input gene
# @Output: true/false value indicating whether gene is valid

sub checkId 
{
	my ($gene) = @_;
	my $dbh;
	my $probequery = '';
	my $sthprobe = '';

	if ($gene =~ /At[1-5]g[0-9]{5}/i)
	{
		#print TEST "gene is an AGI\n";
		$dbh = DBI->connect("dbi:mysql:annotations_lookup:localhost", "efp_user", "efp_user") or die "Cannot open connection: $DBI::errstr\n";
		$probequery = "SELECT agi FROM at_agi_lookup WHERE agi = (?) AND date = (SELECT MAX(t1.date) FROM at_agi_lookup t1)";
		$sthprobe = $dbh->prepare("$probequery") or die "Cannot prepare statement: $DBI::errstr\n";
		$sthprobe->execute($gene) or die "Cannot execute statement: $DBI::errstr";
	}
	else {
		$dbh = DBI->connect("dbi:mysql:annotations_lookup:localhost", "efp_user", "efp_user") or die "Cannot open connection: $DBI::errstr\n";
		$probequery = "SELECT alias FROM agi_alias AS alias WHERE alias = (?) AND date = '2012-02-07'";
		$sthprobe = $dbh->prepare("$probequery") or die "Cannot prepare statement: $DBI::errstr\n";
		$sthprobe->execute($gene) or die "Cannot execute statement: $DBI::errstr";
	}

	my @row = $sthprobe->fetchrow_array();
	$alias = $row[0];
	#print TEST "alias = $alias\n";	
	if ($alias ne "")
	{
		#print TEST "returned 1\n";
		return "1";
	}
	else{
		#print TEST "returned 0\n";
		return "0";
	}
}
