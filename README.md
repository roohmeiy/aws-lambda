- RESOURCE POLICY -> WHO CAN TRIGGER
  - LAMBDA IN VPC- PVT SUBNET + NAT GATEWAY

- Reserved Concurrency: 
  - Limits the maximum number of concurrent executions for a Lambda function.
  - Reserves that amount exclusively for that function (so no other Lambda can use it).

- Provisioned Concurrency:
  - Pre-warms execution environments and keeps them ready to respond instantly.
  - Eliminates cold starts for the specified number of instances.
