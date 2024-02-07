from typing import Dict, TypedDict, Union

import aws_cdk as cdk

from utils.stack_config import StackConfig


class LambdaKwargs(TypedDict):
    code_dir: str
    environment_variables: Dict[str, str]
    handler: str
    timeout: cdk.Duration
    memory_size: int


class APIStackConfig:
    config = StackConfig.load_config(__file__)

    lambda_kwargs: LambdaKwargs = {
        "code_dir": config["lambda"]["code_dir"],
        "environment_variables": {
            "PROJECT_NAME": StackConfig.environment.PROJECT_NAME,
        },
        "handler": config["lambda"]["handler"],
        "timeout": cdk.Duration.seconds(
            int(config["lambda"]["timeout_in_seconds"])
        ),
        "memory_size": int(config["lambda"]["memory_size"]),
    }
