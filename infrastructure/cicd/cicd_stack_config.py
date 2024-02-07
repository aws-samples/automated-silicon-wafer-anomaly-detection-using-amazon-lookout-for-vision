from typing import TypedDict

import aws_cdk as cdk
from aws_cdk import aws_codebuild as codebuild

from utils.stack_config import StackConfig


class CodecommitKwargs(TypedDict):
    dir_name: str
    branch_name: str


class CodebuildKwargs(TypedDict):
    timeout: cdk.Duration
    build_image_id: str
    build_image_compute_type: codebuild.ComputeType


class CodepipelineKwargs(TypedDict):
    branch_name: str
    code_build_clone_output: bool


class CICDStackConfig:
    def _map_compute_types(compute_type: str):
        """Map the compute types
        Args:
            compute_type:       The compute type (Options: "small", "medium", "large", "x2_large")
        Returns:
            codebuild.ComputeType
        """
        return {
            "small": codebuild.ComputeType.SMALL,
            "medium": codebuild.ComputeType.MEDIUM,
            "large": codebuild.ComputeType.LARGE,
            "x2_large": codebuild.ComputeType.X2_LARGE,
        }[compute_type]

    config = StackConfig.load_config(__file__)

    codecommit_kwargs: CodecommitKwargs = {
        "dir_name": config["codecommit"]["dir_name"],
        "branch_name": config["codecommit"]["branch_name"],
    }

    codebuild_kwargs: CodebuildKwargs = {
        "timeout": cdk.Duration.hours(
            int(config["codebuild"]["timeout_in_hours"])
        ),
        "build_image_id": config["codebuild"]["build_image_id"],
        "build_image_compute_type": _map_compute_types(
            config["codebuild"]["build_image_compute_type"]
        ),
    }

    codepipeline_kwargs: CodepipelineKwargs = {
        "branch_name": config["codepipeline"]["branch_name"],
        "code_build_clone_output": bool(
            config["codepipeline"]["code_build_clone_output"]
        ),
    }
