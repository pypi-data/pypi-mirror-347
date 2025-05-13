"""Test downloading AWS SmartDS dataset."""

from dsloader.case.smartds import (
    build_smartds_model_prefix,
    download_aws_smartds_dataset,
    build_smartds_profile_prefix,
)


def test_download_aws_smartds_dataset_model(tmp_path):
    prefix = build_smartds_model_prefix(
        year=2018,
        area="SFO",
        version="v1.0",
        region="P1U",
        folder="opendss",
        feeder="p1uhs0_1247/p1uhs0_1247--p1udt1469",
    )
    download_aws_smartds_dataset(prefix, target_folder=tmp_path)


def test_download_aws_smartds_dataset_profile(tmp_path):
    prefix = build_smartds_profile_prefix(2018, "SFO", "v1.0", "P1U")
    download_aws_smartds_dataset(prefix, target_folder=tmp_path)
