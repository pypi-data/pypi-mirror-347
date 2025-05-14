import logging
import logging.config
import os
import time
import traceback
from datetime import UTC, datetime
from typing import Optional

import typer
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContentSettings
from pydantic import Field

from inspari.config import load_dotenv
from inspari.logging.utils import (
    _logging_extras,
    _logging_prefix,
    _logging_suffix,
    _resolve_environment,
)

"""
The steaming logs module is used to stream logs from an Azure Blob Storage container to the terminal.
Compared to standard Azure tooling, it provides a (much) lower latency.
"""


logger = logging.getLogger(__name__)


_default_conn_str_keys = [
    "AZURE_STORAGE_BLOB_URL",  # default Azure
    "ABS_CONNECTION_STRING",  # default Inspari
    "APP_ABS_CONNECTION_STRING",  # default Inspari App
    "API_ABS_CONNECTION_STRING",  # default Inspari Api
    "RAG_ABS_CONNECTION_STRING",  # default Inspari RAG
]


def _resolve_conn_str(
    conn_str: str | None, env_key: Optional[str] = None
) -> str | None:
    if conn_str is not None:
        return conn_str
    # If key is provided, use it.
    if env_key is not None:
        conn_str = os.getenv(env_key, None)
        if conn_str is None:
            logger.error(
                f"Failed to load connection string from (provided) environment variable {env_key}."
            )
            return None
    # Otherwise, try the default is priority order.
    for key in _default_conn_str_keys:
        conn_str = os.getenv(key, None)
        if conn_str is not None:
            return conn_str
    return None


def _get_blob_client(
    credential: DefaultAzureCredential,
    conn_str: Optional[str] = None,
    container: Optional[str] = None,
    blob_name: Optional[str] = None,
    env_key: Optional[str] = None,
    account_name: Optional[str] = None,
) -> BlobClient:
    # If container is not set, default to "logs" container.
    container = container if container is not None else "logs"

    # If blob is not set, use the default name.
    if blob_name is None:
        now = datetime.now(UTC)
        blob_name = now.strftime("%Y-%m-%d.txt")

    if account_name is not None:
        account_url = f"https://{account_name}.blob.core.windows.net"

        blob_client = BlobClient(
            account_url=account_url,
            container_name=container,
            blob_name=blob_name,
            credential=credential,
        )
        return blob_client

    # Get the connection string from the environment.
    conn_str = _resolve_conn_str(conn_str, env_key)
    if conn_str is None:
        raise ValueError("Failed to resolve connection string or account name.")
    return BlobClient.from_connection_string(conn_str, container, blob_name)


def _parse_bool(value: str | bool) -> bool:
    return value if isinstance(value, bool) else value.lower() == "true"


def _resolve_parameter(param: str | None, env_key: Optional[str] = None) -> str | None:
    if param is not None:
        return param
    if env_key is not None:
        for sub_key in env_key.split(","):
            value = os.getenv(sub_key, None)
            if value is not None:
                return value
    return None


