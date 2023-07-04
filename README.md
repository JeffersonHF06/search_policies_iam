# Search AWS IAM Policies by Action
This is a Python script that returns the name of the IAM policies based on the actions they contain, for example, by default it searches all the User Managed Policies with actions related to RDS.

## Requirements to run the script:
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- Python 3 (I recommend to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions easily).
- Permissions to access an AWS account and use IAM.

## How to use it
- Login into AWS using the CLI of your computer.
- Run the next command: 
```python3 search_policies.py```
