import boto3
import json

# Create an IAM client
client = boto3.client('iam')

# Function to filter the policies
def filter_policies(scope = 'Local', max_items = 1000, action = 'rds'):

    # Get the policies with pagination
    paginator = client.get_paginator('list_policies')
    result = paginator.paginate(
        Scope = scope,
        PaginationConfig={
            'MaxItems': max_items,
            'PageSize': 100,
        }
    )

    # Iterate on the policies and filter them with the Action search criteria
    policies_result_list = []
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
                            if action+':' in object['Action']:
                                if not policy['PolicyName'] in policies_result_list:
                                        policies_result_list.append(policy['PolicyName'])
                        else:
                            for x in object['Action']:
                                if action+':' in x:
                                    if not policy['PolicyName'] in policies_result_list:
                                        policies_result_list.append(policy['PolicyName'])

    # Print the list of names of the found policies
    print(policies_result_list)

# Menus to set configurations
scope = {
    '1': "Local",
    '2': "AWS",
    '3': "All"
}

print("Select the scope of the IAM policies:")
print("1.User Managed")
print("2.AWS Managed")
print("3.All")
choice_scope = input("Choice: ").rstrip()

while int(choice_scope) < 1 or int(choice_scope) > 3:
    choice_scope = input("Invalid Input, please try again: ").rstrip()

selected_scope = scope[choice_scope]

max_items = input("Set the max number of policies to retrieve: ")

action = input("What is the action (service) to look into the policies permissions? ")


filter_policies(selected_scope, max_items, action)


