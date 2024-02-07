from typing import Dict, List

from aws_cdk import Duration
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_signer as signer
from constructs import Construct


class LambdaConstruct(Construct):
    """LambdaConstruct class to construct Lambda.

    Attributes:
    :lambda_function:       The Lambda CDK object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_variables: Dict[str, str],
        initial_policy: List[iam.PolicyStatement],
        kms_key: kms.Key,
        code_dir: str = "api",
        handler: str = "app.lambda_handler",
        timeout: Duration = Duration.seconds(15),
        memory_size: int = 128,
        **kwargs,
    ) -> None:
        """Initialize class

        Args:
            function_name:          The name of the Lambda function
            environment_variables:  The Lambda environmental variables
            initial_policy:         The list of IAM PolicyStatements
            kms_key:                The KMS key for encryption
            code_dir:               The directory name with code
            handler:                The entry Lambda handler path
            timeout:                The number of minutes for timeout
            memory_size:            The memory size in MB

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        code_signing_config = _lambda.CodeSigningConfig(
            self,
            "code-signing-config",
            signing_profiles=[
                signer.SigningProfile(
                    self,
                    "signing-profile",
                    platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA,
                )
            ],
        )

        self.lambda_function = _lambda.Function(
            self,
            "function",
            code_signing_config=code_signing_config,
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler=handler,
            code=_lambda.Code.from_asset(f"assets/lambda/{code_dir}"),
            timeout=timeout,
            memory_size=memory_size,
            environment_encryption=kms_key,
            initial_policy=initial_policy,
            environment=environment_variables,
        )
