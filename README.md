# docdb-autoscaling

An auto-scaling solution for Amazon DocumentDB.

[Amazon DocumentDB (with MongoDB compatibility)](https://aws.amazon.com/documentdb/) supports up to 15 Read Replicas, but by default AWS does not provide an easy way to set up an auto-scaling policy for them.

This script is an implementation of auto-scaling write in Python and supported by AWS Lambda. You can easily deploy and configure this script using Terraform.

## Solution

![Architecture diagram](./assets/diagram.png)
