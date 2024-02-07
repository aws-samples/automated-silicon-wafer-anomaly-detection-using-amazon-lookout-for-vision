import cdk_nag as nag
from aws_cdk import Stack
from constructs import Construct

from infrastructure.cicd.cicd_stack_config import CICDStackConfig
from infrastructure.cicd.constructs.codebuild_construct import \
    CodeBuildConstruct
from infrastructure.cicd.constructs.codecommit_construct import \
    CodeCommitConstruct
from infrastructure.cicd.constructs.codepipeline_construct import \
    CodePipelineConstruct
from infrastructure.cicd.constructs.iam_codebuild_construct import \
    IAMCodeBuildConstruct
from infrastructure.cicd.constructs.s3_construct import S3Construct
from infrastructure.common.kms_construct import KMSConstruct
from utils.environment import Environment


class CICDStack(Stack):
    """CICDStack class to deploy the AWS CDK stack."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ):
        """Initialize the class.

        Args:
            scope:                     The AWS CDK app that is deployed
            construct_id:              The construct ID visible on the CloudFormation console for this resource

        Returns:
            No return
        """
        super().__init__(scope, construct_id, **kwargs)

        s3_kms_key = KMSConstruct(
            self,
            "kms-s3",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-s3",
        ).key

        artifact_bucket = S3Construct(
            self,
            "s3",
            bucket_name=f"{construct_id}-{self.account}-{self.region}",
            kms_key=s3_kms_key,
        ).bucket

        codebuild_kms_key = KMSConstruct(
            self,
            "kms-codebuild",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-cb",
        ).key

        codebuild_role = IAMCodeBuildConstruct(
            self,
            "iam-codebuild",
            region=self.region,
            account=self.account,
            bucket_name=artifact_bucket.bucket_name,
        ).codebuild_role

        repository = CodeCommitConstruct(
            self,
            "codecommit",
            repository_name=f"{construct_id}-repository",
            **CICDStackConfig.codecommit_kwargs,
        ).repository

        codebuild_project = CodeBuildConstruct(
            self,
            "codebuild",
            project_name=construct_id,
            codebuild_role=codebuild_role,
            environment_variables={
                "INPUT_BUCKET": artifact_bucket.bucket_name,
                "PROJECT_NAME": Environment.PROJECT_NAME,
                "MODEL_VERSION": "1",
                "OUTPUT_BUCKET": artifact_bucket.bucket_name,
            },
            repository=repository,
            kms_key=codebuild_kms_key,
            **CICDStackConfig.codebuild_kwargs,
        ).project

        code_pipeline_construct = CodePipelineConstruct(
            self,
            "codepipeline",
            pipeline_name=construct_id,
            repository=repository,
            artifact_bucket=artifact_bucket,
            **CICDStackConfig.codepipeline_kwargs,
        )

        code_pipeline_construct.add_build_stage(
            stage_name="Deploy",
            codebuild_project=codebuild_project,
        )

        ## Nag Suppresions
        nag.NagSuppressions.add_resource_suppressions(
            construct=[
                codebuild_role,
                codebuild_project,
                code_pipeline_construct,
            ],
            suppressions=[
                nag.NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="Use AWS managed policies CodeBuild Project with defaults from cdk",
                )
            ],
            apply_to_children=True,
        )
