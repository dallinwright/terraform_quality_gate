# Terraform Quality Gate
![Publish](https://github.com/dallinwright/terraform_quality_gate/workflows/Publish/badge.svg?branch=master)

Terraform quality gate for Infrastructure-as-Code

### Example usage

###### Terraform Cloud
```yaml
- name: Terraform Quality Gate
  uses: dallinwright/terraform_quality_gate@v0.0.2
  with:
    terratest: terraform_cloud
    terraform_cloud_token: 'xxxxxxxxxxxxxxxxxxxxxx'
```

###### AWS
```yaml
- name: Terraform Quality Gate
  uses: dallinwright/terraform_quality_gate@v0.0.2
  with:
    terratest: AWS
    aws_access_key_id: 'xxxxxxxxxxxxxxxxxxxxxx'
    aws_secret_access_key: 'xxxxxxxxxxxxxxxxxx'
```


### Arguments
terratest: `AWS` or `terraform_cloud`
terraform_cloud_token: Terraform token obtained from terraform login. Used for writing auth file as required. We suggest storing it in a github secret. Required if using terratest full.

### Purpose

This docker image and subsequent github action encapsulate various stages and best practices common to infrastructure CI and CD. Mainly the current iteration addresses the following.

#### Linting
By using the build in `terraform fmt -check` command, we verify that the file is tidy, complies to terraform file format standards, and does not contain any easy to spot syntax errors.

#### Static Anlysis
Linting catches style errors but it very limited in scope, to this end, we implement the tool [tflint](https://github.com/terraform-linters/tflint).

This tool goes much further and can spot compilation and errors in how terraform will extrapolate values and calculate various things. This tool is indespensable in the CI process.

#### Roadmap
Adding flexibility to other remote backends besides terraform cloud.
Adding unit/integration testing for `entrypoint.py`