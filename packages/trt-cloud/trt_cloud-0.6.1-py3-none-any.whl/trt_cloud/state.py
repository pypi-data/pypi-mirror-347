# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""
Manage state for the TRT Cloud CLI which is preserved between uses.

Currently this includes a config file with login credentials and a NGC Private Registry cache.
"""

import configparser
import dataclasses
import datetime
import hashlib
import io
import json
import logging
import os
import platform
import shutil
from typing import Any, Dict, List, Optional, Tuple
import uuid
import enum

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from trt_cloud import constants

# Directory where TRT Cloud stores persistent state.
TRT_CLOUD_DIR = {
    "Linux": os.path.join(os.path.expanduser("~"), ".trt-cloud"),
    "Darwin": os.path.join(os.path.expanduser("~"), ".trt-cloud"),
    "Windows": os.path.join(os.path.expandvars("%appdata%"), "NVIDIA", "TRT Cloud"),
}[platform.system()]

DEFAULT_CONFIG_FILE = os.path.join(TRT_CLOUD_DIR, "config")
DEFAULT_REGISTRY_CACHE_FILE = os.path.join(TRT_CLOUD_DIR, "ngc_private_registry_cache.json")
CONFIG_FILE_BACKUP_SUFFIX = ".backup"

_NO_DEFAULT = object()


class CredentialError(ValueError):
    pass


def _create_trt_cloud_dir():
    """Create a directory for storing TRT Cloud state."""
    os.makedirs(TRT_CLOUD_DIR, exist_ok=True)


class ConfigKey(enum.Enum):
    """
    Enum for config keys.

    The enum value is a tuple of (section, option).
    The option is None for dynamic option values (like licenses, which have a dynamic version string).
    """

    NVAPI_KEY = ("login", "nvapi_key")
    NGC_ORG = ("ngc", "ngc_org_id")
    NGC_TEAM = ("ngc", "ngc_team_id")

    LICENSE = ("license", None)
    PREBUILT_LICENSE = ("prebuilt_license", None)

    @property
    def section(self) -> str:
        return self.value[0]

    @property
    def option(self) -> Optional[str]:
        # Returns None for keys where the option is dynamic (like licenses)
        return self.value[1]


class TRTCloudConfig:
    """
    Class for managing persistent user config for TRT Cloud.

    Abstracts the config file format and provides a few convenience methods.
    """

    _config: configparser.ConfigParser
    _file_path: str

    def __init__(self, file_path: str | None = None):
        """
        Initialize the config object.

        If the config file does not exist, it will be created, including the parent directories.

        Args:
            file_path: The path to the config file. If not provided, no config file will be created.
        """
        self._file_path = file_path

        try:
            if self._file_path:
                self._create_file_if_not_exists(self._file_path)
            else:
                logging.debug("No config file path provided. Using in-memory config.")

            # Initializes the configparser object with the contents of the config file
            self._load()
        except Exception as e:
            logging.debug("Failed to read config file: %s", e, exc_info=True)
            raise RuntimeError(f"Failed to read config file: {e}") from e

    def _create_file_if_not_exists(self, file_path: str):
        """Create the config file if it doesn't already exist."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "x"):
                pass

    def _set(self, key: ConfigKey, value: str | int | float | bool | None, option_override: str | None = None):
        """
        Set an option in the config file using a ConfigKey.

        If option_override is provided, it's used instead of key.option.
        The change is not saved to disk until _save() is called.
        """
        section = key.section
        option = option_override if option_override is not None else key.option
        if option is None:
            raise ValueError(f"Option must be specified either in ConfigKey {key.name} or via option_override")

        if section not in self._config:
            self._config[section] = {}
        self._config[section][option] = str(value) if value is not None else ""

    def _get(
        self,
        key: ConfigKey,
        default: Any = _NO_DEFAULT,
        raise_if_missing: type[Exception] | None = None,
        option_override: str | None = None,
    ) -> str:
        """
        Get an option from the config file using a ConfigKey.

        If option_override is provided, it's used instead of key.option.
        If the option is not found and the default value is provided, it will be returned.
        Otherwise or if the section is not found, and if raise_if_missing is provided, that exception will be raised;
        if not, the original configparser exception is raised.
        """
        section = key.section
        option = option_override if option_override is not None else key.option
        if option is None:
            logging.debug("Option must be specified either in ConfigKey %s or via option_override", key.name)
            raise ValueError(f"Unknown config key: {key.name}")

        try:
            return self._config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as exc:
            logging.debug("Config key %s (section=%s, option=%s) not found: %s", key.name, section, option, exc)

            # Use `object()` to distinguish between a missing default and `None`
            if default is not _NO_DEFAULT:
                return default

            if raise_if_missing is not None:
                raise raise_if_missing(
                    f"The credential: {section}.{option} is not found. Please use trt-cloud login to add it."
                ) from exc

            raise exc

    def __str__(self):
        """Return the config file representation as a string."""
        string_io = io.StringIO()
        self._config.write(string_io)
        return string_io.getvalue()

    def _load(self):
        """Load the config file from disk, replacing the existing in-memory config."""
        if self._file_path:
            self._config = configparser.ConfigParser()
            self._config.read(self._file_path)
        # For in-memory config, create the configparser object just the first time
        elif not getattr(self, "_config", None):
            self._config = configparser.ConfigParser()

    def _save(self):
        """Save the config file to disk."""
        if not self._file_path:
            return

        with open(self._file_path, "w") as f:
            self._config.write(f)

    # Public properties

    @property
    def file_path(self) -> str | None:
        """
        Get the path to the config file.
        """
        return self._file_path

    @property
    def nvapi_key(self) -> str:
        """
        Read the NVAPI key from the config file.
        """
        return self._get(ConfigKey.NVAPI_KEY, raise_if_missing=CredentialError)

    @nvapi_key.setter
    def nvapi_key(self, value: str):
        """
        Set the NVAPI key in the config file.

        NOTE: credentials are stored in plaintext.
        """
        self._set(key=ConfigKey.NVAPI_KEY, value=value)
        self._save()

    @property
    def ngc_org(self) -> str:
        """
        Read the NGC org ID from the config file.
        """
        return self._get(ConfigKey.NGC_ORG, raise_if_missing=CredentialError)

    @ngc_org.setter
    def ngc_org(self, value: str):
        """Set the NGC org ID in the config file."""
        self._set(key=ConfigKey.NGC_ORG, value=value)
        self._save()

    @property
    def ngc_team(self) -> str:
        """
        Read the NGC team ID from the config file.
        """
        return self._get(ConfigKey.NGC_TEAM, raise_if_missing=CredentialError)

    @ngc_team.setter
    def ngc_team(self, value: str | None):
        """
        Set the NGC team ID in the config file.

        None and `no-team` are both treated as an empty string.
        """
        value = "" if not value or value == "no-team" else value
        self._set(key=ConfigKey.NGC_TEAM, value=value)
        self._save()

    @property
    def ngc_org_and_team(self) -> Tuple[str, str]:
        """
        Read the NGC org ID and team ID from the config file.
        """
        return self.ngc_org, self.ngc_team

    def update_credentials(self, nvapi_key: str | None = None, ngc_org: str | None = None, ngc_team: str | None = None):
        """
        Update the credentials in the config file.

        Only parameters that are not None will be updated; existing values will be left unchanged.
        This method performs only one file save operation at the end, even if multiple credentials are updated.
        """
        updated = False
        if nvapi_key is not None:
            self._set(key=ConfigKey.NVAPI_KEY, value=nvapi_key)
            updated = True
        if ngc_org is not None:
            self._set(key=ConfigKey.NGC_ORG, value=ngc_org)
            updated = True
        if ngc_team is not None:
            self._set(key=ConfigKey.NGC_TEAM, value=ngc_team)
            updated = True

        # Save only once at the end if any updates were made
        if updated:
            self._save()

    def clear(self):
        """
        Clear the config file.
        """
        self._config = configparser.ConfigParser()
        self._save()

    # License methods

    def agreed_to_license(self, version: str) -> bool:
        """Return whether the user has agreed to the TRT Cloud license."""
        # Option is the dynamic version string here
        return bool(self._get(ConfigKey.LICENSE, default=False, option_override=version))

    def save_agreed_to_license(self, version: str):
        """Agree to the TRT Cloud license."""
        # Option is the dynamic version string here
        self._set(key=ConfigKey.LICENSE, value="True", option_override=version)
        self._save()

    def agreed_to_engine_license(self, version: str) -> bool:
        """Return whether the user has agreed to the TRT Cloud Prebuilt Engine license."""
        # Option is the dynamic version string here
        return bool(self._get(ConfigKey.PREBUILT_LICENSE, default=False, option_override=version))

    def save_agreed_to_engine_license(self, version: str):
        """Agree to the TRT Cloud Prebuilt Engine license."""
        # Option is the dynamic version string here
        self._set(key=ConfigKey.PREBUILT_LICENSE, value="True", option_override=version)
        self._save()


