import logging
from pathlib import Path
from typing import Annotated, Optional
import typer
from typer import Option, Argument

from cloud_aitools.model import defaults
from .models import Index

from ..handler.cos_handler import COSHandler
from .distribute import DistributeCosHandler, generate_bucket_name, generate_buckets, generate_index, generate_upload_info
from ..utils.dns import detect_region
from ..utils.utils import get_files_in_directory

logger = logging.getLogger(__name__)

app = typer.Typer()

@app.command(name="upload", help="Upload new model to cos.")
def upload(
            secret_id: Annotated[str, Option(help="The secret id of cos used for upload object.")],
            secret_key: Annotated[str, Option(help="The secret key of cos used for upload object.")],
            local_path: Annotated[str, Option(help="The local path of the model to upload.")],
            model_name: Annotated[str, Option(help="The name for the uploaded model.")],
            bucket_prefix: Annotated[str, Option(help="The prefix of the bucket name.")],
            appid: Annotated[str, Option(help="The appid of the cos bucket.")],
            region: Annotated[str, Option(help="The region of the cos bucket.")],
            replication_regions: Annotated[Optional[str], Option(help="The regions splitted by comma for bucket replication. eg. ap-beijing,ap-chengdu")] = None,
            bucket_num: Annotated[int, Option(help="The number of buckets to create.")] = defaults.BUCKET_NUM,
            excludes: Annotated[list[str], Option("--exclude", "-e", help="The file patterns to exclude from the upload.")] = []
        ):
    
    
    handler = DistributeCosHandler(region, secret_id, secret_key)
    
    model_path = Path(local_path)
    file_list = get_files_in_directory(local_path, excludes)
    
    buckets = generate_buckets(f"{bucket_prefix}-{region}-{appid}", bucket_num)
    handler.prepare_buckets(buckets, replication_regions=replication_regions.split(",") if replication_regions else [])
    
    upload_objects = generate_upload_info(buckets, file_list, model_name, model_path)
    first_bucket = next(iter(buckets))
    index = handler.load_index_config(first_bucket)
    model_index = generate_index(model_name, upload_objects=upload_objects)
    index.update(model_index)
    
    handler.upload_object_to_buckets(buckets, "index.json", index.dump().encode("utf-8"))
    
    logger.info("start to upload model to buckets: %s", buckets)
    handler.upload_objects(upload_objects)
    logger.info("upload model finished.")


@app.command(name="download", help="Download model from cos.")
def download_model(model_name: Annotated[str, Argument(help="The model name to download.")],
                   output_dir: Annotated[str, Option("--output", "-o", help="The output directory to save the downloaded model.")],
                   region: Annotated[Optional[str], Argument(help="The region of the cos bucket.")]="",
                   bucket_prefix: Annotated[str, Option(help="The prefix of the bucket name.")]=defaults.BUCKET_PREFIX,
                   appid: Annotated[str, Option(help="The appid of the cos bucket.")]=defaults.PUBLIC_APPID,
                   process_num: Annotated[int, Option("--process-num", "-p", help="The number of processes to use for downloading.")] = defaults.PROC_NUM):

    if not region:
        logger.info("input region is empty, try to detect region automatically")
        detected_region = detect_region()
        
        if not detected_region:
            raise typer.BadParameter("region is not specified and cannot be detected automatically.")
        else:
            region = detected_region
            logger.info("detect region successfully, region is: %s", region)

    bucket_template = f"{bucket_prefix}-{appid}"
    first_bucket = generate_bucket_name(bucket_template, region, 0)
    
    handler = COSHandler(region, "", "")
    index = handler.load_index_config(first_bucket)
    
    model_index = Index.gen_local_index(bucket_prefix, region, appid, index.get_model_objects_index(model_name))
    
    if not model_index:
        raise typer.BadParameter(f"model {model_name} not found.")
    
    handler.download_objects_from_index(model_index, output_dir, process_num=process_num, progress_title=f"Downloading {model_name}...")
    
    
    typer.echo(f"Model {model_name} downloaded successfully to {output_dir}. enjoy ;)")
    

@app.command(name="list", help="List the available models in cos.")
def list_model(
                region: Annotated[Optional[str], Option(help="The region of the cos bucket.")]="",
                bucket_prefix: Annotated[Optional[str], Option(help="The prefix of the bucket name.")]=defaults.BUCKET_PREFIX,
                appid: Annotated[Optional[str], Option(help="The appid of the cos bucket.")]=defaults.PUBLIC_APPID):
    
    
    if not region:
        logger.info("input region is empty, try to detect region automatically")
        detected_region = detect_region()
        if not detected_region:
            raise typer.BadParameter("region is not specified and cannot be detected automatically.")
        else:
            region = detected_region
            logger.info("detect region successfully, region is: %s", region)
            
    bucket_template = f"{bucket_prefix}-{appid}"
    first_bucket = generate_bucket_name(bucket_template, region, 0)
    
    handler = COSHandler(region, "", "")
    index = handler.load_index_config(first_bucket)
    
    typer.echo("Model")
    for model_index in index.get_all_model_index():
        typer.echo(model_index.model_name)

@app.command(help="Add replication from source region to target regions.")
def create_replication(
            secret_id: Annotated[str, Option(help="The secret id of cos used for upload object.")],
            secret_key: Annotated[str, Option(help="The secret key of cos used for upload object.")],
            bucket_prefix: Annotated[str, Option(help="The prefix of the bucket name.")],
            appid: Annotated[str, Option(help="The appid of the cos bucket.")],
            source_region: Annotated[str, Option(help="The source region of the cos bucket to be replicated.")],
            replication_regions: Annotated[str, Option(help="The target regions splitted by comma for bucket replication. eg. ap-beijing,ap-chengdu")],
            overwrite: Annotated[bool, Option(help="Whether to overwrite the existing replication rule.")] = False,
            bucket_num: Annotated[int, Option(help="The number of buckets for replication.")] = defaults.BUCKET_NUM):
    
    handler = DistributeCosHandler(source_region, secret_id, secret_key)
    buckets = generate_buckets(f"{bucket_prefix}-{source_region}-{appid}", bucket_num=bucket_num)
    
    for region in replication_regions.split(","):
        handler.set_replication(buckets, region, overwrite)
    

if __name__ == "__main__":
    app()
    