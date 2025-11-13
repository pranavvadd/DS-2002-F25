import boto3
import requests

bucket_name = 'ds2002-f25-xta7yq'
local_file = 'apples2.jpg'
s3_key = 'uploads/apples2.jpg'
expires_in = 3600  # 1 hour

url = 'https://cdn.britannica.com/22/187222-050-07B17FB6/apples-on-a-tree-branch.jpg'
r = requests.get(url)
with open(local_file, 'wb') as f:
    f.write(r.content)

s3 = boto3.client('s3', region_name='us-east-1')
s3.upload_file(local_file, bucket_name, s3_key)

url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': s3_key},
    ExpiresIn=expires_in
)
print("Presigned URL:", url)
