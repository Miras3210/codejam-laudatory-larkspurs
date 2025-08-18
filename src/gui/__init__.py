import js  # type: ignore[import]

from gui.element import Element
from gui.layout import Layout

_base_style = """
html,
body {
    margin: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    font-family: monospace;
    background-color: var(--body-background-color);
    color: var(--text-color);
}

:root {
    color-scheme: dark;
    --body-background-color: #262626;
    --terminal-background-color: black;
    --terminal-output-color: white;
    --terminal-error-color: red;
    --terminal-success-color: green;
    --terminal-suggestion-color: rgb(119, 119, 119);
    --description-background-color: #1c1c1c;
    --description-button-border-color: #6b6b6b;
    --text-color: white;
    --image-preview-background: repeating-conic-gradient(#202020 0 25%, #0000 0 50%) 50% / 3em 3em;
    --separator-color: #6b6b6b;
}

#description {
    position: fixed;
    top: 0;
    right: 0;
    width: 5em;
    background-color: var(--description-background-color);
    transition: width 0.2s ease;
    z-index: 100;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#description.open {
    width: 40%;
    overflow-y: auto;
    overflow-x: hidden;
}

@media screen and (max-width: 600px) {
    #description {
        width: 100%;
        position: static;
    }

    #description.open {
        width: 100%;
    }

    #description > .expand-btn {
        min-height: 2em;
    }
}

.expand-btn:hover {
    filter: brightness(0.9);
    cursor: pointer;
}

#description > .description-content {
    transition: height 0.2s ease;
    display: flex;
    flex-direction: column;
    height: 0;
    overflow-y: hidden;
}

#description.open > .description-content {
    height: 100vh;
    width: 100%;
    overflow-y: auto;
}

#image-preview {
    cursor: pointer;
}

#image-preview:hover {
    background-color: #b8b8b8;
}

#image-preview.drag-over {
    background-color: #e3f2fd !important;
    border-color: #2196f3 !important;
}

#image-preview {
    cursor: pointer;
}

#image-preview:hover {
    background-color: #b8b8b8;
}

#image-preview.drag-over {
    background-color: #e3f2fd !important;
    border-color: #2196f3 !important;
}

.terminal-output, .user-input, .user-input > span {
    white-space: pre-wrap;
    word-break: break-all;
}

#terminal, #terminal * {
    color: var(--terminal-output-color);
    background-color: var(--terminal-background-color);
}

#terminal::selection, #terminal *::selection {
    color: var(--terminal-background-color);
    background-color: var(--terminal-output-color);
}

.terminal-input-verb-text, .command-verb-span {
    text-decoration: underline;
}
"""


def init_gui() -> Element:
    """Initialize the top-level layout for the application.

    ---

    Authors:
        - Jont
        - Ricky
    """
    # Hide the loading screen
    js.document.getElementById("loading").style.display = "none"

    body = Element(element=js.document.body)

    # Set the base style for the app
    base_style = Element("style")
    base_style.text = _base_style
    js.document.head.appendChild(base_style.html_element)

    # Create the main layout with image preview, separator, and terminal
    layout = Layout(parent=body)

    # Set up global event handlers
    body.on("click", lambda _: layout.description["classList"].remove("open"))
    body.on("mouseup", layout.handle_global_mouse_up)
    body.on("mousemove", layout.handle_global_mouse_move)

    return body
