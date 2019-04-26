import tkinter as tk
from tkinter import ttk

from application.domain.application import Application
from application.infrastructure.applicationWorker import ApplicationWorker
from application.infrastructure.chargeStationWatcher import ChargeStationWatcher
from application.infrastructure.robotWatcher import RobotWatcher
from application.infrastructure.tkinterUi import TkinterUi
from communication.infrastructure.socketRobotConnector import SocketRobotConnector
from communication.service.communicationService import CommunicationService
from light.service.lightService import LightService
from objective.service.objectiveService import ObjectiveService
from pathDrawing.infrastructure.openCvDrawer import OpenCvDrawer
from pathDrawing.service.pathDrawingService import PathDrawingService
from pathfinding.domain.angle import Angle
from pathfinding.domain.table import Table
from pathfinding.infrastructure.adaptivePathableCatalog import AdaptivePathableCatalog
from pathfinding.infrastructure.approachPositionFinder import ApproachPositionFinder
from pathfinding.infrastructure.grassfirePathfinderFactory import GrassfirePathfinderFactory
from pathfinding.infrastructure.pathableCatalog import PathableCatalog
from pathfinding.service.pathService import PathService
from pathfinding.service.pathfindingService import PathfindingService
from pathfinding.service.positionService import PositionService
from prehensor.infrastructure.chargeStation import ChargeStation
from prehensor.service.prehensorService import PrehensorService
from remote.infrastructure.remoteControl import RemoteControl
from remote.service.remoteService import RemoteService
from timer.infrastructure.pythonChronometer import PythonChronometer
from timer.service.timeService import TimeService
from ui.domain.directionalControl import DirectionalControl
from ui.domain.indicator.charge import Charge
from ui.domain.indicator.indicators import Indicators
from ui.domain.indicator.light import Light
from ui.domain.indicator.objective import Objective
from ui.domain.indicator.timer import Timer
from ui.domain.onBoardCamera import OnBoardCamera
from ui.domain.subroutine.championshipSubroutine import ChampionshipSubroutine
from ui.domain.subroutine.chargeSubroutine import ChargeSubroutine
from ui.domain.subroutine.dropSubroutine import DropSubroutine
from ui.domain.subroutine.goHomeSubroutine import GoHomeSubroutine
from ui.domain.subroutine.grabSubroutine import GrabSubroutine
from ui.domain.subroutine.magnetSubroutine import MagnetSubroutine
from ui.domain.subroutine.readQrSubroutine import ReadQrSubroutine
from ui.domain.subroutine.sightSubroutine import SightSubroutine
from ui.domain.subroutine.subroutines import Subroutines
from ui.domain.subroutine.updateDirectionsSubroutine import UpdateDirectionsSubroutine
from ui.domain.subroutine.winSubroutine import WinSubroutine
from ui.domain.worldCameraSelector import WorldCameraSelector
from ui.infrastructure.remoteMainView import RemoteMainView
from ui.infrastructure.remoteSubroutineRunner import RemoteSubroutineRunner
from vision.infrastructure.cvCameraCalibrationFactory import CvCameraCalibrationFactory
from vision.infrastructure.cvCameraFactory import CvCameraFactory
from vision.infrastructure.cvGoalFinder import CvGoalFinder
from vision.infrastructure.cvImageDrawer import CvImageDrawer
from vision.infrastructure.cvObstacleFinder import CvObstacleFinder
from vision.infrastructure.cvPlayAreaFinder import CvPlayAreaFinder
from vision.infrastructure.cvRobotFinder import CvRobotFinder
from vision.infrastructure.cvSourceFinder import CvSourceFinder
from vision.service.robotCameraService import RobotCameraService
from vision.service.visionService import VisionService


