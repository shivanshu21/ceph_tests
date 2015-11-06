open my $fh, '<', "deletes" or die "Cannot open";
my @list = <$fh>;
foreach $i (@list) {
    ##print("Line: $i\n");
    $command = "git rm $i";
    `$command`;
}
