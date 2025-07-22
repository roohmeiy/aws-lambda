import boto3
import urllib.parse
import os
import subprocess
s3 = boto3.client('s3')

# Ensure /tmp is clean before each run
def cleanup_tmp():
    for file in os.listdir('/tmp'):
        os.remove(f"/tmp/{file}")

def download_file(bucket, key, local_path):
    s3.download_file(bucket, key, local_path)

def upload_file(local_path, bucket, key):
    s3.upload_file(local_path, bucket, key)

def transcode(input_path, output_path, resolution):
    width, height, bitrate = resolution
    command = [
        "/opt/bin/ffmpeg", "-i", input_path,
        "-vf", f"scale={width}:{height}",
        "-b:v", str(bitrate),
        "-c:a", "aac", "-b:a", "96k",
        "-y",  # Overwrite if exists
        output_path
    ]
    subprocess.run(command, check=True)

def lambda_handler(event, context):
    print("Event received:", event)

    if 'Records' not in event:
        return {'statusCode': 400, 'body': 'Not an S3 event'}

    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        if not key.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            continue

        base_filename = os.path.splitext(os.path.basename(key))[0]
        local_input = f"/tmp/input.mp4"
        download_file(source_bucket, key, local_input)

        resolutions = {
            "360p": (640, 360, "400k"),
            "480p": (854, 480, "800k"),
            "720p": (1280, 720, "1500k")
        }

        for label, res in resolutions.items():
            local_output = f"/tmp/{base_filename}_{label}.mp4"
            s3_output_key = f"transcoded/{base_filename}_{label}.mp4"

            try:
                transcode(local_input, local_output, res)
                upload_file(local_output, 'target-bucket', s3_output_key)
                print(f"Uploaded: {s3_output_key}")
            except subprocess.CalledProcessError as e:
                print(f"Error during transcoding {label}: {e}")

        cleanup_tmp()

    return {'statusCode': 200, 'body': 'Transcoding complete'}
