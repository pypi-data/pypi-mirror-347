"""Hub module for hosting tools."""

import importlib
import json
import os
import time
from collections.abc import Callable
from types import ModuleType
from huggingface_hub import delete_file, hf_hub_download, snapshot_download, upload_file
from huggingface_hub.errors import LocalEntryNotFoundError
from pydantic import BaseModel


class AgentHub:
    """Hugging Face Repo class.

    This class provides an interface to interact with Hugging Face repositories.
    It allows loading files, configs, and tools from a specified repository,
    as well as handling local caching when possible.
    """

    tools_dir: str = "tools"
    agents_dir: str = "agents"
    result_types_dir: str = "result_types"
    repo_type: str = "space"
    update_interval: int = 600

    def __init__(self, repo_id: str) -> None:
        """Initialize the Hugging Face Hub."""
        self.repo_id = repo_id

    def _load_module(self, module_name: str, path: str) -> ModuleType:
        """Load a module from a path."""
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:  # pragma: no cover
            raise ImportError(f"Could not load spec for module {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _check_extension(self, filename: str, extension: str) -> str:
        """Check if the filename has the correct extension."""
        if not filename.endswith(extension):  # pragma: no cover
            filename = f"{filename}{extension}"
        return filename

    def _lazy_update(self) -> None:
        """Lazily update the local cache.

        Update the repo only when self.get_file_path is called, and when
        interval has passed.
        """
        cache_path = self.download_files(local_files_only=True)
        last_modified = os.path.getmtime(cache_path)
        if time.time() - last_modified > self.update_interval:
            self.download_files()
            os.utime(cache_path, None)

    def download_files(self, local_files_only: bool = False) -> str:
        """Download all files from the Hugging Face Hub.

        This should be called at the service start up, as well as when any
        changes are made to the repo.
        """
        return snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            local_files_only=local_files_only,
        )

    def get_file_path(self, filename: str, subdir: str) -> str:
        """Get the local path to a file in the repo."""
        self._lazy_update()
        match subdir:
            case self.tools_dir:
                extension = ".py"
                subfolder = self.tools_dir
            case self.result_types_dir:
                extension = ".py"
                subfolder = self.result_types_dir
            case self.agents_dir:
                extension = ".json"
                subfolder = self.agents_dir
            case _:  # pragma: no cover
                raise ValueError(f"Invalid subdir: {subdir}")

        filename = self._check_extension(filename, extension)
        try:
            file_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=filename,
                subfolder=subfolder,
                local_files_only=True,
                repo_type=self.repo_type,
            )
        except LocalEntryNotFoundError:
            file_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=filename,
                subfolder=subfolder,
                repo_type=self.repo_type,
            )
        return file_path

    def delete_file(self, filename: str, subdir: str) -> None:
        """Delete a file from the Hugging Face Hub."""
        delete_file(
            path_in_repo=f"{subdir}/{filename}",
            repo_id=self.repo_id,
            repo_type=self.repo_type,
        )

    def load_config(self, filename: str) -> dict:
        """Load a config from the Hugging Face Hub."""
        if not filename:  # pragma: no cover
            return {}
        file_path = self.get_file_path(filename, self.agents_dir)

        with open(file_path) as file:
            return json.load(file)

    def load_tool(self, filename: str) -> Callable | None:
        """Load a tool from the Hugging Face Hub."""
        if not filename:  # pragma: no cover
            return None
        name_without_extension = filename.split(".")[0]
        file_path = self.get_file_path(filename, self.tools_dir)
        module = self._load_module(name_without_extension, file_path)
        func = getattr(module, name_without_extension)
        assert callable(func)

        return func

    def load_result_type(self, filename: str) -> type[BaseModel] | None:
        """Load a result type from the Hugging Face Hub."""
        if not filename:  # pragma: no cover
            return None
        name_without_extension = filename.split(".")[0]
        file_path = self.get_file_path(filename, self.result_types_dir)
        module = self._load_module(name_without_extension, file_path)
        model = getattr(module, name_without_extension)
        assert isinstance(model, type) and issubclass(model, BaseModel)

        return model

    def upload_content(
        self,
        filename: str,
        content: str,
        subdir: str,
    ) -> None:
        """Upload a file to the Hugging Face Hub."""
        match subdir:
            case self.tools_dir:
                extension = ".py"
            case self.result_types_dir:
                extension = ".py"
            case self.agents_dir:
                extension = ".json"
            case _:
                raise ValueError(f"Invalid type: {subdir}")

        filename = self._check_extension(filename, extension)

        upload_file(
            path_or_fileobj=content.encode("utf-8"),
            path_in_repo=f"{subdir}/{filename}",
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            commit_message=f"Update {filename}",
        )

    def list_files(self, subdir: str) -> list[str]:
        """List all files in the Hugging Face Hub."""
        repo_dir = snapshot_download(
            repo_id=self.repo_id, repo_type=self.repo_type, local_files_only=True
        )
        subdir_path = os.path.join(repo_dir, subdir)

        if not os.path.exists(subdir_path):
            return []

        if not os.path.isdir(subdir_path):
            return []

        return [
            f.split(".")[0]
            for f in os.listdir(subdir_path)
            if os.path.isfile(os.path.join(subdir_path, f))
        ]
