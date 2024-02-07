from aws_cdk import aws_iam as iam
from constructs import Construct


class IAMCodeBuildConstruct(Construct):
    """IAMCodeBuildConstruct class with roles for this particular project.

    Attributes:
    :codebuild_role:               The IAM Role for CodeBuild
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        region: str,
        account: str,
        bucket_name: str,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            region:                 The region of the stack
            account:                The account id of the stack
            bucket_name:            The S3 bucket name for artifacts

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        # Define the IAM role
        self.codebuild_role = iam.Role(
            self,
            "codebuild-role",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            description="This role ensures CodeBuild has the right access rights to deploy in the use case account.",
            inline_policies={
                "codebuild-inline": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "lookoutvision:DescribeProject",
                                "lookoutvision:CreateProject",
                                "lookoutvision:DeleteDataset",
                                "lookoutvision:CreateDataset",
                                "lookoutvision:DescribeDataset",
                                "lookoutvision:CreateModel",
                                "lookoutvision:DescribeModel",
                                "lookoutvision:StartModel",
                                "lookoutvision:DetectAnomalies",
                                "lookoutvision:StopModel",
                                "lookoutvision:ListDatasetEntries",
                                "lookoutvision:ListModels",
                                "lookoutvision:DeleteModel",
                                "lookoutvision:DeleteProject",
                            ],
                            resources=[
                                "*",
                            ],
                        ),
                        iam.PolicyStatement(
                            actions=[
                                "s3:GetObject*",
                                "s3:GetBucket*",
                                "s3:List*",
                                "s3:DeleteObject*",
                                "s3:PutObject",
                                "s3:PutObjectLegalHold",
                                "s3:PutObjectRetention",
                                "s3:PutObjectTagging",
                                "s3:PutObjectVersionTagging",
                            ],
                            resources=[
                                f"arn:aws:s3:::{bucket_name}",
                                f"arn:aws:s3:::{bucket_name}/*",
                            ],
                        ),
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
                    ],
                ),
            },
        )
