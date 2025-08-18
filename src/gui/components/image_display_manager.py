from typing import Any

import js  # type: ignore[import]

from gui.element import Element


class ImageDisplayManager:
    """Manages image display functionality."""

    image_container: Element
    image_element: Element
    placeholder_text: Element
    cursor_info: Element
    color_info: Element | None

    def __init__(
        self,
        container: Element,
        cursor_info_element: Element,
        color_info_element: Element | None = None,
    ) -> None:
        self.container = container
        self.current_image_src: str | None = None
        self.cursor_info = cursor_info_element
        self.color_info = color_info_element
        self._canvas_context: Any | None = None  # noqa: ANN401
        self._setup_elements()

    def _setup_elements(self) -> None:
        """Create the image container, image element, and placeholder text."""

        # Image container element
        self.image_container = Element(
            "div",
            parent=self.container,
            style="""
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        """,
        )

        # Image element
        self.image_element = Element(
            "img",
            parent=self.image_container,
            style="""
            max-width: 100%;
            max-height: 100%;
            display: none;
            object-fit: contain;
        """,
        )

        # Create placeholder text
        self.placeholder_text = Element(
            "div",
            parent=self.image_container,
            style="""
            font-size: 18px;
            color: #666;
            text-align: center;
            user-select: none;
        """,
        )
        self.placeholder_text.text = "Loading default image..."

        # Events
        self.image_element.on("mousemove", self._on_image_mouse_move)
        self.image_element.on("mouseleave", self._on_image_mouse_leave)
        self.image_element.on("load", self._on_image_load)

    def _on_image_load(self, _event: Any) -> None:  # noqa: ANN401
        """Prepare an offscreen canvas for pixel color sampling."""
        try:
            natural_width = self.image_element["naturalWidth"]
            natural_height = self.image_element["naturalHeight"]
            canvas = js.document.createElement("canvas")
            canvas.width = natural_width
            canvas.height = natural_height
            ctx = canvas.getContext("2d")
            ctx.drawImage(self.image_element.html_element, 0, 0)
            self._canvas_context = ctx
        except (AttributeError, RuntimeError) as exc:  # pragma: no cover
            print(f"Failed to prepare canvas for color sampling: {exc}")

    def _on_image_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        if not self.current_image_src:
            self.cursor_info.text = ""
            if self.color_info is not None:
                self.color_info.text = ""
            return

        natural_width = self.image_element["naturalWidth"]
        natural_height = self.image_element["naturalHeight"]
        intrinsic_mouse_x = int(
            (
                (event.clientX - self.image_element["offsetLeft"])
                / self.image_element["clientWidth"]
            )
            * natural_width,
        )
        intrinsic_mouse_y = int(
            (
                (event.clientY - self.image_element["offsetTop"])
                / self.image_element["clientHeight"]
            )
            * natural_height,
        )
        intrinsic_mouse_x = max(0, min(intrinsic_mouse_x, natural_width - 1))
        intrinsic_mouse_y = max(0, min(intrinsic_mouse_y, natural_height - 1))
        self.cursor_info.text = f"X: {intrinsic_mouse_x}, Y: {intrinsic_mouse_y}"

        if self.color_info is not None and self._canvas_context is not None:
            try:
                pixel = self._canvas_context.getImageData(
                    intrinsic_mouse_x, intrinsic_mouse_y, 1, 1
                ).data
                r, g, b = pixel[0], pixel[1], pixel[2]
                self.color_info.text = f"R: {r} G: {g} B: {b}"
            except (
                AttributeError,
                RuntimeError,
                ValueError,
            ) as exc:  # pragma: no cover
                self.color_info.text = "R: - G: - B: -"
                print(f"Color sample error: {exc}")

    def _on_image_mouse_leave(self, _event: Any) -> None:  # noqa: ANN401
        """Clear cursor info when mouse leaves the image."""
        self.cursor_info.text = ""
        if self.color_info is not None:
            self.color_info.text = ""

    def display_image(self, image_src: str) -> None:
        """Display an image in the preview area."""
        self.current_image_src = image_src
        self.image_element["src"] = image_src
        self.image_element["style"].display = "block"
        self.placeholder_text["style"].display = "none"

    def hide_image(self) -> None:
        """Hide the current image (useful during drag operations)."""
        if self.current_image_src:
            self.image_element["style"].display = "none"

    def show_image(self) -> None:
        """Show the current image again."""
        if self.current_image_src:
            self.image_element["style"].display = "block"

    def show_error(self, message: str) -> None:
        """Show an error message."""
        print(message)

    def _reset_placeholder(self) -> None:
        """Reset placeholder to original state."""
        if not self.current_image_src:
            self.placeholder_text.text = "Drop an image here or click to upload"
            self.placeholder_text["style"].color = "#666"
