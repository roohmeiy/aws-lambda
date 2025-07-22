### ✅ Lambda Execution Role Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::source-aesthisia/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::target-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::368677659604:role/MediaCOnvert"
    },
    {
      "Effect": "Allow",
      "Action": [
        "mediaconvert:*"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### ✅ MediaConvert Role Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowMediaConvertS3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::source-bucket",
        "arn:aws:s3:::source-bucket/*",
        "arn:aws:s3:::target-bucket",
        "arn:aws:s3:::target-bucket/*"
      ]
    },
    {
      "Sid": "AllowMediaConvert",
      "Effect": "Allow",
      "Action": "mediaconvert:*",
      "Resource": "*"
    }
  ]
}
```

