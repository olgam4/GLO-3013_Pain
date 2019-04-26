from os import path
from tkinter import *
from tkinter import filedialog
from typing import List, Tuple

import cv2
import numpy as np


def select_camera_to_calibrate(max_camera_to_find: int) -> int:
    cameras: List[int] = []
    index: int = 0

    while index < max_camera_to_find:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, image = cap.read()
            cv2.imshow('Camera id:{}'.format(index), image)
            cv2.waitKey(1)
            cameras.append(index)

        index += 1
        cap.release()

    print('Valid camera indexes are {}'.format(cameras))
    camera_to_calibrate = int(input('Enter which camera to calibrate: '))
    cv2.destroyAllWindows()

    return camera_to_calibrate


class CalibrationParameters:
    def __init__(self, grid_width: int, grid_height: int, grid_square_size: float) -> None:
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height
        self.grid_square_size: float = grid_square_size
        self.window_size: Tuple[int, int] = (11, 11)
        self.zero_zone: Tuple[int, int] = (-1, -1)
        self.maximum_iteration: int = 30
        self.move_epsilon: float = 0.001


def ask_calibration_parameters() -> CalibrationParameters:
    grid_width: int = int(input('Enter calibration grid width [int]: '))
    grid_height: int = int(input('Enter calibration grid height [int]: '))
    grid_square_size: float = float(input('Enter calibration grid square size [float]: '))
    return CalibrationParameters(grid_width, grid_height, grid_square_size)


def calibrate_camera(camera_id, calibration_parameters: CalibrationParameters) -> Tuple[np.ndarray, np.ndarray]:
    print('Press "u" to use the current image in the calibration process')
    print('Press "c" to continue with the calibration process once enough images have been selected')
    print('Press "q" to quit the calibration process')
    print('Press any key to skip the current image from the calibration process')

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    object_points: np.ndarray = np.zeros(
        (calibration_parameters.grid_width * calibration_parameters.grid_height, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:calibration_parameters.grid_width, 0:calibration_parameters.grid_height]\
        .T.reshape(-1, 2)
    object_points[:, :2] *= calibration_parameters.grid_square_size

    # Arrays to store object points and image points from all the images.
    object_points_detected = []  # 3d point in real world space
    image_points_detected = []  # 2d points in image plane.

    should_calibrate: bool = True
    should_continue: bool = True
    cap = cv2.VideoCapture(camera_id)
    while cap.isOpened() and should_continue:
        is_success: bool = True
        image: np.ndarray = None
        is_success, image = cap.read()
        if is_success:
            gray_image: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            is_success, corners = cv2.findChessboardCorners(
                gray_image, (calibration_parameters.grid_width, calibration_parameters.grid_height), None)

            if is_success:
                termination_criterion = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                                         calibration_parameters.maximum_iteration, calibration_parameters.move_epsilon)

                corners2 = cv2.cornerSubPix(
                    gray_image, corners, calibration_parameters.window_size, calibration_parameters.zero_zone,
                    termination_criterion)

                image = cv2.drawChessboardCorners(image,
                                                  (calibration_parameters.grid_width,
                                                   calibration_parameters.grid_height),
                                                  corners2, is_success)
                cv2.imshow('Calibration Window', image)

                key = cv2.waitKey(0)
                if key == ord('u'):
                    object_points_detected.append(object_points)
                    image_points_detected.append(corners2)
                elif key == ord('c'):
                    should_continue = False
                elif key == ord('q'):
                    should_calibrate = False
                    should_continue = False
            else:
                cv2.imshow('Calibration Window', image)
                key = cv2.waitKey(0)
                if key == ord('q'):
                    should_calibrate = False
                    should_continue = False

    if should_calibrate:
        rotation_vector: np.ndarray = None
        translation_vector: np.ndarray = None
        ret, camera_matrix, distortion_coefficients, rotation_vector, translation_vector = cv2.calibrateCamera(
            object_points_detected, image_points_detected, gray_image.shape[::-1], None, None)

        mean_error: float = 0
        for i in range(len(object_points_detected)):
            projected_image_pts, _ = cv2.projectPoints(
                object_points_detected[i], rotation_vector[i], translation_vector[i], camera_matrix,
                distortion_coefficients)
            error = cv2.norm(image_points_detected[i], projected_image_pts, cv2.NORM_L2) / len(projected_image_pts)
            mean_error += error
        mean_error /= len(object_points_detected)
        print("mean error: {}. This should as close to zero as possible".format(mean_error))

        cap.release()
        cv2.destroyAllWindows()
        return camera_matrix, distortion_coefficients

    cap.release()
    cv2.destroyAllWindows()
    raise RuntimeError('The calibration process could not terminate properly')


def show_calibrated_camera(camera_matrix: np.ndarray, distortion_coefficients: np.ndarray, camera_id) -> None:
    print('Press "q" to quit the display of the calibration')

    cap = cv2.VideoCapture(camera_id)
    while cap.isOpened():
        ret, image = cap.read()
        h, w = image.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))

        dst = cv2.undistort(image, camera_matrix, distortion_coefficients, None, new_camera_mtx)

        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv2.imshow('Distorted Image', image)
        cv2.imshow('Undistorted Image', dst)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def save_calibration(camera_matrix: np.ndarray, distortion_coefficients: np.ndarray) -> None:
    root = Tk()
    filepath: path = filedialog.asksaveasfilename(filetypes=[('Numpy Files', '.npz')])

    if filepath:
        np.savez(filepath, camera_matrix=camera_matrix, distortion_coefficients=distortion_coefficients)
        print('Calibration Saved to: {}'.format(filepath))
    else:
        print('Calibration Save Canceled.')

    root.destroy()
    root.mainloop()


def main():
    print(cv2.__version__)

    camera_to_calibrate: int = select_camera_to_calibrate(10)

    calibration_parameters: CalibrationParameters = ask_calibration_parameters()

    camera_matrix: np.ndarray = None
    distortion_coefficients: np.ndarray = None
    camera_matrix, distortion_coefficients = calibrate_camera(camera_to_calibrate, calibration_parameters)

    show_calibrated_camera(camera_matrix, distortion_coefficients, camera_to_calibrate)
    save_calibration(camera_matrix, distortion_coefficients)


if __name__ == "__main__":
    main()
