#!/usr/bin/perl

# Script for searching&replacing in files of interest.
# Combines the functionalities of `find` and `sed`.

use strict;
use warnings;
use File::Find;


my $fptrn = shift @ARGV;
my $search = shift @ARGV;
my $replacement = shift @ARGV;

my $USAGE = <<"ENU";
Usage: $0 <filename_regex> <search_regex> <replacment_regex>
ENU

die $USAGE unless ($fptrn and $search and $replacement);

find({wanted => \&add, no_chdir => 1}, '.');

sub add {
  my $filename = $_;
  push @ARGV, $filename if (-f and $filename =~ /$fptrn/);
}

# Trick (together with the use of @ARGV below) to perform an in-place edit.
our $^I = "";
while ( <ARGV> ) {
  s/$search/$replacement/g;
  print;
}
