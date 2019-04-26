from vision.domain.visionError import VisionError, VisionFactoryError


class CameraDoesNotExistError(VisionError):
    """Exception raised when trying to create a camera with an invalid index"""

    def __init__(self, index: int) -> None:
        super().__init__('[OpenCV] Camera with id: {} does not exist'.format(index))


class AcquisitionError(VisionError):
    """Exception raised when an image could not be capture from a camera"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Image could not be captured')


class HomeCouldNotBeFound(VisionError):
    """Exception raised when a suitable Home contours could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Home square could not be found')


class SourceCouldNotBeFound(VisionError):
    """Exception raised when a suitable Source contours could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Source zone could not be found')


class GoalCouldNotBeFound(VisionError):
    """Exception raised when a suitable Goal contours could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Goal zone could not be found')


class RobotCouldNotBeFound(VisionError):
    """Exception raised when the robot could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Robot could not be found')


class PlayAreaCouldNotBeFound(VisionError):
    """Exception raised when the play area could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Play Area could not be found')


class ObstaclesCouldNotBeFound(VisionError):
    """Exception raised when obstacles could not be found"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Obstacles could not be found')


class CameraCalibrationCouldNotBeCreatedUsingImage(VisionFactoryError):
    """Exception raised when the camera calibration could not be created from image"""

    def __init__(self) -> None:
        super().__init__('[OpenCV] Camera Calibration could not be created using current image')
