from typing import Any

from gui.components.drag_drop_handler import DragDropHandler
from gui.components.file_upload_handler import FileUploadHandler
from gui.components.image_display_manager import ImageDisplayManager
from gui.element import Element, HTMLElement


class ImagePreview(Element):
    """An image preview component for displaying an image with a drag-drop upload functionality.

    ---

    Authors:
        - Jont
        - Ricky
    """

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        """Initialize the image preview element.

        Args:
            parent: The parent element to attach this preview to

        ---

        Authors:
            - Jont (`cursor_info`)
            - Ricky (`color_info`)

        """
        super().__init__(
            tag_name="div",
            parent=parent,
            id="image-preview",
            style="""
            background: var(--image-preview-background);
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

        # Cursor info element
        self.cursor_info = Element(
            "div",
            parent=self,
            style="""
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: white;
            font-size: 14px;
            z-index: 1;
            """,
        )

        # Color info element
        self.color_info = Element(
            "div",
            parent=self,
            style="""
            position: absolute;
            bottom: 10px;
            right: 10px;
            color: white;
            font-size: 14px;
            z-index: 1;
            text-align: right;
            """,
        )
        self.color_info.text = "R: - G: - B: -"

        # Initialize the image display manager
        self.image_manager = ImageDisplayManager(
            self,
            self.cursor_info,
            self.color_info,
        )

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
        self.image = None

    def _on_file_processed(self, data_url: str) -> None:
        """Handle successfully processed file.

        Args:
            data_url: The data URL of the processed image

        ---

        :author: Ricky

        """
        if self.image is not None:
            self.image.load_from_image_link(data_url)
        else:
            self.image_manager.display_image(data_url)

    def _on_error(self, error_message: str) -> None:
        """Handle file processing error.

        Args:
            error_message: The error message to display

        ---

        :author: Ricky

        """
        self.image_manager.show_error(error_message)

    def _on_file_drop(self, file: Any) -> None:  # noqa: ANN401
        """Handle file drop from drag and drop.

        Args:
            file: The dropped file

        ---

        :author: Ricky

        """
        self.file_handler.process_file(file)

    def display_image(self, image_src: str) -> None:
        """Display an image in the preview area.

        Args:
            image_src: The source URL of the image to display

        ---

        :author: Ricky

        """
        self.image_manager.display_image(image_src)
