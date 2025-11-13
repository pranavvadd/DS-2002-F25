#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    exit 1
fi

FILE=$1
BUCKET=$2
EXPIRE=$3

echo "Uploading $FILE to s3://$BUCKET/ ..."
aws s3 cp "$FILE" "s3://$BUCKET/"

echo "Generating presigned URL (expires in $EXPIRE seconds)..."
URL=$(aws s3 presign "s3://$BUCKET/$(basename "$FILE")" --expires-in "$EXPIRE")

echo ""
echo "=============================="
echo "Presigned URL:"
echo "$URL"
echo "=============================="
echo ""
