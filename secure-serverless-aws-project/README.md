Secure Serverless API on AWS

Overview

As part of my cloud security journey, I built a serverless API using Amazon API Gateway, AWS Lambda, Amazon DynamoDB, IAM, and CloudWatch.

My goal was to understand how these services work together while applying basic cloud security principles, particularly the principle of least privilege.

Architecture

Client → API Gateway → AWS Lambda → Amazon DynamoDB

CloudWatch collects Lambda execution logs for monitoring and troubleshooting.

AWS Services Used

* Amazon API Gateway: Exposes the API endpoint.
* AWS Lambda: Executes the application code.
* Amazon DynamoDB: Stores project records.
* AWS IAM: Controls the permissions granted to Lambda.
* Amazon CloudWatch: Collects execution logs.

What I Implemented

* Created a DynamoDB table containing sample project records.
* Created a Lambda function to retrieve data from DynamoDB.
* Connected the function to API Gateway.
* Replaced broad database permissions with a custom IAM policy restricted to the required read actions on a specific table.
* Used CloudWatch Logs to troubleshoot and inspect function execution.

Challenges and Lessons Learned

1. Empty API response

My API initially returned an empty list. After investigating, I discovered that I had two DynamoDB tables with similar names, and one contained no records.

Lesson: Verify your data source before assuming your code is broken.

2. IAM permissions

I initially used broad DynamoDB permissions while testing. I later created a custom policy to restrict access to the required read operations on a single table.

Lesson: An application should have only the permissions it needs.

3. Security awareness

Preparing screenshots for my portfolio reminded me to review and redact sensitive account information before sharing technical work publicly.

Security Considerations

* Restricted Lambda’s DynamoDB permissions to the intended table.
* Reviewed database access and encryption settings.
* Inspected CloudWatch execution logs.
* Reviewed screenshots before publishing.

The API was used for learning and testing. Authentication, request validation, and throttling should be evaluated before production deployment.

Key Takeaway

This project taught me that building a functional application is only part of the job. Understanding permissions, monitoring execution, and reducing unnecessary access are essential parts of cloud security.

Future Improvements

* Implement API authentication.
* Add request validation and throttling.
* Explore AWS CloudTrail auditing.
* Automate deployment using infrastructure as code.

Project Status

Completed as part of my hands-on AWS and cloud security learning journey.
