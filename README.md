# Terraform Quality Gate
![Publish](https://github.com/OptionAlpaca/terraform_quality_gate/workflows/Publish/badge.svg?branch=master)

Terraform quality gate for Infrastructure-as-Code

### Example usage

```yaml
- name: Terraform Quality Gate
  uses: OptionAlpaca/terraform_quality_gate@0.1.1
  with:
    terratest: 'full'
```

### Arguments
terratest: `none` or `full`

### Purpose

This docker image and subsequent github action encapsulate various stages and best practices common to infrastructure CI and CD. Mainly the current iteration addresses the following.

#### Linting
By using the build in `terraform fmt -check` command, we verify that the file is tidy, complies to terraform file format standards, and does not contain any easy to spot syntax errors.

#### Static Anlysis
Linting catches style errors but it very limited in scope, to this end, we implement the tool [tflint](https://github.com/terraform-linters/tflint).

This tool goes much further and can spot compilation and errors in how terraform will extrapolate values and calculate various things. This tool is indespensable in the CI process.

#### Future Stages
In development is the integration of [`terratest`](https://github.com/gruntwork-io/terratest) integration testing library. By supplying valid AWS credentials (only planned on supported provider) you can test your infrastructure implmentations and see the speed, quality, and outcomes you can expect without deploying the infrastructure directly to your target environments.
