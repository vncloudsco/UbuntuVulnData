#!/bin/bash -e

# ------ VARIABLES ------ #
stack_name="UbuntuVulnData" 
num_code_builds=3 # manually update this variable depending on the number of packages being installed in CloudFormation.yaml
# ----------------------- #

# Exit and clean up when any command fails
function cleanup {
  echo "Cleaning up and deleting cloudformation stack $stack_name"
  aws cloudformation delete-stack --stack-name $stack_name --profile twitch-cwijulia
}
trap cleanup ERR EXIT

# ------- BUILD STARTING ------- #
echo "Starting project build process"

# Create stack
echo "Creating stack named $stack_name"
aws cloudformation create-stack --stack-name $stack_name --template-body file://CloudFormation.yaml --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --profile twitch-cwijulia

# Wait for stack to finish creating
echo "Waiting for stack to finish creating (3 minutes)"
sleep 180

# Update stack (interface endpoint parameter PrivateDNSEnabled must be updated to true)
echo "Updating stack named $stack_name"
aws cloudformation update-stack --stack-name $stack_name --template-body file://CloudFormation_update.yaml --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --profile twitch-cwijulia

# Wait for stack to finish updating
echo "Waiting for stack to finish updating (3 minutes)"
sleep 180

# Start codebuild projects
echo "Starting CodeBuild process"
counter=1
while [ $counter -le $num_code_builds ]
do 
    echo "Starting CodeBuild project $stack_name-codebuild-project-$counter"
    aws codebuild start-build --project-name $stack_name-codebuild-project-$counter --profile twitch-cwijulia
    counter=$((counter+1))
    echo "Enter :q to continue"
done

# Wait for codebuild projects to finish running
echo "Waiting for coldebuild projects to complete (10 minutes)"
sleep 600

echo "Project build complete" # stack will automatically delete itself once it reaches the EOF

