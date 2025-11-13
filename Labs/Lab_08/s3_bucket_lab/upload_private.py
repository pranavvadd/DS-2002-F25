import boto3

# -------- CONFIGURATION --------
bucket_name = 'ds2002-f25-xta7yq'  # Your S3 bucket
local_file = 'banana2.jpeg'         # Local file to upload
s3_key = 'banana2_private.jpeg'     # Destination key in S3
region = 'us-east-1'

# -------- CREATE S3 CLIENT --------
s3 = boto3.client('s3', region_name=region)

# -------- UPLOAD FILE (PRIVATE) --------
try:
    s3.upload_file(
        Filename=local_file,  # local file path
        Bucket=bucket_name,   # S3 bucket name
        Key=s3_key            # S3 object key
        # No ACL = private by default
    )
    print(f"Successfully uploaded {local_file} to s3://{bucket_name}/{s3_key} (PRIVATE)")
except Exception as e:
    print("Error uploading file:", e)

# -------- GENERATE PRESIGNED URL --------
expires_in = 3600  # seconds (1 hour)
try:
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=expires_in
    )
    print("\nPresigned URL (expires in 1 hour):")
    print(presigned_url)
except Exception as e:
    print("Error generating presigned URL:", e)
