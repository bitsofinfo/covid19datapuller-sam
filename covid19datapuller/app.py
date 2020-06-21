import json
import os
import sys
import uuid
import datetime
import re

import boto3
import requests


def fetch(event, context):

    headers = {
        'Accept': "*/*",
        'Cache-Control': "no-cache"
    }

    response = requests.get("http://coronavirusapi.com/getTimeSeriesJson/NY", headers=headers)
    records = json.loads(response.text)

    timestampStr = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    timestampDir = re.sub('[^0-9a-zA-Z]+', '-', timestampStr)

    version = os.getenv("VERSION")

    decorated = { 
        "version" : version,
        "fetchedAt" : timestampStr,
        "data" : records
    }

    s3 = boto3.client('s3')
    s3.put_object(Bucket=os.getenv("TARGET_BUCKET"),
                  Key=(timestampDir+'/data.json'),
                  Body=str.encode(json.dumps(decorated, sort_keys=True, indent=4)),
                  ServerSideEncryption='AES256')

    return {
        "statusCode": 200,
        "version" : version,
        "sourceEvent": event
    }

