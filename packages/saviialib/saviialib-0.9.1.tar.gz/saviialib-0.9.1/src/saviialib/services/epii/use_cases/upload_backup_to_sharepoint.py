import asyncio
import os
from time import time
import saviialib.services.epii.use_cases.constants.upload_backup_to_sharepoint_constants as c
from saviialib.general_types.error_types.api.epii_api_error_types import (
    BackupEmptyError,
    BackupSourcePathError,
    BackupUploadError,
)
from saviialib.general_types.error_types.common import (
    SharepointClientError,
)
from saviialib.libs.files_client import FilesClient, FilesClientInitArgs, ReadArgs
from saviialib.libs.sharepoint_client import (
    SharepointClient,
    SharepointClientInitArgs,
    SpUploadFileArgs,
)
from saviialib.services.epii.utils.upload_backup_to_sharepoint_utils import (
    calculate_percentage_uploaded,
    count_files_in_directory,
    directory_exists,
    extract_error_message,
    parse_execute_response,
    show_upload_result,
)

from .types.upload_backup_to_sharepoint_types import (
    UploadBackupToSharepointUseCaseInput,
)
from .constants.upload_backup_to_sharepoint_constants import LOGGER


class UploadBackupToSharepointUsecase:
    def __init__(self, input: UploadBackupToSharepointUseCaseInput):
        self.sharepoint_config = input.sharepoint_config
        self.local_backup_source_path = input.local_backup_source_path
        self.destination_folders = input.destination_folders
        self.files_client = self._initialize_files_client()
        self.log_history = []
        self.grouped_files_by_folder = None
        self.total_files = None

    def _initialize_files_client(self):
        return FilesClient(FilesClientInitArgs(client_name="aiofiles_client"))

    async def _extract_filesnames_by_folder(self) -> dict[str, list[str]]:
        """Groups files by their parent folder."""
        backup_folder_exists = await asyncio.to_thread(
            os.path.exists, self.local_backup_source_path
        )
        if not backup_folder_exists:
            return {}
        folder_names = await asyncio.to_thread(
            os.listdir, self.local_backup_source_path
        )
        return {
            folder_name: [
                file_name
                for file_name in await asyncio.to_thread(
                    os.listdir, os.path.join(self.local_backup_source_path, folder_name)
                )
            ]
            for folder_name in folder_names
        }

    def _save_log_history(self) -> None:
        text_file = "\n".join(self.log_history)
        log_history_filepath = "BACKUP_LOG_HISTORY.log"
        with open(log_history_filepath, "w") as file:
            file.write(text_file)

    async def export_file_to_sharepoint(
        self, folder_name: str, file_name: str, file_content: bytes
    ) -> tuple[bool, str]:
        """Uploads a file to the specified folder in SharePoint."""
        uploaded = None
        error_message = ""

        try:
            sharepoint_client = SharepointClient(
                SharepointClientInitArgs(
                    self.sharepoint_config, client_name="sharepoint_rest_api"
                )
            )
        except ConnectionError as error:
            raise SharepointClientError(error)

        async with sharepoint_client:
            try:
                destination_folder = self.destination_folders.get(
                    folder_name, folder_name
                )
                folder_url = f"{c.SHAREPOINT_BASE_URL}/{destination_folder}"
                args = SpUploadFileArgs(
                    folder_relative_url=folder_url,
                    file_content=file_content,
                    file_name=file_name,
                )
                await sharepoint_client.upload_file(args)
                uploaded = True
            except ConnectionError as error:
                error_message = str(error)
                uploaded = False

        return uploaded, error_message

    async def upload_and_log_progress_task(self, folder_name, file_name) -> dict:
        """Task for uploads a file and logs progress."""
        uploading_message = (
            f"[BACKUP] Uploading file '{file_name}' from '{folder_name}' "
        )
        self.log_history.append(uploading_message)
        LOGGER.debug(uploading_message)
        file_path = os.path.join(self.local_backup_source_path, folder_name, file_name)
        file_content = await self.files_client.read(ReadArgs(file_path, mode="rb"))
        uploaded, error_message = await self.export_file_to_sharepoint(
            folder_name, file_name, file_content
        )
        result_message = show_upload_result(uploaded, file_name)
        LOGGER.debug(result_message)
        self.log_history.append(result_message)
        return {
            "parent_folder": folder_name,
            "file_name": file_name,
            "uploaded": uploaded,
            "error_message": error_message,
        }

    async def retry_upload_failed_files(self, results) -> None:
        failed_files = [item for item in results if not item["uploaded"]]
        tasks = []
        retry_message = (
            f"[BACKUP] Retrying upload for {len(failed_files)} failed files... 🚨"
        )
        self.log_history.append(retry_message)
        LOGGER.debug(retry_message)
        for file in failed_files:
            tasks.append(
                self.upload_and_log_progress_task(
                    file["parent_folder"], file["file_name"]
                )
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = calculate_percentage_uploaded(results, self.total_files)
        if success < 100.0:
            raise BackupUploadError(reason=extract_error_message(results, success))
        else:
            successful_upload_retry = (
                "[BACKUP] All files uploaded successfully after retry."
            )
            self.log_history.append(successful_upload_retry)
            LOGGER.debug(successful_upload_retry)
            self._save_log_history()
            return parse_execute_response(results)

    async def execute(self):
        """Exports all files from the local backup folder to SharePoint cloud."""
        self.grouped_files_by_folder = await self._extract_filesnames_by_folder()
        self.total_files = sum(
            len(files) for files in self.grouped_files_by_folder.values()
        )
        tasks = []
        start_time = time()

        # Check if the local path exists in the main directory
        if not await directory_exists(self.local_backup_source_path):
            raise BackupSourcePathError(
                reason=f"'{self.local_backup_source_path}' doesn't exist."
            )

        # Check if the current folder only have files.
        items = [
            item
            for item in await asyncio.to_thread(
                os.listdir, self.local_backup_source_path
            )
        ]
        for item in items:
            folder_included = item in self.destination_folders.keys()
            is_file = not await asyncio.to_thread(
                os.path.isdir, os.path.join(self.local_backup_source_path, item)
            )

            if not folder_included and not is_file:
                raise BackupSourcePathError(
                    reason=(
                        f"'{item}' must be included in the destination folders dictionary",
                    )
                )
            elif folder_included and is_file:
                print(folder_included, is_file)
                raise BackupSourcePathError(reason=(f"'{item}' must be a directory.",))

        if self.total_files == 0:
            no_files_message = (
                f"[BACKUP] {self.local_backup_source_path} has no files ⚠️"
            )
            self.log_history.append(no_files_message)
            LOGGER.debug(no_files_message)
            raise BackupEmptyError
        # Create task for each file stored in the the local backup folder.
        for folder_name in self.grouped_files_by_folder:
            if (
                await count_files_in_directory(
                    self.local_backup_source_path, folder_name
                )
                == 0
            ):
                empty_folder_message = f"[BACKUP] The folder '{folder_name}' is empty ⚠️"
                LOGGER.debug(empty_folder_message)
                self.log_history.append(empty_folder_message)
                continue
            extracting_files_message = (
                "[BACKUP]" + f" Extracting files from '{folder_name} ".center(15, "*")
            )
            self.log_history.append(extracting_files_message)
            LOGGER.debug(extracting_files_message)
            for file_name in self.grouped_files_by_folder[folder_name]:
                tasks.append(self.upload_and_log_progress_task(folder_name, file_name))

        # Execution of multiple asynchronous tasks for files migration.
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = calculate_percentage_uploaded(results, self.total_files)
        if success < 100.0:
            await self.retry_upload_failed_files(results)
        else:
            end_time = time()
            backup_time = end_time - start_time
            successful_backup_message = (
                f"[BACKUP] Migration time: {backup_time:.2f} seconds ✨"
            )
            self.log_history.append(successful_backup_message)

            finished_backup_message = (
                "[BACKUP] All the files were uploaded successfully 🎉"
            )
            self.log_history.append(finished_backup_message)

            self._save_log_history()
            return parse_execute_response(results)
