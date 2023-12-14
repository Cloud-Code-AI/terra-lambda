import json
import subprocess
import boto3

# Path to the Terraform executable
TERRA_PATH = "./terraform"

def run_command(command):
    """
    Executes a given shell command and returns the output and error.

    Args:
    command (list): The command to be executed as a list of strings.

    Returns:
    tuple: A tuple containing an error message (if any) and the command's output.
    """
    print("Incoming Command: ", command)
    try:
        # Run the command and capture the output and error
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        # Extract the output and error
        output = result.stdout
        error = result.stderr
        print("Terraform Output: ", output)
        print("Terraform error: ", error)

        # Check if the command was executed successfully
        if result.returncode != 0:
            return f"Error: {error}", None
        else:
            return None, output

    except Exception as e:
        # Handle any other exceptions
        return f"Exception: {str(e)}", None


def deploy_terraform(s3_bucket, path):
    """
    Downloads a Terraform file from S3 and applies the Terraform plan.

    Args:
    s3_bucket (str): The name of the S3 bucket.
    path (str): The path to the Terraform file in the S3 bucket.

    Returns:
    str: The result of the Terraform apply command.
    """
    s3 = boto3.resource('s3')
    main_file = s3.Object(s3_bucket, path)
    main_file.download_file('/tmp/main.tf')

    # Initialize and apply the Terraform plan
    res, _ = run_command(f'{TERRA_PATH} -chdir=/tmp init')
    res, _ = run_command(f'{TERRA_PATH} -chdir=/tmp apply -auto-approve')
    return res
    

def lambda_handler(event, context):
    """
    AWS Lambda handler function for applying a Terraform plan.

    Args:
    event (dict): The event triggering the Lambda function, expected to contain
                  'bucket' and 'key' keys with S3 bucket and path information.
    context (LambdaContext): Provides information about the invocation, function, and runtime environment.

    Returns:
    dict: A response object with status code and body.
    """
    s3_bucket = event.get("bucket")
    path = event.get("key")
    print(f"S3 Bucket: {s3_bucket} and Path: {path}")

    # Validate event data
    if not s3_bucket or not path:
        return {
            'statusCode': 404,
            'body': json.dumps('Invalid event data')
        }

    # Apply the Terraform plan
    deploy_terraform(s3_bucket=s3_bucket, path=path)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
