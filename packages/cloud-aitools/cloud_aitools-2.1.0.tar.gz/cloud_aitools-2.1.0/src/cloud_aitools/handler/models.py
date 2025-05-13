import datetime
import json
import logging
from typing import List, Optional, Self, Sequence, cast
import xml.etree.ElementTree as ET

from minio import Minio, S3Error
import minio
from minio.xml import unmarshal, marshal
from minio import commonconfig
import minio.versioningconfig
from minio.replicationconfig import (
    ReplicationConfig,
    Rule,
    DeleteMarkerReplication,
    Destination,
    ExistingObjectReplication,
)
from minio import lifecycleconfig
from minio.commonconfig import BaseRule
from minio.helpers import md5sum_hash


class Bucket:
    def __init__(
        self,
        bucket_name: str,
        region: str,
        uin: str = "",
        minio_client: Optional[Minio] = None,
    ) -> None:
        self._minio_client = minio_client
        self.bucket_name = bucket_name
        self.region = region
        self.appid = self.get_appid_from_bucket(bucket_name)
        self.uin = uin

    @property
    def client(self):
        if not self._minio_client:
            raise Exception("Minio client not initialized")
        return self._minio_client

    @property
    def credential_provider(self):
        return self.client._provider

    def exists(self):
        return self.client.bucket_exists(self.bucket_name)

    def create(self, public_read: bool = False, multi_versioning: bool = False):
        if not self.exists():
            self.client.make_bucket(self.bucket_name, self.region)

        if public_read:
            self.make_public_read()

        if multi_versioning:
            self.enable_versioning()
            # 开启多版本后, 添加周期性回收历史版本对象的生命周期规则
            self.add_lifecycle(
                self.generate_regular_delete_noncurrent_version_lifycyle_rule()
            )

    def make_public_read(self):
        if not self.exists():
            raise Exception("Bucket does not exist")

        policy = self.generate_read_only_bucket_policy()
        self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))

    def generate_read_only_bucket_policy(self):
        policy = {
            "Statement": [
                {
                    "Action": ["name/cos:GetObject", "name/cos:HeadObject"],
                    "Effect": "Allow",
                    "Principal": {"qcs": ["qcs::cam::anyone:anyone"]},
                    "Resource": [
                        f"qcs::cos:{self.region}:uid/{self.appid}:{self.bucket_name}/*"
                    ],
                }
            ],
            "version": "2.0",
        }

        return policy

    @staticmethod
    def get_appid_from_bucket(bucket: str):
        *_, appid = bucket.split("-")
        return appid

    def get_versioning(self):
        return self.client.get_bucket_versioning(self.bucket_name)

    def is_versioning_enabled(self):
        return self.get_versioning().status == commonconfig.ENABLED

    def enable_versioning(self):
        if not self.exists():
            raise Exception("Bucket does not exist")

        if self.is_versioning_enabled():
            logging.info(f"Bucket {self.bucket_name} already has versioning enabled.")
            return

        self.client.set_bucket_versioning(
            self.bucket_name,
            minio.versioningconfig.VersioningConfig(status=commonconfig.ENABLED),
        )

    def generate_replication_config(self, target_bucket: Self):
        role_id = f"{self.bucket_name}_to_{target_bucket.bucket_name}"
        config = ReplicationConfig(
            f"qcs::cam::uin/{self.uin}:uin/{self.uin}",
            [
                Rule(
                    Destination(
                        f"qcs::cos:{target_bucket.region}::{target_bucket.bucket_name}",
                    ),
                    status=commonconfig.ENABLED,
                    # Note: 存量对象复制有一天的延迟生效时间
                    existing_object_replication=ExistingObjectReplication(
                        commonconfig.ENABLED
                    ),
                    delete_marker_replication=DeleteMarkerReplication(
                        commonconfig.DISABLED,
                    ),
                    rule_id=role_id,
                ),
            ],
        )
        return config

    def get_lifecycle(self):
        return self.client.get_bucket_lifecycle(self.bucket_name)

    def get_replication(self):

        def process_body(body: str):
            root = ET.fromstring(body)
            # 将ExistingObjectReplication中的text用Status标签包裹起来, 以兼容S3协议, 后续cos发版本会解决这个兼容问题
            for rule in root.findall("Rule"):
                existing_object_replication = rule.find("ExistingObjectReplication")
                if existing_object_replication is None:
                    continue

                # 存在status标签时不再做处理
                status = existing_object_replication.find("Status")
                if status:
                    continue

                text = existing_object_replication.text
                existing_object_replication.text = None
                status_element = ET.SubElement(existing_object_replication, "Status")
                status_element.text = text

            res = ET.tostring(root, encoding="unicode")
            return res

        # 这部分代码对minio的get_replication做了部分修改, 对cos返回的内容做了一些兼容性处理
        # 因为cos返回的内容中ExistingObjectReplication的格式不兼容S3, 导致minio的get_replication报错

        try:
            resp = self.client._execute(
                "GET", bucket_name=self.bucket_name, query_params={"replication": ""}
            )
            content = process_body(resp.data.decode())
            return unmarshal(ReplicationConfig, content)
        except S3Error as e:
            if e.code != "ReplicationConfigurationNotFoundError":
                raise
        return None

    @staticmethod
    def merge_rules[T: BaseRule](
        src_rules: list[T], target_rules: list[T], overwirte: bool = False
    ):
        src_rules_map = {rule.rule_id: rule for rule in src_rules}

        target_rules = target_rules.copy()

        for rule in target_rules.copy():
            if rule.rule_id in src_rules_map:
                if overwirte:
                    src_rules_map.pop(rule.rule_id)
                else:
                    target_rules.remove(rule)

        return list(src_rules_map.values()) + target_rules

    @staticmethod
    def merge_replication_rules(
        src: ReplicationConfig, target: ReplicationConfig, overwirte: bool = False
    ):

        if src.role != target.role:
            raise Exception(
                "Replication config cannot be merged if the roles are different."
            )

        rules = Bucket.merge_rules(src.rules, target.rules, overwirte)

        return ReplicationConfig(role=src.role, rules=rules)

    def set_replication(self, config: ReplicationConfig):

        def process_config(body: ReplicationConfig):
            # 将ExistingObjectReplication中的Status标签中的text提取出来, 放在ExistingObjectReplication中, 并将Status标签删除
            root = body.toxml(None)
            for rule in root.findall("Rule"):
                for node in rule.findall("ExistingObjectReplication"):
                    status = node.find("Status")
                    if status is None:
                        continue
                    node.remove(status)
                    node.text = status.text

            return ET.tostring(root, encoding="utf-8")

        body = process_config(config)

        # 该方法参考minio中的实现, 但是在之前预处理了config, 使其与cos api兼容
        self.client._execute(
            "PUT",
            self.bucket_name,
            body=body,
            headers={"Content-MD5": cast(str, md5sum_hash(body))},
            query_params={"replication": ""},
        )

    def add_replication(self, target_bucket: Self, overwrite: bool = False):

        if not (self.exists() and target_bucket.exists()):
            raise Exception("Bucket does not exist")

        if not self.uin:
            raise Exception("Uni must be set to enable replication.")

        config = self.generate_replication_config(target_bucket)

        if raw_replication := self.get_replication():
            if not overwrite and not self.subtract_rules(
                config.rules, raw_replication.rules
            ):
                logging.info("No new replication rules to add.")
                return

            config = self.merge_replication_rules(raw_replication, config, overwrite)

        self.set_replication(config)

    @staticmethod
    def subtract_rules[T: BaseRule](a: list[T], b: list[T]):
        # a - b
        b_map = {rule.rule_id: rule for rule in b}

        a = a.copy()
        for rule in a.copy():
            if rule.rule_id in b_map:
                a.remove(rule)

        return a

    def generate_regular_delete_noncurrent_version_lifycyle_rule(self, days: int = 15):
        return lifecycleconfig.LifecycleConfig(
            rules=[
                lifecycleconfig.Rule(
                    rule_id="regular_delete_non_current_version_object",
                    rule_filter=lifecycleconfig.Filter(prefix=""),
                    status=commonconfig.ENABLED,
                    noncurrent_version_expiration=lifecycleconfig.NoncurrentVersionExpiration(
                        noncurrent_days=days
                    ),
                    abort_incomplete_multipart_upload=lifecycleconfig.AbortIncompleteMultipartUpload(
                        days_after_initiation=days
                    ),
                )
            ]
        )

    def merge_lifecycle(
        self,
        src_config: lifecycleconfig.LifecycleConfig,
        target_config: lifecycleconfig.LifecycleConfig,
        overwrite: bool = False,
    ):
        return lifecycleconfig.LifecycleConfig(
            rules=Bucket.merge_rules(src_config.rules, target_config.rules, overwrite)
        )

    def add_lifecycle(
        self, config: lifecycleconfig.LifecycleConfig, overwrite: bool = False
    ):
        if not self.exists():
            raise Exception("Bucket does not exist")

        raw_lifycycle = self.get_lifecycle()

        if raw_lifycycle:
            if not overwrite and not self.subtract_rules(
                config.rules, raw_lifycycle.rules
            ):
                logging.info("No new lifecycle rules to add.")
                return

            config = self.merge_lifecycle(raw_lifycycle, config, overwrite)

        self.client.set_bucket_lifecycle(self.bucket_name, config)

    def remove(self):
        if not self.exists():
            raise Exception("Bucket does not exist")

        self.client.remove_bucket(self.bucket_name)
