# AWS Serverless API Architecture

## 1. Overview

This document describes the architecture of my secure serverless API built on Amazon Web Services (AWS).

The application uses API Gateway to receive requests, AWS Lambda to process them, and Amazon DynamoDB to store project data.

AWS IAM controls the permissions available to Lambda, while Amazon CloudWatch collects execution logs for monitoring and troubleshooting.

## 2. Architecture Diagram

```text
                 +----------------------+
                 |        Client        |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Amazon API Gateway|
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |      AWS Lambda     |
                 | secure-cloud-project-api |
                 +----------+-----------+
                            |
                   IAM execution role
                   (DynamoDB read access)
                            |
                            v
                 +----------------------+
                 |   Amazon DynamoDB   |
                 | cloud-security-projects |
                 +----------------------+

                 +----------------------+
                 |   Amazon CloudWatch |
                 |    Execution Logs   |
                 +----------------------+
                            ^
                            |
                      Lambda logs
3. AWS Components

Amazon API Gateway

Provides the HTTP endpoint through which clients submit requests to the application.

API Gateway invokes the configured Lambda integration.

AWS Lambda

The secure-cloud-project-api function processes incoming requests and retrieves project data from DynamoDB.

The function runs without requiring a dedicated server.

Amazon DynamoDB

The cloud-security-projects table stores the sample project records returned by the API.

AWS IAM

The Lambda execution role controls which AWS resources the function can access.

The custom LeastPrivilege-DynamoDB-Read-only policy grants the specified DynamoDB read actions:

* dynamodb:Scan
* dynamodb:GetItem
* dynamodb:Query

The policy should be restricted to the intended DynamoDB table and AWS account.

Amazon CloudWatch

CloudWatch Logs collects Lambda execution information, helping with troubleshooting and investigation of application errors.

4. Request Flow

1. A client sends an HTTP request to API Gateway.
2. API Gateway invokes the Lambda function.
3. Lambda processes the request.
4. Lambda uses its execution role to access DynamoDB.
5. DynamoDB returns the requested data.
6. Lambda prepares a response.
7. API Gateway returns the response to the client.
8. CloudWatch collects Lambda execution logs.

5. Security Considerations

Least-Privilege Access

The Lambda execution role should have only the permissions required for its task.

The custom IAM policy is intended to permit specific read operations rather than unrestricted DynamoDB access.

Database Access

DynamoDB access is controlled through AWS IAM permissions.

The database should not be exposed directly to unauthenticated clients.

API Protection

If the API endpoint is publicly accessible, additional controls should be considered before production use:

* API authentication and authorization
* Request validation
* Throttling and rate limiting
* Appropriate error handling

Logging

CloudWatch Logs supports monitoring and troubleshooting.

Logs should not contain credentials, access tokens, or unnecessary sensitive information.

6. Current Limitations

This is a learning project rather than a production-ready service.

Additional work may be needed to implement and verify authentication, request validation, rate limiting, automated testing, and alerting.

7. Key Learning

This project helped me understand how API Gateway, Lambda, DynamoDB, IAM, and CloudWatch work together.

It also reinforced the importance of restricting permissions and considering security throughout the application architecture.