@dataclasses.dataclass
class NGCModel:
    org: str
    team: str
    model_name: str
    version: str

    @property
    def _team_str(self) -> str:
        # Even though most NGC print-outs show "no-team" when selecting the default team, most
        # assets, including NGC private registry models, actually skip the team name when that is
        # the case.
        if self.team == constants.NGC_NO_TEAM:
            return ""
        if self.team:
            return f"{self.team}/"
        return ""

    @property
    def target(self) -> str:
        return f"{self.org}/{self._team_str}{self.model_name}:{self.version}"

    @property
    def target_without_version(self) -> str:
        return f"{self.org}/{self._team_str}{self.model_name}"


class NGCRegistryCache:
    """
    Class for reading and writing to the NGC private registry cache.
    The cache is helpful to prevent uploading the same input file or directory multiple times.

    The cache file has the following JSON format:

    {
        "<file_or_dir_hash>": {
            "org": <str>,
            "team": <str>,
            "model_name": <str>,
            "version": <str>,
        },
        ...
    },
    """

    _file_path: str

    def __init__(self, file_path: str):
        if not file_path:
            raise ValueError("NGC registry cache file path must be provided")

        self._file_path = file_path
        _create_trt_cloud_dir()

        # Create cache file if it doesn't already exist.
        if not os.path.exists(self._file_path):
            self.clear()

    def file_hash(self, filepath: str) -> str:
        """
        Compute the SHA256 hash of a file.
        """
        block_size = 64 * 1024
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            blob = f.read(block_size)
            while blob:
                sha.update(blob)
                blob = f.read(block_size)
        return sha.hexdigest()

    def path_hash(self, path: str) -> str:
        """
        Compute the SHA256 hash of a file or directory.

        Adapted from https://stackoverflow.com/a/49701019.
        """
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Input path {abs_path} does not exist.")

        if os.path.isfile(abs_path):
            return self.file_hash(abs_path)

        digest = hashlib.sha256()
        for root, _, files in sorted(os.walk(path)):
            for file in files:
                file_path = os.path.join(root, file)

                # Hash the relative path and add to the digest to account for empty files
                relative_path = os.path.relpath(file_path, path)
                digest.update(hashlib.sha256(relative_path.encode()).digest())

                if os.path.isfile(file_path):
                    file_hash = self.file_hash(file_path)
                    digest.update(file_hash.encode())

        return digest.hexdigest()

    def read(self) -> Dict[str, NGCModel]:
        with open(self._file_path, "r") as f:
            cache_json = json.load(f)
        cache = {
            file_hash: NGCModel(
                org=entry["org"], team=entry["team"], model_name=entry["model_name"], version=entry["version"]
            )
            for file_hash, entry in cache_json.items()
        }
        return cache

    def write(self, cache: Dict[str, NGCModel]):
        cache_json = {
            file_hash: dataclasses.asdict(entry)
            for file_hash, entry in cache.items()  # noqa
        }
        with open(self._file_path, "w") as f:
            json.dump(cache_json, f, indent=4)

    def clear(self):
        self.write({})

    def upload_path(self, filepath_to_upload: str) -> str:
        """
        Uploads a local file or directory to NGC and returns the NGC model target.

        If the file or directory was already uploaded, the existing NGC model target is returned.
        """
        import ngcsdk
        from ngcbase.errors import ResourceAlreadyExistsException

        logging.info("Local model was provided. Checking NGC upload cache for existing model...")
        ngc_client = ngcsdk.Client()
        config = State.get().config
        org, team = config.ngc_org_and_team
        nvapi_key = config.nvapi_key

        team_display = "None (default)" if team == "" else team
        logging.info(f"Configuring NGC client with org: {org}, team: {team_display}")
        # NGC SDK does not understand that `team_name=""` or `team_name=None` should correspond to
        # "no-team".
        team_name = team if team else "no-team"
        ngc_client.configure(org_name=org, team_name=team_name, api_key=nvapi_key)
        logging.info("NGC client configured successfully.")

        logging.info(f"Computing hash of local path '{filepath_to_upload}' for cache lookup...")
        hash = self.path_hash(filepath_to_upload)
        cache = self.read()

        # The file or directory was already uploaded.
        if hash in cache:
            ngc_model = cache[hash]
            # Double-check that the NGC model still exists.
            try:
                ngc_client.registry.model.get_version(
                    org_name=ngc_model.org,
                    team_name=ngc_model.team,
                    model_name=ngc_model.model_name,
                    version=ngc_model.version,
                )

                logging.info(f"Reusing uploaded NGC model with target '{ngc_model.target}'")
                return ngc_model.target
            except Exception:
                logging.info(f"NGC model with target '{ngc_model.target}' does not exist. Uploading new model.")
                del cache[hash]
                self.write(cache)

        created_model = False
        while not created_model:
            # There is a very small chance of short UUID collision, hence the while loop.
            short_uuid = str(uuid.uuid4())[:8]
            model_name = f"local-model-{short_uuid}"
            ngc_model = NGCModel(org=org, team=team, model_name=model_name, version="1.0")

            logging.info(f"Creating NGC Model '{model_name}' in Private Registry")
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                ngc_client.registry.model.create(
                    target=ngc_model.target_without_version,
                    application="CONTENT_GENERATION",
                    framework="unknown_framework",
                    model_format="unknown_format",
                    precision="ALL",
                    short_description=f"This model was uploaded from a local file using TensorRT Cloud at {now}",
                )
                created_model = True
            except ResourceAlreadyExistsException:
                logging.warning(f"NGC Model '{model_name}' already exists. Creating a new model.")

        logging.info(f"Uploading local path '{filepath_to_upload}' to NGC Model '{model_name}'")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Upload progress:")

            def progress_callback_func(
                completed_bytes,
                failed_bytes,
                total_bytes,
                completed_count,
                failed_count,
                total_count,
            ):
                progress.update(task, completed=completed_bytes, total=total_bytes)

            upload_result = ngc_client.registry.model.upload_version(
                target=ngc_model.target,
                source=filepath_to_upload,
                progress_callback_func=progress_callback_func,
            )
            upload_status = upload_result[1]

        if upload_status == "Completed":
            logging.info(f"Successfully uploaded NGC Model '{model_name}'")
        else:
            # Clean up if the upload failed.
            try:
                logging.info(f"Attempting to remove NGC Model '{model_name}'")
                ngc_client.registry.model.remove(ngc_model.target_without_version)
                logging.info(f"Successfully removed NGC Model '{model_name}'")
            except Exception as exc:
                logging.error(f"Failed to remove NGC Model '{model_name}': {exc}")

            raise RuntimeError(
                f"Failed to upload NGC Model '{model_name}' because upload status is {upload_status}."
            ) from exc

        # Save model to cache.
        cache[hash] = ngc_model
        self.write(cache)
        return ngc_model.target


