import sys, json, pandas as pd, boto3, logging

    
def get_scan_info(json_scan_results, package_name):
    # Convert scan json to dictionary
    scan_info_dict = json.loads(json_scan_results)
    logging.warning("REAL PACKAGE NAME IS: " + package_name)
    for scan in scan_info_dict["imageScanFindings"]["findings"]:
        scan_package_name = scan["attributes"][1]["value"]
        scan_package_version = scan["attributes"][0]["value"]
        logging.warning("package name + version is : " + scan_package_name + "=" + scan_package_version)
        name_version = scan_package_name + "=" + scan_package_version
        logging.warning(name_version==package_name)
        if (name_version == package_name):
            return scan

def convert_to_csv(scan, csv_file_name):

    logging.warning(scan)

    # Scan info HAS CVSS2 score and vector 
    if len(scan['attributes']) > 2:
        # Format scan dictionary to improve readability
        formatted_scan = {
            'cve_id': [scan['name']],
            'description': [scan['description']],
            'uri': [scan['uri']],
            'severity': [scan['severity']],
            'package_name': [scan['attributes'][1]['value']],
            'package_version': [scan['attributes'][0]['value']],
            'CVSS2_VECTOR': [scan['attributes'][2]['value']],
            'CVSS2_SCORE': [scan['attributes'][3]['value']]
        }

    # Scan info DOES NOT HAVE CVSS 2 score or vector
    else:
        # Format scan dictionary to improve readability
        formatted_scan = {
            'cve_id': [scan['name']],
            'description': [scan['description']],
            'uri': [scan['uri']],
            'severity': [scan['severity']],
            'package_name': [scan['attributes'][1]['value']],
            'package_version': [scan['attributes'][0]['value']]
        }

    # Create CSV file
    df = pd.DataFrame(formatted_scan)
    df.to_csv(csv_file_name, index=False)


def upload_to_s3(file_name, s3_file, s3_bucket_name):

    # Create boto3 s3 resource
    s3_resource = boto3.resource('s3')

    # Get s3 bucket
    s3_bucket = s3_resource.Bucket(s3_bucket_name)

    # Upload csv file to s3 bucket
    s3_bucket.put_object(Key = s3_file, Body = open(file_name, 'rb'))


if __name__ == "__main__":
    results=sys.argv[1] # JSON results from ECR vulnerability scanning
    package_name=sys.argv[2] # Package name and version
    #logging.warning(results)
    logging.warning("package name is " + package_name)
    s3_bucket_name = sys.argv[3] # S3 bucket name

    # Get vulnerability info for package 
    scan = get_scan_info(results, package_name) 

    # Convert vulnerability info to CSV file
    convert_to_csv(scan, package_name + ".csv") 

    # Upload CSV to s3
    upload_to_s3(package_name + ".csv", package_name + ".csv", s3_bucket_name) 