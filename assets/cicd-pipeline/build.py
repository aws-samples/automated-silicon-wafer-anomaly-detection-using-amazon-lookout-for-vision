import argparse
import json
import logging
import os

# Import all the libraries needed to get started:
from lookoutvision.image import Image
from lookoutvision.lookoutvision import LookoutForVision
from lookoutvision.manifest import Manifest
from lookoutvision.metrics import Metrics

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", type=str, default=os.environ.get("LOGLEVEL", "INFO").upper())
    parser.add_argument("--input-bucket", type=str, required=True)
    parser.add_argument("--project-name", type=str, required=True)
    parser.add_argument("--model-version", type=str, required=True)
    parser.add_argument("--output-bucket", type=str, required=True)
    args, _ = parser.parse_known_args()

    # Configure logging to output the line number and message
    log_format = "%(levelname)s: [%(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(format=log_format, level=args.log_level)

    # Training
    input_bucket = args.input_bucket
    project_name = args.project_name
    model_version = args.model_version
    output_bucket = args.output_bucket

    logger.info(f"Input bucket: {input_bucket}.")
    logger.info(f"Project name: {project_name}.")
    logger.info(f"Model version: {model_version}.")
    logger.info(f"Output bucket: {output_bucket}.")

    logger.info("Initialize classes.")
    img = Image()
    mft = Manifest(
        bucket=input_bucket,
        s3_path="{}/".format(project_name),
        datasets=["training", "validation"])
    l4v = LookoutForVision(project_name=project_name)
    met = Metrics(project_name=project_name)

    logger.info("Create project.")
    p = l4v.create_project()
    logger.info(p)

    logger.info("Check images sizes.")
    sizes = img.check_image_sizes(verbose=False)
    logger.info(sizes)

    logger.info("Check images shapes.")
    shapes = img.check_image_shapes(verbose=False)
    logger.info(shapes)

    logger.info("Upload from local.")
    img.upload_from_local(
        bucket=input_bucket,
        s3_path="{}/".format(project_name),
        train_and_test=True,
        test_split=0.2,
        prefix="")

    logger.info("Push manifest file.")
    mft_resp = mft.push_manifests()
    logger.info(mft_resp)

    logger.info("Create dataset.")
    dsets = l4v.create_datasets(mft_resp, wait=True)
    logger.info(dsets)

    logger.info("Fit...")
    l4v.fit(
        output_bucket=output_bucket,
        model_prefix="model_",
        wait=True)

    logger.info("Deploy...")
    l4v.deploy(
        model_version=model_version,
        wait=True)
