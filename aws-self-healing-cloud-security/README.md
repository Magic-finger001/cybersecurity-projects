AWS Self-Healing Cloud Security Monitoring and Threat Detection System

Project Overview

This project demonstrates an event-driven AWS security monitoring and automated remediation workflow designed to detect and respond to publicly accessible Amazon S3 buckets.

The system uses AWS Config to evaluate S3 bucket configurations, Amazon EventBridge to trigger a response when a relevant non-compliance event occurs, AWS Lambda to apply corrective security settings, and Amazon SNS to send email alerts.

The goal is to demonstrate how cloud security monitoring and automation can reduce the time between detecting a security misconfiguration and taking corrective action.

Project Status: Working prototype — further hardening and testing in progress.

Objectives

* Detect S3 bucket configurations that violate public-access security requirements.
* Trigger an automated response to relevant AWS Config compliance events.
* Apply S3 Block Public Access settings through AWS Lambda.
* Attempt to remove the affected bucket’s bucket policy.
* Send email notifications using Amazon SNS.
* Record execution activity in Amazon CloudWatch Logs.
* Investigate failures and verify remediation outcomes.
* Document security considerations and opportunities for improvement.

Architecture

The project follows this workflow:

1. An S3 bucket is configured in a way that violates the intended security rule.
2. AWS Config evaluates the bucket and records a non-compliant result.
3. Amazon EventBridge matches the relevant compliance-change event.
4. AWS Lambda receives the event and identifies the affected resource.
5. Lambda applies S3 Block Public Access settings and attempts to remove the bucket policy.
6. Amazon SNS sends a security notification.
7. Amazon CloudWatch Logs records execution details for troubleshooting and investigation.

Architecture Diagram

        S3 Bucket Configuration
                  |
                  v
             AWS Config
         Compliance Evaluation
                  |
                  v
          Amazon EventBridge
           Event Detection
                  |
                  v
             AWS Lambda
          Automated Response
                  |
          +-------+-------+
          |               |
          v               v
     Amazon S3         Amazon SNS
     Remediation       Email Alert
          |
          v
    Verify Final State
      CloudWatch Logs
      Execution Evidence

The diagram represents the intended workflow. Successful detection, remediation, notification, and final-state verification must each be tested independently.

AWS Services Used

Service	Purpose
Amazon S3	Stores the test bucket and its configuration
AWS Config	Evaluates bucket compliance
Amazon EventBridge	Routes relevant compliance-change events
AWS Lambda	Executes automated remediation logic
Amazon SNS	Sends security alert emails
Amazon CloudWatch Logs	Records Lambda execution activity
AWS CloudTrail	Supports investigation of relevant API activity
AWS IAM	Controls permissions for the Lambda execution role

Implementation

1. S3 Test Environment

I created a dedicated S3 bucket for controlled security testing.

For the test, I intentionally introduced a public-access misconfiguration to simulate a cloud security incident.

No production data should be used for this experiment.

2. Detection with AWS Config

I configured the AWS managed rule:

s3-bucket-level-public-access-prohibited

The rule evaluates S3 bucket configurations against its public-access requirements.

When a resource violates the rule, AWS Config can record a non-compliant evaluation.

3. Event-Driven Response

I configured an Amazon EventBridge rule to match relevant AWS Config compliance-change events indicating non-compliance.

The rule invokes the Lambda function responsible for remediation.

4. Automated Remediation with Lambda

The Lambda function is named:

auto-remediate-s3-public

Its intended responsibilities are:

* Identify and validate the affected S3 bucket.
* Apply all four S3 Block Public Access settings.
* Attempt to remove the bucket policy.
* Publish a notification to Amazon SNS.
* Record execution details in CloudWatch Logs.

The implementation requires appropriate IAM permissions for the actions it performs.

5. Email Notifications

I configured an Amazon SNS topic named:

Magic-security-alerts

After the remediation workflow executes, the function publishes a notification to the configured topic.

The alert provides information about the affected bucket and the attempted corrective action.

6. Logging and Investigation

CloudWatch Logs provides execution records that help investigate failures and understand the Lambda function’s behavior.

CloudTrail can provide additional evidence about API activity, identities, and changes associated with the incident.

Testing and Results

I tested the workflow by introducing a controlled public-access misconfiguration in the dedicated S3 test bucket.

The following behaviors were observed during testing:

