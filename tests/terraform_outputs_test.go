package tests

import (
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestTerraformOutputs(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../",
	}

	terraform.InitAndPlan(t, terraformOptions)

	templateRepositoryOutput := terraform.Output(t, terraformOptions, "bucket_arn")
	assert.IsType(t, "string", templateRepositoryOutput)
}
