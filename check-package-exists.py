import sys, boto3, logging, json, os

def check_package_exists(package_name, s3_bucket):
    # Create boto3 s3 resource
    s3_resource = boto3.resource('s3')

    # Get all file names in s3 bucket
    s3_bucket = s3_resource.Bucket(s3_bucket)
    for file in s3_bucket.objects.all():
        file_name = file.key
        # Check if file with the same package name + version already exists
        if file_name == package_name + ".csv":
            return True
    return False

def stop_build(file_exists, codebuild_ids):
    if file_exists: # S3 file with the same package name & version exists
        codebuild_ids_dict = json.loads(codebuild_ids) # convert json to dictionary
        # Get ID of most recent code build with PROJECT_NAME
        build_id = codebuild_ids_dict["ids"][0] 
        # Stop the build
        os.system("aws codebuild stop-build --id " + build_id)
        logging.info('Build stoppped because there is already an existing file in s3 with the same package name/version')


if __name__ == "__main__":
    package_name=sys.argv[1] # Package name and version
    s3_bucket=sys.argv[2] # S3 bucket name
    codebuild_ids=sys.argv[3] # List of CodeBuild IDs with PROJECT_NAME

    file_exists = check_package_exists(package_name, s3_bucket)
    stop_build(file_exists, codebuild_ids)