class Remote:
    def __init__(self, port: int, address: str, timeout: float) -> None:
        self._play_area_finder = CvPlayAreaFinder()
        self._vision_service = VisionService(CvCameraFactory(), CvCameraCalibrationFactory(self._play_area_finder),
                                             CvImageDrawer(), self._play_area_finder, CvGoalFinder(),
                                             CvSourceFinder(), CvObstacleFinder(), CvRobotFinder())
        self._time_service = TimeService(PythonChronometer())
        self._robot_camera_service = RobotCameraService()
        self._robot_connector = SocketRobotConnector(port, address, timeout)
        self._communication_service = CommunicationService(self._robot_connector)
        self._position_service = PositionService(self._vision_service, self._communication_service)
        self._light_service = LightService()
        self._objective_service = ObjectiveService()
        self._remote_control = RemoteControl(self._communication_service)
        self._remote_service = RemoteService(self._remote_control)
        self._subroutine_runner = RemoteSubroutineRunner(self._remote_service)
        pathfinder_factory = GrassfirePathfinderFactory(Table(111, 231, -1, 27, Angle(0), 15))
        self._pathable_catalog = PathableCatalog(self._vision_service, pathfinder_factory, ApproachPositionFinder())
        self._pathfinding_service = PathfindingService(self._pathable_catalog)
        self._path_service = PathService()
        self._path_drawing_service = PathDrawingService(OpenCvDrawer(), self._vision_service, self._path_service)
        self._prehensor_service = PrehensorService()

    def application(self) -> Application:
        tkinter_ui = self._make_tkinter_ui()
        robot_watcher = self._make_robot_watcher()
        application_worker = self._make_application_worker()
        charge_station = ChargeStation()
        charge_station_watcher = ChargeStationWatcher(self._communication_service, charge_station)
        return Application(tkinter_ui, robot_watcher, application_worker, charge_station_watcher)

    def _make_tkinter_ui(self) -> TkinterUi:
        return TkinterUi(RemoteMainView(None, self._make_subroutines, self._make_world_camera_selector,
                                        self._make_on_board_camera, self._make_directional_control,
                                        self._make_indicators))

    def _make_robot_watcher(self) -> RobotWatcher:
        return RobotWatcher(self._communication_service, self._light_service, self._remote_control,
                            self._robot_camera_service, self._pathfinding_service, self._position_service,
                            self._path_service, self._prehensor_service, self._objective_service)

    def _make_application_worker(self) -> ApplicationWorker:
        return ApplicationWorker(self._vision_service, self._time_service)

    def _make_subroutines(self, parent: ttk.Frame) -> Subroutines:
        subroutines = Subroutines(parent)
        subroutines.add(ChargeSubroutine(subroutines, self._subroutine_runner),
                        text="charge", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(ReadQrSubroutine(subroutines, self._subroutine_runner, self._make_objective),
                        text="qrCode", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(GrabSubroutine(subroutines, self._subroutine_runner),
                        text="grab", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(DropSubroutine(subroutines, self._subroutine_runner),
                        text="drop", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(GoHomeSubroutine(subroutines, self._subroutine_runner),
                        text="goHome", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(WinSubroutine(subroutines, self._subroutine_runner, self._make_light),
                        text="win!", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(MagnetSubroutine(subroutines, self._subroutine_runner),
                        text="magnet", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(UpdateDirectionsSubroutine(subroutines, self._subroutine_runner),
                        text="direction", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(SightSubroutine(subroutines, self._subroutine_runner),
                        text="sight", sticky=tk.N + tk.W + tk.E + tk.S)
        subroutines.add(ChampionshipSubroutine(subroutines, self._subroutine_runner, self._time_service),
                        text="championship", sticky=tk.N + tk.W + tk.E + tk.S)
        return subroutines

    def _make_indicators(self, parent: ttk.Frame) -> Indicators:
        return Indicators(parent, self._make_objective, self._make_light, self._make_charge, self._make_timer)

    def _make_directional_control(self, parent: ttk.Frame) -> DirectionalControl:
        return DirectionalControl(parent, self._subroutine_runner)

    def _make_on_board_camera(self, parent: ttk.Frame) -> OnBoardCamera:
        return OnBoardCamera(parent, self._robot_camera_service)

    def _make_objective(self, parent: ttk.Frame) -> Objective:
        return Objective(parent, self._objective_service)

    def _make_light(self, parent: ttk.Frame) -> Light:
        return Light(parent, self._light_service)

    def _make_charge(self, parent: ttk.Frame) -> Charge:
        return Charge(parent, self._prehensor_service)

    def _make_timer(self, parent: ttk.Frame) -> Timer:
        return Timer(parent, self._time_service)

    def _make_world_camera_selector(self, parent: ttk.Frame) -> WorldCameraSelector:
        return WorldCameraSelector(parent, self._vision_service, self._path_drawing_service)
