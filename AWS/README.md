ep:
DOC. BASADO EN 
https://github.com/aws-samples/aws-hpc-workshops/blob/master/README-WRF.rst


wokkon wrf_aws
sudo pip install cfncluster

aws configure
[Errno 13] Permission denied: '/Users/luisvargas/.aws/credentials'
FIX
sudo chmod 777  /Users/luisvargas/.aws/credentials
sudo chmod 777  /Users/luisvargas/.aws/config     
sudo chown luisvargas /Users/luisvargas/.aws/config
sudo chown luisvargas /Users/luisvargas/.aws/credentials 
            
aws configure
AWS Access Key ID [****************XXDA]: AKIAJKSDIYHC25IOFS2A
AWS Secret Access Key [****************v3KT]: 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
Default region name [us-east-1]: 
Default output format [json]: json

cfncluster configure    
Cluster Template [default]: wrf
AWS Access Key ID []: AKIAJKSDIYHC25IOFS2A
AWS Secret Access Key ID []: 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

Add the following setting into 

cat  ~/.cfncluster/config
[aws]
aws_region_name = us-west-2
aws_access_key_id = AKIAJKSDIYHC25IOFS2A
aws_secret_access_key = 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

[cluster WRF]
vpc_settings = test
key_name = test1_aws
compute_instance_type = t2.micro
master_instance_type = t2.micro
master_root_volume_size = 100
cluster_type = ondemand
placement = cluster
placement_group = DYNAMIC
base_os = alinux
extra_json = { "cfncluster" : { "cfn_scheduler_slots" : "cores" } }
s3_read_write_resource = arn:aws:s3:::bucket-id1-cfncluster/*
post_install = s3://bucket-id1-cfncluster/cfncluster_postinstall.sh
ebs_settings = wrf-ebs


[vpc test]
master_subnet_id = subnet-933914f6
vpc_id = vpc-7380dc16

[global]
update_check = true
sanity_check = true
cluster_template = WRF

[aliases]
ssh = ssh {CFN_USER}@{MASTER_IP} {ARGS}

[ebs wrf-ebs]  ## Used for the NFS mounted file system
volume_type = io1
volume_size = 250
volume_iops = 5000

TODOOOOOOOO MUY IMPORTANTE VER SETTING DE SCALING O AUTOSCALING

RAM MINIMA PARA INTELCOMPILER : 2 GB


cfncluster create WRF
cfncluster ssh WRF  -i ~/Downloads/test1_aws.pem
cfncluster delete WRF


UNA VEZ EN EL MASTER
DE ACA EN ADELANTE SEGUIR INSTALACION DE WRF/WPS/ARWPOST/NETCDF, ETC

cfncluster create WRF               
Beginning cluster creation for cluster: WRF
Creating stack named: cfncluster-WRF
Status: cfncluster-WRF - ROLLBACK_IN_PROGRESS                                   
Cluster creation failed.  Failed events:
  - AWS::EC2::Instance MasterServer Placement groups may not be used with instances of type 't2.micro'. (Service: AmazonEC2; Status Code: 400; Error Code: InvalidParameterCombination; Request ID: 540a82f4-2c6f-453b-8435-000b0706df6e)

FIX : check parametros [cluster] en ~/.cfncluster/config

probar sin estos parametros
compute_instance_type = t2.micro
master_instance_type = t2.micro
master_root_volume_size = 100







 INTEL COMPILER
https://software.intel.com/sites/default/files/managed/17/53/parallel-studio-xe-2018-install-guide-linux.pdf



vim .bashrc



cd /shared/

wget http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12998/parallel_studio_xe_2018_update3_cluster_edition.tgz

tar xvf parallel_studio_xe_2018_update3_cluster_edition.tgz 

cd parallel_studio_xe_2018_update3_cluster_edition
sudo su
./install.sh




mkdir WRF
cd WRF 
wget WRFV3.8.1.TAR.gz
tar xvf WRFV3.8.1.TAR.gz
cd WRFV3



cd

wget netcdf-4.1.3.tar.gz



