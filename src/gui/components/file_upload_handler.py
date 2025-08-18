import base64
from collections.abc import Callable
from typing import Any

import js  # type: ignore[import]
from pyodide.ffi import create_proxy


class FileUploadHandler:
    """Handles file upload functionality via click and file processing.

    ---

    Authors:
        - Ricky
    """

    def __init__(
        self,
        on_file_processed: Callable[[str], None],
        on_error: Callable[[str], None],
    ) -> None:
        """Initialize file upload handler.

        Args:
            on_file_processed: Callback when file is successfully processed with data URL
            on_error: Callback when an error occurs during file processing

        ---

        :author: Ricky

        """
        self.on_file_processed = on_file_processed
        self.on_error = on_error

    def handle_click_upload(self, _event: Any) -> None:  # noqa: ANN401
        """Handle click to upload functionality.

        Args:
            _event: The mouse click event

        ---

        :author: Ricky

        """
        # Create a hidden file input
        file_input = js.document.createElement("input")
        file_input.type = "file"
        file_input.accept = "image/*"
        file_input.style.display = "none"

        # Handle file selection
        def handle_file_select(e: Any) -> None:  # noqa: ANN401
            files = e.target.files
            if files.length > 0:
                self.process_file(files.item(0))

        # Create a persistent proxy for the event handler
        file_select_proxy = create_proxy(handle_file_select)
        file_input.addEventListener("change", file_select_proxy)
        js.document.body.appendChild(file_input)
        file_input.click()
        js.document.body.removeChild(file_input)

    def process_file(self, file: Any) -> None:  # noqa: ANN401
        """Process the uploaded file and convert it to a data URL.

        Args:
            file: The file to process

        ---

        :author: Ricky

        """
        reader = js.FileReader.new()

        # Create a persistent proxy for the load event handler
        def on_load(event: Any) -> None:  # noqa: ANN401
            # Get the file data
            array_buffer = event.target.result

            # Convert to data URL for display
            try:
                # Convert array buffer to bytes
                uint8_array = js.Uint8Array.new(array_buffer)
                file_bytes = bytes(uint8_array.to_py())

                # Create base64 data URL
                file_b64 = base64.b64encode(file_bytes).decode("utf-8")

                # Determine MIME type based on file type
                mime_type = "image/png"  # Default
                if hasattr(file, "type") and file.type:
                    mime_type = str(file.type)

                data_url = f"data:{mime_type};base64,{file_b64}"
                self.on_file_processed(data_url)

            except ImportError as e:
                self.on_error(f"Error importing required modules: {e!s}")
            except (AttributeError, TypeError, ValueError) as e:
                self.on_error(f"Error processing image data: {e!s}")

        # Use create_proxy to ensure the event handler persists
        load_proxy = create_proxy(on_load)
        reader.addEventListener("load", load_proxy)
        reader.readAsArrayBuffer(file)
