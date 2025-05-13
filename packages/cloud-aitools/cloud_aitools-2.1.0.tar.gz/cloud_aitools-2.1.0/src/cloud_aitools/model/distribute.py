import logging
from pathlib import Path

from ..handler.cos_handler import COSHandler
from .models import ModelBucket, RemoteObjectIndex, ModelIndex, UploadObject

logger = logging.getLogger(__name__)


def generate_bucket_name(bucket_template: str, region: str, bucket_index: int) -> str:
    *parts, appid = bucket_template.split("-")
    return f"{'-'.join(parts)}-{region}-{bucket_index}-{appid}"


def generate_buckets(bucket_template: str, bucket_num: int):
    *parts, appid = bucket_template.split("-")

    res = []
    for i in range(bucket_num):
        bucket_name = f"{'-'.join(parts)}-{i}-{appid}"
        res.append(bucket_name)
        logger.debug("Generated bucket: %s", bucket_name)

    logger.info("Generated %d buckets with template: %s", bucket_num, bucket_template)
    return res


def distribute_objects(buckets: str, files: list[Path]) -> dict[str, list[Path]]:
    res = {}

    logger.debug("Distributing %d files across %d buckets", len(files), len(buckets))
    for i, bucket in enumerate(buckets):
        for filepath in files[i :: len(buckets)]:
            res.setdefault(bucket, []).append(filepath)
            logger.debug("Assigned file %s to bucket %s", filepath.name, bucket)

    logger.info("Distributed files to buckets: %s", list(res.keys()))
    return res


def get_relative_path(filepath: Path, local_parent_dir: Path) -> str:
    return str(filepath.absolute().relative_to(local_parent_dir))


def gen_object_key(object_prefix: str, path: str) -> str:
    return f"{object_prefix}/{path}"


def generate_upload_info(
    buckets, files: list[Path], object_prefix: str, local_parent_dir: Path
) -> list[UploadObject]:
    res = []
    logger.debug(
        "Generating upload info for %d files with prefix: %s", len(files), object_prefix
    )

    for bucket, files in distribute_objects(buckets, files).items():
        for filepath in files:
            relative_path = get_relative_path(filepath, local_parent_dir)
            upload_obj = UploadObject(
                filepath=str(filepath),
                bucket=bucket,
                object_key=gen_object_key(object_prefix, relative_path),
                relative_path=relative_path,
            )
            res.append(upload_obj)
            logger.debug(
                "Created upload object for %s in bucket %s", relative_path, bucket
            )

    logger.info("Generated upload info for %d objects", len(res))
    return res


def generate_index(model_name: str, upload_objects: list[UploadObject]):
    logger.info("Generating index for model: %s", model_name)

    file_list = []
    for item in upload_objects:
        obj_index = RemoteObjectIndex(
            filename=item.relative_path,
            bucket_index=ModelBucket(item.bucket).index,
            object_key=item.object_key,
        )

        file_list.append(obj_index)
        logger.debug("Added file to index: %s", item.relative_path)

    model_index = ModelIndex(model_name=model_name, file_list=file_list)

    logger.info("Generated index with %d files", len(file_list))
    return model_index


class DistributeCosHandler(COSHandler):

    def prepare_buckets(self, buckets: list[str], replication_regions: list[str]):
        model_buckets = self.create_model_buckets(
            buckets, public_read=True, multi_versioning=True
        )

        bucket_names = [bucket.bucket_name for bucket in model_buckets]

        # 设置跨区域复制
        for region in replication_regions:
            self.set_replication(bucket_names, region)

        return model_buckets

    def set_replication(self, source_buckets: list[str], target_region: str, overwrite: bool = False):
        source_bucket_list = [
            ModelBucket(bucket, self.uin, self.minio_client)
            for bucket in source_buckets
        ]

        for source_bucket in source_bucket_list:
            target_bucket = source_bucket.get_bucket_for_region(target_region)
            target_bucket.create(public_read=True, multi_versioning=True)
            source_bucket.add_replication(target_bucket, overwrite)

    