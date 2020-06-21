# covid19datapuller SAM demo

This demo will get you up and running with the [AWS SAM (Serverless Application Model)](https://aws.amazon.com/serverless/sam/) with an example AWS lambda (python3) function that pulls public data from http://coronavirusapi.com/ every `60` minutes, and writes it to an s3 bucket under `[bucketname]/[fetch-timestamp]/data.json`

## Prerequisites

* Docker Desktop (https://docs.docker.com/desktop/)
* Python 3.x & pip 3.x
* AWS cli w/ configured credentials with the appropriate access to create s3 buckets, lambda functions, cloudformation stacks, cloudwatch events etc.

## Setup

Osx, install via brew:
```
brew tap aws/tap
brew install aws-sam-cli
```

Verify installed version:
```
sam --version
```

Create the S3 bucket where SAM will upload its artifacts:
```
aws --region us-east-1 s3 mb s3://sam-covid19datapuller
```

Build the app:
```
sam build 
```

Deploy to "dev"
```
sam deploy \
  --parameter-overrides "ParameterKey=Env,ParameterValue=dev ParameterKey=Version,ParameterValue=1.0.0" \
  --stack-name covid19datapuller-dev
```

Deploy to "prod"
```
sam deploy \
  --parameter-overrides "ParameterKey=Env,ParameterValue=prod ParameterKey=Version,ParameterValue=1.0.0" \
  --stack-name covid19datapuller-prod
```

## Notes

Once up and running you can checkout the created items in the follow AWS services. Be sure to verify that your region matches the region in your local AWS creds file which in-turn is the region where serverless will deploy everything to.

* https://console.aws.amazon.com/events (click on events -> rules)
  * There will be 2 `covid19datapuller-[dev|prod]` event triggers created for both the dev/prod functions (every 60m, you can change this in `template.yaml`)
  
* https://s3.console.aws.amazon.com/s3/home
  * There will be 2 `covid19datapuller-bucket-[dev|prod]` buckets created, one for each dev/prod function, where the pulled data will be written in JSON format and annotated w/ the function version and timestamp the data was pulled. (every 60m)
  
* https://console.aws.amazon.com/lambda
  * There should be 2 `covid19datapuller-[dev|prod]` functions, one for each serverless "stage" (dev/prod)

* https://console.aws.amazon.com/cloudformation/home
    * There should be 2 `covid19datapuller-[dev|prod]` stacks, one for each dev/prod serverless app
  
* https://console.aws.amazon.com/iam/home (look in roles)
  * There should be ONE `covid19datapuller-[dev|prod]` role with appropriate permissions. 

## Cleanup
```
aws --region us-east-1 cloudformation delete-stack --stack-name covid19datapuller-dev
aws --region us-east-1 cloudformation delete-stack --stack-name covid19datapuller-prod
```

## Errate

You can create 7 types of CF things represented by these higher level abstractions in the SAM spec + any other lower-level CF resource types

* `AWS::Serverless::Api`: Documents the API via openapi spec. Implicitly created via any AWS::Serverless::Function
  
* `AWS::Serverless::Application`: Embeds/refs a named serverless application as a nested app from a published ref the SAM app repository or an S3 bucket 
  
* `AWS::Serverless::Function`: defines a lambda function to be created referencing the local `CodeUri` of a folder in the project 

* `AWS::Serverless::HttpApi`: API gateway definition, might also be created automatically if your `AWS::Serverless::Function` declares an event of type `Api`

* `AWS::Serverless::LayerVersion`: Creates a lambda layer, reference local or remote s3 repo where this lives

* `AWS::Serverless::SimpleTable`: Creates a DynamoDB table with a single attribute primary key

* `AWS::Serverless::StateMachine`: Creates an AWS Step Functions state machine
