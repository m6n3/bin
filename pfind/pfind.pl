#!/usr/bin/perl

use strict;
use warnings;
use File::Find;


my $verbose = 0;
if ($ARGV[0] eq '-v') {
  $verbose = 1;
  shift @ARGV
}

my $fpattern = shift @ARGV;
my $cpattern = shift @ARGV;

unless ($fpattern and $cpattern) {
  die "Usage: $0 [-v] <file pattern> <content pattern>\n";
}

find({ wanted => \&process, no_chdir => 1}, '.');

sub process {
  my $filename = $_;
  if (-f and $filename =~ /$fpattern/) {
    open my $fh, '<', $filename or warn "Could not open $filename: $!";
    while (my $line = <$fh> ) {
      chomp($line);
      if ($line =~ /$cpattern/) {
        $verbose ? print "$filename: $line \n" : print "$filename \n";
        last;     
      }
    }
    close $fh;
  }
}