class AzureBlobStorageHandler(logging.Handler):
    """
    Logging handler that streams logs to an Azure blob storage container.
    """

    def __init__(
        self,
        conn_str: Optional[str] = None,
        container: Optional[str] = None,
        blob: Optional[str] = None,
        env_key: Optional[str] = None,
        account_name_env_key: Optional[str] = None,
        account_name: Optional[str] = None,
        client_id: Optional[str] = None,
        client_id_env_key: Optional[str] = None,
        load_dot_env: bool | str = False,
        log_local: bool | str = False,
        exclude_environment_credentials: bool = False,
    ):
        self.client = None
        try:
            self.client = self._setup_client(
                conn_str,
                container,
                blob,
                env_key,
                account_name_env_key,
                account_name,
                client_id,
                client_id_env_key,
                load_dot_env,
                log_local,
                exclude_environment_credentials,
            )
        except Exception:
            logger.error("Failed to setup AzureBlobStorageHandler.")
            logger.error(traceback.format_exc())

    def _setup_client(
        self,
        conn_str: Optional[str] = None,
        container: Optional[str] = None,
        blob: Optional[str] = None,
        env_key: Optional[str] = None,
        account_name_env_key: Optional[str] = None,
        account_name: Optional[str] = None,
        client_id: Optional[str] = None,
        client_id_env_key: Optional[str] = None,
        load_dot_env: bool | str = False,
        log_local: bool | str = False,
        exclude_environment_credentials: bool = False,
    ) -> None | BlobClient:
        logging.Handler.__init__(self=self)
        # Check if running locally.
        local = _resolve_environment() == "local"
        if local and not _parse_bool(log_local):
            logger.debug("Not logging to Azure Blob Storage as environment is local.")
            return None
        # If we are local, we do NOT want to authenticate with a managed identity, so we skip the client_id.
        client_id = None if local else _resolve_parameter(client_id, client_id_env_key)
        # Setup credential.
        credential = DefaultAzureCredential(
            managed_identity_client_id=client_id,
            exclude_environment_credential=_parse_bool(exclude_environment_credentials),
        )
        # Optionally, load from .env file.
        if _parse_bool(load_dot_env):
            load_dotenv(credential=credential)
        # Resolve parameters.
        account_name = _resolve_parameter(account_name, account_name_env_key)
        # Setup client.
        client = _get_blob_client(
            credential, conn_str, container, blob, env_key, account_name
        )
        # Create blob if not exists.
        logger.info(f"Logging to storage account {client.account_name}.")
        if not client.exists():
            content_settings = ContentSettings(
                content_type="text/plain",
            )
            try:
                client.create_append_blob(content_settings=content_settings)
            except ResourceNotFoundError as e:
                logger.error(
                    f"Error creating blob: {e} {client.blob_name} in container {client.container_name} in {client.account_name}."
                )
                return
        logger.info(
            f"Logging to blob {client.blob_name} in container {client.container_name}."
        )
        return client

    def _prefix(self):
        pass

    def emit(self, record) -> None:
        if self.client is None:
            return
        msg = self.format(record)
        msg_with_extras = (
            f"{_logging_extras[_logging_prefix]}{msg}{_logging_extras[_logging_suffix]}"
        )
        self.client.append_block(f"{msg_with_extras}\n".encode("utf-8"))


def stream_logs(
    conn_str: Optional[str] = None,
    container: Optional[str] = None,
    blob: Optional[str] = None,
    env_key: Optional[str] = None,
    account_name: Optional[str] = None,
    account_name_env_key: Optional[str] = "APP_ABS_ACCOUNT_NAME",
    client_id_env_key: Optional[str] = None,
    client_id: Optional[str] = Field(
        None,
        description="The client ID for the managed identity. Not needed if using regular az cli login.",
    ),
    delay: int = 1,
    exclude_environment_credentials: bool = False,
):
    """
    Stream logs to terminal from the specified blob.
    """
    account_name = _resolve_parameter(account_name, account_name_env_key)
    client_id = _resolve_parameter(client_id, client_id_env_key)
    credential = DefaultAzureCredential(
        managed_identity_client_id=client_id,
        exclude_environment_credential=_parse_bool(exclude_environment_credentials),
    )
    client = _get_blob_client(
        credential, conn_str, container, blob, env_key, account_name
    )
    assert client is not None
    offset = 0
    first = True
    last_modified = None
    logging.info(
        f"Streaming logs from {client.blob_name} in container {client.container_name} in {client.account_name}."
    )
    while True:
        try:
            props = client.get_blob_properties()
            if last_modified is None or last_modified < props["last_modified"]:
                last_modified = props["last_modified"]
                bts = client.download_blob(offset=0).readall()
                offset += len(bts)
                print(bts.decode("utf-8"))
        except ResourceNotFoundError:
            if first:
                print("Blob not found.", end="")
            print(".", end="", flush=True)
        except HttpResponseError as e:
            print(f"Error: {e}")
        first = False
        time.sleep(delay)


def stream_logs_entrypoint():
    """
    Stream logs to terminal from the specified blob.
    """
    load_dotenv(dotenv_path=".env")
    # Set loglevel to info
    logging.basicConfig(level=logging.INFO)
    # Silence the azure logger
    logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
    typer.run(stream_logs)


if __name__ == "__main__":
    stream_logs_entrypoint()
