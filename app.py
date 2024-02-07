#!/usr/bin/env python3

import aws_cdk as cdk
import cdk_nag as nag

from infrastructure.api.api_stack import APIStack
from infrastructure.cicd.cicd_stack import CICDStack
from utils.environment import Environment

# --------------------------------
# Set stack environment variables
# --------------------------------

PROJECT_NAME = Environment.PROJECT_NAME
ENV = cdk.Environment(
    account=Environment.AWS_ACCOUNT_ID, region=Environment.AWS_REGION
)

# --------------------------------
# Initialize App
# --------------------------------

app = cdk.App()

# --------------------------------
# Lookout for Vision CICD
# --------------------------------

lookout_stack = CICDStack(
    scope=app,
    construct_id=f"{PROJECT_NAME}-cicd",
    env=ENV,
)

# --------------------------------
# Lambda Integration
# --------------------------------
api_stack = APIStack(
    scope=app,
    construct_id=f"{PROJECT_NAME}-api",
    env=ENV,
)

# --------------------------------

cdk.Aspects.of(app).add(nag.AwsSolutionsChecks())
cdk.Tags.of(app).add("project", PROJECT_NAME)
app.synth()
