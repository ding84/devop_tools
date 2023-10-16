import subprocess
import yaml

# Load the YAML configuration
with open('sync_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Define the source and target bucket names
source_bucket = config['source_bucket']
target_buckets = config['target_buckets']

# AWS credentials
aws_access_key_id = config.get('aws_access_key_id')
aws_secret_access_key = config.get('aws_secret_access_key')

# Build the AWS CLI command
aws_cli_command = ["aws", "s3", "sync", f"s3://{source_bucket}"]

if aws_access_key_id and aws_secret_access_key:
    # If access key and secret key are provided in the config, use them
    aws_cli_command.extend(["--access-key", aws_access_key_id, "--secret-key", aws_secret_access_key])

# Sync data from the source bucket to each target bucket
for target_bucket in target_buckets:
    sync_command = aws_cli_command + [f"s3://{target_bucket}", "--delete"]
    
    try:
        # Run the AWS CLI sync command
        result = subprocess.run(sync_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output
        print(f"Synced data from {source_bucket} to {target_bucket}")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error syncing data to {target_bucket}:")
        print(e.stderr)

