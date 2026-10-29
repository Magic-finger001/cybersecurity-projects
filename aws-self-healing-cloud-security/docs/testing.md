Test 1 — Detection

* Introduce the intended misconfiguration in the isolated test bucket.
* Wait for AWS Config to evaluate the resource.
* Record the compliance result.

Test 2 — Event Delivery

* Confirm that EventBridge receives the relevant event.
* Check whether the configured rule matches it.
* Confirm that Lambda is invoked.

Test 3 — Remediation

* Inspect the Lambda execution logs.
* Confirm that the required S3 security settings were applied.
* Check whether the bucket policy was removed or whether that operation failed.

Test 4 — Alerting

* Confirm that the SNS Publish operation succeeded.
* Verify that the expected email arrived.

Test 5 — Final-State Verification

* Check the bucket’s Block Public Access settings.
* Inspect the bucket policy.
* Test the relevant access paths to verify that public access is blocked.

Test 6 — Failure Handling

* Test what happens if the SNS topic ARN is missing or invalid.
* Check what happens when the function cannot perform a remediation action.
* Confirm that failures are visible in the logs and do not produce misleading success notifications.
