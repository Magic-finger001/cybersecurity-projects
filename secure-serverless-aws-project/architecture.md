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
