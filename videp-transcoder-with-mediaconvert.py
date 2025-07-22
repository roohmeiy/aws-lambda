import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))  # Debug
    
    if 'Records' not in event:
        print("No Records found - this is not an S3 event")
        return {'statusCode': 400, 'body': 'Not an S3 event'}
    
    # Initialize MediaConvert client with endpoint
    mediaconvert = boto3.client('mediaconvert')
    endpoint = mediaconvert.describe_endpoints()['Endpoints'][0]['Url']
    mc = boto3.client('mediaconvert', endpoint_url=endpoint)
    
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        if not key.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            continue
        
        filename = key.rsplit('.', 1)[0]

        audio_description = {
            'AudioSourceName': 'Audio Selector 1',
            'CodecSettings': {
                'Codec': 'AAC',
                'AacSettings': {
                    'Bitrate': 96000,
                    'CodingMode': 'CODING_MODE_2_0',
                    'SampleRate': 48000
                }
            }
        }

        job = {
            'Role': 'arn:aws:iam::ACCOUNT:role/MediaCOnvert',
            'Settings': {
                'Inputs': [{
                    'FileInput': f's3://{source_bucket}/{key}',
                    'AudioSelectors': {
                        'Audio Selector 1': {
                            'DefaultSelection': 'DEFAULT'
                        }
                    }
                }],
                'OutputGroups': [{
                    'OutputGroupSettings': {
                        'Type': 'FILE_GROUP_SETTINGS',
                        'FileGroupSettings': {
                            'Destination': 's3://target-bucket/'
                        }
                    },
                    'Outputs': [
                        {
                            'NameModifier': f'_360p',
                            'VideoDescription': {
                                'Width': 640,
                                'Height': 360,
                                'CodecSettings': {
                                    'Codec': 'H_264',
                                    'H264Settings': {
                                        'Bitrate': 400000
                                    }
                                }
                            },
                            'AudioDescriptions': [audio_description],
                            'ContainerSettings': {
                                'Container': 'MP4'
                            }
                        },
                        {
                            'NameModifier': f'_480p',
                            'VideoDescription': {
                                'Width': 854,
                                'Height': 480,
                                'CodecSettings': {
                                    'Codec': 'H_264',
                                    'H264Settings': {
                                        'Bitrate': 800000
                                    }
                                }
                            },
                            'AudioDescriptions': [audio_description],
                            'ContainerSettings': {
                                'Container': 'MP4'
                            }
                        },
                        {
                            'NameModifier': f'_720p',
                            'VideoDescription': {
                                'Width': 1280,
                                'Height': 720,
                                'CodecSettings': {
                                    'Codec': 'H_264',
                                    'H264Settings': {
                                        'Bitrate': 1500000
                                    }
                                }
                            },
                            'AudioDescriptions': [audio_description],
                            'ContainerSettings': {
                                'Container': 'MP4'
                            }
                        }
                    ]
                }]
            }
        }

        response = mc.create_job(**job)
        print(f"Job created: {response['Job']['Id']}")
    
    return {'statusCode': 200}