* AWS Config recorded a non-compliant result.
* The EventBridge rule triggered the Lambda function.
* CloudWatch Logs recorded remediation activity.
* An SNS email notification was received after correcting an SNS topic configuration issue.

One Lambda execution reported a duration of approximately 662 milliseconds.

This is the Lambda execution duration, not the total time from the original security misconfiguration to verified remediation.

End-to-end response time requires separate measurement.

The final security state should be verified by checking the bucket configuration and confirming that the bucket is no longer publicly accessible through the tested access paths.

See docs/testing.md for the test procedure and evidence.

Challenges Encountered

SNS Topic Configuration Error

During testing, the Lambda function failed to publish a notification because the SNS topic could not be found.

CloudWatch Logs reported a NotFound error during the SNS Publish operation.

Root Cause

The Lambda function did not have the correct SNS topic ARN configured for its execution environment.

Resolution

I configured the SNS_TOPIC_ARN Lambda environment variable with the correct SNS topic ARN and verified that the execution role had permission to publish to the topic.

I then repeated the test and confirmed that the email notification arrived.

This experience demonstrated the importance of environment configuration, logging, and end-to-end testing in event-driven cloud security systems.

Security Considerations

This project is a learning prototype and should not be deployed directly into production without further review.

Important considerations include:

* Apply least-privilege IAM permissions.
* Validate incoming events before performing security-sensitive actions.
* Confirm that the affected resource belongs to the intended AWS account and environment.
* Handle failed remediation actions explicitly.
* Avoid suppressing unexpected exceptions.
* Verify the final S3 configuration after remediation.
* Consider legitimate bucket policies before deleting them.
* Monitor failed Lambda executions and notification failures.
* Protect logs and screenshots from exposing sensitive information.
* Test the workflow against duplicate events, malformed events, and partial failures.
* Review S3 Block Public Access settings at both bucket and account levels.

A successful Lambda invocation or email notification does not, by itself, prove that the bucket is secure.

Lessons Learned

This project helped me understand how AWS security services can work together to detect and respond to cloud misconfigurations.

Key lessons included:

1. Monitoring and remediation are separate stages.
2. Event-driven architectures depend on correct configuration between services.
3. CloudWatch Logs is essential for troubleshooting.
4. Automated security actions require careful permission design.
5. Remediation must be verified rather than assumed.
6. Security evidence makes a project easier to review and reproduce.

Future Improvements

Planned improvements include:

* Create a CloudWatch dashboard for security events and remediation activity.
* Improve error handling and failure notifications.
* Measure end-to-end detection and remediation time.
* Add structured logging and more detailed remediation results.
* Integrate additional security findings where appropriate.
* Expand testing to cover failure scenarios.
* Document the complete deployment process.
* Add a short demonstration video.

Evidence

Screenshots and supporting documentation are stored in the screenshots/ directory.

The evidence should demonstrate the configuration, detection event, remediation execution, notification, and verified final state.

Disclaimer

This project was developed for educational and portfolio purposes in a controlled AWS environment.

The test intentionally introduces a security misconfiguration. Do not reproduce it on production resources or buckets containing sensitive information.

Automated remediation can affect application availability and legitimate access. Review and test all security actions before using them in a production environmentIAM Permissions and Least-Privilege Design

The automated remediation function uses an IAM execution role to interact with AWS services.

The role needs permission to apply S3 Block Public Access settings, perform the configured bucket-policy remediation, publish security notifications through Amazon SNS, and write execution logs to CloudWatch Logs.

Permission Design

* Amazon S3: Allows the function to apply public-access restrictions to the intended test bucket.
* Amazon SNS: Allows the function to publish security alerts to the configured notification topic.
* Amazon CloudWatch Logs: Allows the function to record execution activity for troubleshooting and investigation.

Security Considerations

The execution role should follow the principle of least privilege by granting only the permissions required for the function’s intended responsibilities.

Resource-level restrictions should be applied wherever supported. The function should also validate incoming events before making security-sensitive changes.

The IAM policy published in this repository is intended to document the project’s permission design. It should be checked against the actual deployed role before being treated as an exact representation of the AWS environment.

For production use, permissions and remediation behavior should undergo additional security review and testing.


Author

Jacob Idowu

Cloud security learner documenting practical AWS security engineering projects.

GitHub: Magic-finger001

⸻

Learning by building, testing, troubleshooting, and documenting.
