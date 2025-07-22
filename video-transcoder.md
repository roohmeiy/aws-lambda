### lambda execution role
```yaml
lambda exec role-

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
			"Resource": "arn:aws:s3:::target-aesthisia/*"
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

### media convert role-
```yaml
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
				"arn:aws:s3:::source-aesthisia",
				"arn:aws:s3:::source-aesthisia/*",
				"arn:aws:s3:::target-aesthisia",
				"arn:aws:s3:::target-aesthisia/*"
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
