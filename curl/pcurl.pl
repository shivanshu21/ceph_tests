##============= PARAMS ==============
#my $user_id        = '08d9079e37ca4750ae1b223af8869f92';
my $user_id        = '304018976221';
#my $user_name      = 'DSS';
my $user_name      = 'dss_test_0001';
#my $passw          = 'Reliance111@';
my $passw          = 'D2=lH6-fA2$b';

#my $token          = '86c226d787cb4341911cdf9e5cee1732'; ## Generate and put
my $token          = '2fb7ae1a40b94926af127a56dd5d77d3'; ## Generate and put
my $access_key     = '2bf9f42cc7fa47fdae06f14dddd7e4ac';
my $user_to_create = ''; ## For creating new users
##===================================


##===================================
## DO NOT ALTER
##===================================

## No terminating slash '/' in URLs
#my $rgw_endpoint   = 'http://127.0.0.1:8000';
my $rgw_endpoint   = 'http://10.140.214.198:7480';
my $iam_endpoint   = 'https://iam.ind-west-1.staging.jiocloudservices.com:5000/v3';
my $signature      = 'H/AUlsWSTz7LeeeSDhu2G4m8S+E=';
my $cannonical_str = 'R0VUCgoKRnJpLCAwNSBGZWIgMjAxNiAxMTowNjo0NiBHTVQKLw==';
our $GLOBAL_DEBUG  = 1;
##========== IAM REQUESTS ===========

my $signreq = "curl -s -vvv -X POST $iam_endpoint/sign-auth -H \"Content-Type: application/json\" -d '{\"credentials\": {\"access\": \"$access_key\", \"signature\": \"$signature\", \"token\": \"$cannonical_str\", \"action_resource_list\": [{\"action\": \"jrn:jcs:dss:ListBucket\", \"resource\": \"jrn:jcs:dss::Bucket:*\", \"implicit_allow\": \"False\"}]}}'";

my $tokreq = "curl -v -H \"Content-Type: application/json\" -d '{ \"auth\": {\"identity\": {\"methods\": [\"password\"],\"password\": {\"user\": {\"name\": \"$user_name\",\"account\": { \"id\": \"$user_id\" },\"password\":\"$passw\"}}}}}' $iam_endpoint/auth/tokens";

my $usercreate = "curl -i -H \"Content-Type: application\/json\" -H \"X-Auth-Token: $token\"  \"$iam_endpoint?Action=CreateUser&Name=$user_to_create&Password=Reliance111@\" ";

my $usercredentialscreate = "curl -i -H \"Content-Type: application\/json\" -H \"X-Auth-Token: $token\"  $iam_endpoint?Action=CreateCredential&UserId=$user_id";

my $iamtokvalidation = "curl -v -H \"X-Auth-Token: $token\" \"$iam_endpoint/token-auth?action=jrn:jcs:dss:ListBucket&resource=jrn:jcs:dss::Bucket:newbucket \" ";

##========== DSS REQUESTS ===========

my $rgwreq = "curl -v -X \"PUT\" -H \"X-Auth-Token: $token\" $rgw_endpoint/consolebucktest001"; # Create bucket

#my $rgwreq = "curl -v -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002"; # List bucket

#my $rgwreq = "curl -v -H \"X-Auth-Token: $token\" $rgw_endpoint/"; # List all my buckets

#my $rgwreq = "curl -v -X \"HEAD\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002"; # Head bucket

#my $rgwreq = "curl -v -X \"DELETE\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002"; # Delete bucket

#####my $rgwreq = "curl -v -X \"PUT\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002"; # Create object

#my $rgwreq = "curl -v -X \"GET\" -H \"X-Auth-Token: $token\" $rgw_endpoint/bucket1/obj"; # Download object

#my $rgwreq = "curl -v -X \"HEAD\" -H \"X-Auth-Token: $token\" \"$rgw_endpoint/bucket1/obj\""; # Head object

