#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.api.api_stack import APIStack


class TestAPIStack:
    def test_api_resources(self):
        app = cdk.App()
        api_stack = APIStack(
            scope=app,
            construct_id="api-stack",
        )
        template = cdk.assertions.Template.from_stack(api_stack)
        template.resource_count_is("AWS::KMS::Key", 1)
        template.resource_count_is("AWS::KMS::Alias", 1)
        template.resource_count_is("AWS::IAM::Policy", 1)
        template.resource_count_is("AWS::IAM::Role", 1)
        template.resource_count_is("AWS::Signer::SigningProfile", 1)
        template.resource_count_is("AWS::Lambda::CodeSigningConfig", 1)
        template.resource_count_is("AWS::Lambda::Function", 1)
