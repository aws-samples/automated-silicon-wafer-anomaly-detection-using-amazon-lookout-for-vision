#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.cicd.cicd_stack import CICDStack


class TestCICDStack:
    def test_cicd_resources(self):
        app = cdk.App()
        lookout_stack = CICDStack(
            scope=app,
            construct_id="cicd-stack",
        )
        template = cdk.assertions.Template.from_stack(lookout_stack)
        template.resource_count_is("AWS::KMS::Key", 2)
        template.resource_count_is("AWS::KMS::Alias", 2)
        template.resource_count_is("AWS::S3::Bucket", 1)
        template.resource_count_is("AWS::S3::BucketPolicy", 2)
        template.resource_count_is("AWS::IAM::Policy", 4)
        template.resource_count_is("AWS::IAM::Role", 4)
        template.resource_count_is("AWS::CodeBuild::Project", 1)
        template.resource_count_is("AWS::CodeCommit::Repository", 1)
        template.resource_count_is("AWS::CodePipeline::Pipeline", 1)
        template.resource_count_is("AWS::Events::Rule", 1)