#my $rgwreq = "curl -v -X \"DELETE\" -H \"X-Auth-Token: $token\" $rgw_endpoint/bucket1/obj"; # Delete object

#my $rgwreq = "curl -v -X \"PUT\" -H \"X-Auth-Token: $token\" -H \"x-jcs-metadata-directive: COPY\" -H \"x-jcs-copy-source: copysourcebucket\/obj500\" -H \"x-jcs-storage-class: STANDARD\" -H \"Content-Length: 0\" \"$rgw_endpoint/shivbucket0002/obj501\""; # Copy object

#my $rgwreq = "curl -v -X \"POST\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002/output.dat?uploads"; # Initiate multipart upload

####my $rgwreq = "curl -v -X \"PUT\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002output.dat?uploadId=2~0qEl87oQBALdIZY-g6IcawZuKjyLFi3&partNumber=1"; # Upload a part

#my $rgwreq = "curl -v -X \"GET\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002?uploadId=2~D3L6Qv_VdSER9dhOs2BjTkKXSTGcxPU"; # List all parts

#my $rgwreq = "curl -v -X \"GET\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002?uploads"; # List all multipart uploads

#my $rgwreq = "curl -v -X \"PUT\" -H \"X-Auth-Token: $token\" $rgw_endpoint/shivbucket0002"; # Abort multipart uploads

##============ WORKFLOW  ============

#doAction($signreq);
#doAction($tokreq);
doAction($rgwreq);
#doAction($usercreate);
#doAction($usercredentialscreate);
#doAction($iamtokvalidation);

while(0) {
    my $input = getMainChoice();
    if ($input =~ /[1]/) {
        whisper("\nIAM action requested");
        handleIamChoice(getIamChoice());
    } elsif ($input =~ /[2]/) {
        whisper("\nDSS action requested");
        doAction($rgwreq);
        #handleDssChoice(getDssChoice());
        last;
    } elsif ($input =~ /[3]/) {
        whisper("\nIAM user workflow");
        #handleUserChoice(getUserChoice());
        last;
    } elsif ($input =~ /[4]/) {
        whisper("\nIAM policy workflow");
        #handlePolicyChoice(getPolicyChoice());
        last;
    } elsif ($input =~ /[5]/) {
        last;
    }
}

##============ SUBROUTINES ===========

sub doAction {
    my $str = shift;
    print ($str);
    my $resp = qx($str);
    print $resp;
    print("\n=====\n\n");
}

sub whisper {
    if($GLOBAL_DEBUG == 1) {
        print shift;
    }
}

sub getMainChoice()
{
    my $choice;
    print("\n\nEnter command:\n");
    print("\t1. IAM actions\n");
    print("\t2. DSS actions\n");
    print("\t3. IAM user workflow\n");
    print("\t4. IAM policy workflow\n");
    print("\t5. Exit\n");
    $choice = <STDIN>;
    chomp($choice);
    return $choice;
}

sub getIamChoice {
    my $choice;
    print("\n\tIAM choices:");
    print("\n\t\t1. Generate new token");
    print("\n\t\t2. Update your user info for this program (ID, username, password)");
    print("\n\t\t3. Send a signed request to IAM for verification");
    print("\n\t\t4. Update token value for this program");
    print("\n\t\t5. Back\n");
    $choice = <STDIN>;
    chomp($choice);
    return $choice;
}

sub handleIamChoice {
    my $choice = shift;
    if ($choice =~ /[1]/) {
        doAction($tokreq);
    } elsif ($choice =~ /[2]/) {
        exit(0);
    } elsif ($choice =~ /[3]/) {
        doAction($signreq);
    } elsif ($choice =~ /[4]/) {
        print("\nEnter new token: ");
        $token = <STDIN>;
        chomp($token);
    } elsif ($choice =~ /[5]/) {

    }
    return 0;
}
##===================================
