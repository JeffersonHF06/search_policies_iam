import boto3
import json

# Create an IAM client
client = boto3.client('iam')

paginator = client.get_paginator('list_policies')
result = paginator.paginate(
    Scope = 'Local',
    PaginationConfig={
        'MaxItems': 1000,
        'PageSize': 100,
    }
)

rds_policies = []
for iterator in result:
    policies = iterator['Policies']
    for policy in policies:
        policy_info = client.get_policy(PolicyArn=policy['Arn'])
        policy_default_version = client.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy_info['Policy']['DefaultVersionId'])
        statement = policy_default_version['PolicyVersion']['Document']['Statement']
        for object in statement:
            if 'Action' in object:
                if not isinstance(object, str):
                    if isinstance(object['Action'], str):
                        if 'rds:' in object['Action']:
                            if not policy['PolicyName'] in rds_policies:
                                    rds_policies.append(policy['PolicyName'])
                    else:
                        for x in object['Action']:
                            if 'rds:' in x:
                                if not policy['PolicyName'] in rds_policies:
                                    rds_policies.append(policy['PolicyName'])

print(rds_policies)