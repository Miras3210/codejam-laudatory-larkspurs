from typing import Any

from gui.components.drag_drop_handler import DragDropHandler
from gui.components.file_upload_handler import FileUploadHandler
from gui.components.image_display_manager import ImageDisplayManager
from gui.element import Element, HTMLElement


class ImagePreview(Element):
    """A component for displaying an image preview with a drag-drop upload functionality.

    Authors:
        Jont
        Ricky
    """

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            parent=parent,
            id="image-preview",
            style="""
            background-color: var(--image-preview-background-color);
            height: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            flex-shrink: 0;
            position: relative;
            border: 2px dashed transparent;
            transition: border-color 0.3s ease, background-color 0.3s ease;
        """,
        )
        self.class_name = "image-preview"

        # Initialize the image display manager
        self.image_manager = ImageDisplayManager(self)

        # Initialize the file upload handler
        self.file_handler = FileUploadHandler(
            on_file_processed=self._on_file_processed,
            on_error=self._on_error,
        )

        # Initialize the drag drop handler
        self.drag_handler = DragDropHandler(
            element=self,
            on_file_drop=self._on_file_drop,
            on_drag_enter=self.image_manager.hide_image,
            on_drag_leave=self.image_manager.show_image,
            on_error=self._on_error,
        )

        # Set up drag overlay and events
        self.drag_overlay = self.drag_handler.setup_drag_overlay()
        self.drag_handler.setup_events()

        # Add click to upload functionality
        self.on("click", self.file_handler.handle_click_upload)

    def _on_file_processed(self, data_url: str) -> None:
        """Handle successfully processed file."""
        self.image_manager.display_image(data_url)

    def _on_error(self, error_message: str) -> None:
        """Handle file processing error."""
        self.image_manager.show_error(error_message)

    def _on_file_drop(self, file: Any) -> None:  # noqa: ANN401
        """Handle file drop from drag and drop."""
        self.file_handler.process_file(file)

    def display_image(self, image_src: str) -> None:
        """Display an image in the preview area."""
        self.image_manager.display_image(image_src)
