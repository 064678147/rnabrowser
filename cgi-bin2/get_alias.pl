#!/usr/bin/perl
# Hardeep Nahal
# January 17 2013
# get_alias.pl
# Backend Perl script that returns a list of matching gene aliases based on the first few characters of user's input
# Returns a list in JSON format

use DBI;
use CGI qw/standard/;
use JSON;

my $cgiobject = new CGI;
my @probesetList;
my $result = "";

#open (TEST, ">output/testing_probeset.txt");

$primaryGene = $cgiobject->param('term');
# if entered gene looks like an AGI, then don't search database since it's not a gene alias
if ($primaryGene =~ /At[1-5]/)
{
	exit;
}

print "Content-type: text/html\n\n";
my $dbh = DBI->connect("dbi:mysql:annotations_lookup:localhost", "efp_user", "efp_user") or die "Cannot open connection: $DBI::errstr\n";
my $probequery = "SELECT alias, agi FROM agi_alias AS alias WHERE alias LIKE (?) AND date = '2012-02-07'";
my $sthprobe = $dbh->prepare("$probequery") or die "Cannot prepare statement: $DBI::errstr\n";
$sthprobe->execute($primaryGene.'%') or die "Cannot execute statement: $DBI::errstr";

while (my @row = $sthprobe->fetchrow_array())
{
	my $json = {};
	my $alias = $row[0];
	my $agi = $row[1];
	$json->{value} = $alias;
	$json->{label} = "$alias $agi";
	$json->{id} = $agi;
	push (@probesetList, $json);
}
	
print JSON::to_json(\@probesetList);
