from vision.domain.visionError import VisionError


class VisionServiceNotInitialized(VisionError):
    """Exception raised when the VisionService has not yet been initialized"""

    def __init__(self) -> None:
        super().__init__('VisionService not initialized')
