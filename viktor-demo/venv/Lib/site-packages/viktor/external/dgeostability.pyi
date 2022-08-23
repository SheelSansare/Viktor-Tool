from .external_program import ExternalProgram as ExternalProgram
from io import BytesIO
from typing import Any, Optional

class DGeoStabilityAnalysis(ExternalProgram):
    input_file: Any
    def __init__(self, input_file: BytesIO) -> None: ...
    def get_output_file(self, extension: str = ...) -> Optional[BytesIO]: ...
