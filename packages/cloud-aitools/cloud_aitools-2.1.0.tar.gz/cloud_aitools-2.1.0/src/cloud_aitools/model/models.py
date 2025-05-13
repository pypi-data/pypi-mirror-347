from copy import deepcopy
import logging
from dataclasses import dataclass
import json
import re
from typing import Any, Optional, Self

from minio import Minio

from minio.replicationconfig import ReplicationConfig, Rule, Destination, DeleteMarkerReplication
from minio import commonconfig
from pydantic import BaseModel
from ..handler.models import Bucket

logger = logging.getLogger(__name__)


@dataclass
class UploadObject:
    filepath: str
    bucket: str
    object_key: str
    relative_path: str


class RemoteObjectIndex(BaseModel):
    filename: str
    bucket_index: int
    object_key: str


class LocalObjectIndex:
    
    def __init__(self, bucket_prefix: str, region:str, appid: str, remote_index: RemoteObjectIndex) -> None:
        self.remote_index = remote_index
        self.region = region
        self.appid = appid
        self.bucket_name = ModelBucket.gen_bucket_name_from_part(bucket_prefix, region, appid, self.bucket_index)
        self.url = f"https://{self.bucket_name}.cos.{self.region}.myqcloud.com/{self.object_key}"
    
    @property    
    def object_key(self):
        return self.remote_index.object_key
    
    @property
    def filename(self):
        return self.remote_index.filename
    
    @property
    def bucket_index(self):
        return self.remote_index.bucket_index
    
    
class ModelIndex(BaseModel):
    model_name: str
    file_list: list[RemoteObjectIndex]


class Index:

    def __init__(self, index_config: list[dict[str, Any]]) -> None:
        self.index_config = index_config
        self.model_config: dict[str, ModelIndex] = self.load_config(
            self.index_config)

    def load_config(self, index_config: list[dict[str, Any]]):
        res = {}
        logger.debug("Loading index configuration with %d models",
                     len(index_config))
        
        for model_item in index_config:
            try:
                item = ModelIndex.model_validate(model_item)
                res[item.model_name] = item
                logger.debug("Loaded model: %s with %d files", item.model_name,
                             len(item.file_list))
            except Exception as e:
                logger.error("Failed to load model: %s", model_item)
                logger.error(e)

        logger.info("Loaded configuration for %d models", len(res))
        return res

    def update(self, model_index_config: ModelIndex):
        logger.info("Updating index for model: %s",
                    model_index_config.model_name)
        logger.debug("Model has %d files", len(model_index_config.file_list))
        self.model_config[model_index_config.model_name] = model_index_config

    def dump(self):
        logger.debug("Dumping index configuration")
        dumped = [model.model_dump() for model in self.model_config.values()]
        logger.info("Dumped configuration for %d models", len(dumped))
        return json.dumps(dumped)

    def get_model_objects_index(self, model_name: str):
        return self.model_config[model_name].file_list

    @staticmethod
    def gen_local_index(bucket_prefix:str, region: str, appid: str, remote_index_ls: list[RemoteObjectIndex]):
        return [LocalObjectIndex(bucket_prefix, region, appid, remote_index) for remote_index in remote_index_ls]
        
    def get_all_model_index(self):
        return self.model_config.values()



class ModelBucket(Bucket):
    # model bucket name should be in the format of <bucket-prefix>-<region>-<index>-<appid>
    
    def __init__(self, bucket_name: str, uin: str = "", minio_client: Optional[Minio] = None) -> None:
        bucket_prefix, region, index, _ = self.parse_bucket_info(bucket_name)
        super().__init__(bucket_name, region, uin, minio_client)
        self.index = index
        self.bucket_prefix = bucket_prefix

    @staticmethod
    def parse_bucket_info(bucket_name: str):
        region = ModelBucket.parse_region_from_bucket_name(bucket_name)
        *bucket_prefix, index, appid = bucket_name.replace(f"-{region}", "").split("-")
        return "-".join(bucket_prefix), region, int(index), appid

    @staticmethod
    def parse_region_from_bucket_name(bucket_name: str):
        *parts, _, _ = bucket_name.split("-")
        pattern = r'-(ap|na|sa|eu)-[a-z]{3,}(-([0-9]{1,3}|fsi))?$'
        match = re.search(pattern, "-".join(parts))
        if match:
            return match.group().strip('-')
        else:
            raise ValueError("region info not found from bucket name.")
    
    @staticmethod
    def gen_bucket_name_from_part(bucket_prefix: str, region: str, appid: str, index: int):
        return f"{bucket_prefix}-{region}-{index}-{appid}"
    
    
    def switch_bucket_name_for_region(self, region: str):
        return self.gen_bucket_name_from_part(
            self.bucket_prefix, region, self.appid, self.index)
    
    
    def get_bucket_for_region(self, region: str):
        client = Minio(
            endpoint=f"cos.{region}.myqcloud.com",
            region = region,
            credentials=deepcopy(self.client._provider)
        )
        
        client.enable_virtual_style_endpoint()
        
        bucket_name = self.switch_bucket_name_for_region(region)
        model_bucket = ModelBucket(bucket_name, self.uin, client)
        
        return model_bucket