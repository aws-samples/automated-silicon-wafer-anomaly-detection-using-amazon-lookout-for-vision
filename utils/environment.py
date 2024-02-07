import os
from typing import Any


class Environment:
    """Environment class to read and store env vars.

    Attributes:
    :PROJECT_NAME:          The project name
    :RUN_NAG:               The flag whether nag runs or not
    :AWS_REGION:            The AWS region
    :AWS_ACCOUNT_ID:        The AWS account id
    """

    def _read_env_variable(variable_name: str, default_value: Any = None):
        """Read environment variables

        Args:
            variable_name:          The name of the variable
            default_value:          The default value

        Returns:
            value:                  The env var defined
        """
        value = os.environ.get(variable_name, default_value)
        if value:
            return value
        raise KeyError(f"Variable {variable_name} is not defined")

    PROJECT_NAME: str = _read_env_variable(
        "PROJECT_NAME", "amazon-l4v-project"
    )

    AWS_REGION: str = _read_env_variable("CDK_DEFAULT_REGION")
    AWS_ACCOUNT_ID: str = _read_env_variable("CDK_DEFAULT_ACCOUNT")
