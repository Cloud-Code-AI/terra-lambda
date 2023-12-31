# Terra-lambda
An Terraform Executor Lambda Function. Run terraform from lambda function using python.

## Overview

This AWS Lambda function is designed to automate the process of applying Terraform plans. It downloads a specified Terraform file from an AWS S3 bucket and executes the Terraform plan. This function is particularly useful for automating infrastructure provisioning and management tasks in AWS environments.

## Features

- **S3 Integration**: Downloads Terraform files directly from a specified S3 bucket.
- **Automated Terraform Execution**: Automatically initializes and applies Terraform plans. It uses terraform 1.5.7 which is truly open source, so no need to worry about the license issue.

## Prerequisites

- **AWS Account**: You must have an AWS account and be familiar with AWS services, particularly AWS Lambda and S3.
- **IAM Role**: An IAM role with necessary permissions for Lambda execution, S3 access, and any other AWS services that your Terraform plan interacts with.

## Deployment

1. **Package the Lambda Function**:
   - Clone the github repository
   - run the `build.sh` file using `bash build.sh` command. This will generate a zip file named `terra_lambda.zip` to your folder.

2. **Create Lambda Function**:
   - Go to the AWS Lambda console and create a new function.
   - Upload the zip file as the function package.
   - Set the runtime to Python 3.11.
   - Attach the IAM policy provided in `iam_policy.json`

3. **Set Up Trigger Permissions**:
   - Configure the trigger permission for the Lambda function so that it can read S3 bucket files..

4. **Test the Function**:
   - You can test the function manually by creating a test event in the Lambda console with the required `bucket` and `key` values.

## Usage

To use the Lambda function, trigger it with an event containing the following structure:

```json
{
  "bucket": "your-s3-bucket-name",
  "key": "path/to/your/terraform/file.tf"
}
```

The function will download the specified Terraform file from the given S3 bucket and path, initialize the Terraform environment, and apply the plan.

## Security

Ensure that the Lambda function's IAM role has only the necessary permissions and follows the principle of least privilege. Review and validate your Terraform scripts to ensure they do not perform any unintended actions.

## Logging and Monitoring

Logs are generated by the Lambda function and can be monitored via Amazon CloudWatch. It's recommended to set up alerts for any errors or unexpected behavior.

