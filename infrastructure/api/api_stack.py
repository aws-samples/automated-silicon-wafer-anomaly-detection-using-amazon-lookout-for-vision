import cdk_nag as nag
from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from constructs import Construct

from infrastructure.api.api_stack_config import APIStackConfig
from infrastructure.api.constructs.lambda_construct import LambdaConstruct
from infrastructure.common.kms_construct import KMSConstruct


class APIStack(Stack):
    """APIStack class to deploy the AWS CDK stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Init the class
        Args:
            scope:                              The app construct
            construct_id:                       The name of the stack
        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        kms_key = KMSConstruct(
            self,
            "kms",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-lambda",
        ).key

        lambda_function = LambdaConstruct(
            self,
            "lambda",
            kms_key=kms_key,
            initial_policy=[
                iam.PolicyStatement(
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    resources=[
                        "arn:aws:logs:*:*:log-group:*",
                        "arn:aws:logs:*:*:log-group:*:log-stream:*",
                    ],
                ),
                iam.PolicyStatement(
                    actions=[
                        "lookoutvision:DetectAnomalies",
                    ],
                    resources=[
                        "arn:aws:lookoutvision:*:*:model/*/*",
                    ],
                ),
            ],
            **APIStackConfig.lambda_kwargs,
        ).lambda_function

        ## Nag Suppresions
        nag.NagSuppressions.add_resource_suppressions(
            construct=[lambda_function],
            suppressions=[
                nag.NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="Use AWS managed policies CodeBuild Project with defaults from cdk",
                ),
                nag.NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="Use AWS managed policies",
                ),
            ],
            apply_to_children=True,
        )
