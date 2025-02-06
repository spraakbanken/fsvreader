class MissingError(Exception):
    """Raised when something is missing."""

    def __init__(self, *, title: str, header: str, message: str) -> None:
        self.title = title
        self.header = header
        self.message = message


class UnknownDirError(MissingError):
    """Raised when an dir is missing."""

    def __init__(self, *, dir: str) -> None:
        super().__init__(
            title="Okänd mapp", header="Mapp saknas", message=f"Mappen '{dir}' saknas"
        )


class UnknownFileError(MissingError):
    """Raised when a file is missing."""

    def __init__(self, *, dir: str, file: str) -> None:
        super().__init__(
            title="Okänd fil",
            header="Fil saknas",
            message=f"Filen '{file}' saknas i mappen '{dir}'",
        )