class State:
    """
    Singleton class for managing state for the TRT Cloud CLI.

    Responsible for managing the state of the CLI, including:
    - Configuration
    - NGC registry cache

    This class is a singleton and its instance can be accessed either via the `state` module variable declared at the
    bottom of this file (recommended) or by calling `State.get()`.

    Most state properties are only available after `State.initialize()` is called with the proper config and registry
    cache file paths. However the instance will not change, so it's safe to call `State.get()` before initialization.
    """

    _initialized: bool = False
    _instance: Optional["State"] = None
    _config: TRTCloudConfig
    _registry_cache: NGCRegistryCache

    def __init__(self):
        """
        Create a new State instance.

        Should only be called by `State.get()`.
        """
        # Ensure the singleton is instantiated only once
        if State._instance is not None:
            raise RuntimeError("Use State.get() instead")

        self._initialized = False

    # Class methods to manage the Singleton instance.
    # - get: Get the Singleton instance.
    # - initialize: Initialize the Singleton instance with the provided config and registry cache files.
    # - reset: Reset the Singleton instance to allow reinitialization with different files.

    @classmethod
    def initialize(cls, config_file_path: str | None = None, registry_cache_file_path: str | None = None) -> "State":
        """
        Initialize the State class.

        This method must be called before accessing any properties.

        It can only be called once; subsequent calls will be ignored. This is useful for testing, where we want to
        initialize the state with a temporary config file before the main CLI initializes it with the default config
        file.

        To initialize after the first initialization, call `reset()` before calling `initialize()` again.
        """
        instance = cls.get()

        # Already initialized
        if instance._initialized:
            return instance

        # Ensure that the default config file is not used when running tests.
        if (
            config_file_path == DEFAULT_CONFIG_FILE or registry_cache_file_path == DEFAULT_REGISTRY_CACHE_FILE
        ) and os.environ.get("PYTEST_CURRENT_TEST"):
            raise RuntimeError("Must use temporary files when running tests")

        instance._config = TRTCloudConfig(file_path=config_file_path)
        instance._registry_cache = NGCRegistryCache(file_path=registry_cache_file_path)
        instance._initialized = True
        return instance

    @classmethod
    def reset(cls):
        """
        Reset the initialized state.

        Allows reinitialization with different config and registry cache files.
        """
        instance = cls.get()
        instance._config = None
        instance._registry_cache = None
        instance._initialized = False

    @classmethod
    def get(cls):
        """
        Get the singleton instance of the State class.

        This method can be called before initialization, but not all properties are available until initialization is
        complete.

        The instance shouldn't ever change, even after reset and reinitialization.
        """
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    # Properties to access the state.

    @property
    def is_initialized(self) -> bool:
        """
        Check if the state has been initialized.
        """
        return self._initialized

    @property
    def config(self) -> TRTCloudConfig:
        """
        Get the TRT Cloud config.
        """
        if not self._initialized:
            raise RuntimeError("Configuration not initialized.")

        return self._config

    @property
    def registry_cache(self) -> NGCRegistryCache:
        """
        Get the NGC registry cache.
        """
        return self.get()._registry_cache


# Singleton instance that other modules can use to access the state.
state = State().get()
