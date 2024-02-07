from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as actions
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct


class CodePipelineConstruct(Construct):
    """CodePipelineConstruct class to construct a CodePipeline project.

    Attributes:
    :pipeline:              The CodePipeline CDK project object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        pipeline_name: str,
        repository: codecommit.Repository,
        artifact_bucket: s3.Bucket,
        branch_name: str = "main",
        code_build_clone_output: bool = True,
        **kwargs
    ) -> None:
        """
        Args:
            scope:                          The app construct
            construct_id:                   The name of the stack
            pipeline_name:                  The name of the project
            repository:                     The CodeCommit repository
            artifact_bucket:                The S3 bucket CDK object
            branch_name:                    The branch to be leveraged
            code_build_clone_output:        The indication if code build will clone output

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self._source_output = codepipeline.Artifact()

        # create code pipeline with source stage
        self.pipeline = codepipeline.Pipeline(
            self,
            "codepipeline-project",
            pipeline_name=pipeline_name,
            artifact_bucket=artifact_bucket,
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        actions.CodeCommitSourceAction(
                            action_name="Codecommit_Source",
                            output=self._source_output,
                            branch=branch_name,
                            repository=repository,
                            code_build_clone_output=code_build_clone_output,
                        )
                    ],
                )
            ],
        )

    def add_build_stage(
        self,
        stage_name: str,
        codebuild_project: codebuild.Project,
    ) -> None:
        self.pipeline.add_stage(
            stage_name=stage_name,
            actions=[
                actions.CodeBuildAction(
                    action_name="Deploy",
                    project=codebuild_project,
                    input=self._source_output,
                    outputs=[codepipeline.Artifact()],
                )
            ],
        )
