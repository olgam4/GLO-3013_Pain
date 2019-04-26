from logging import getLogger
from threading import Event, Thread

from application.domain.iBaseWatcher import IBaseWatcher
from application.infrastructure.championshipBaseWatcher import ChampionshipBaseWatcher
from application.infrastructure.remoteCerebrum import RemoteCerebrum
from communication.service.communicationService import CommunicationService
from communication.service.displayService import DisplayService
from communication.service.message import Message
from cortex.domain.cortex import Cortex
from cortex.domain.directionCortex import DirectionCortex
from dexterity.service.dexterityService import DexterityService
from remote.messageTranslator import MessageTranslator
from remote.remoteService import RemoteService
from remote.translationError import TranslationError
from sight.service.sightService import SightService

logger = getLogger(__name__)


class RemoteBaseWatcher(IBaseWatcher):
    def __init__(self, communication_service: CommunicationService, remote_service: RemoteService,
                 display_service: DisplayService, message_translator: MessageTranslator,
                 dexterity_service: DexterityService, remote_cerebrum: RemoteCerebrum,
                 cortex: Cortex, direction_cortex: DirectionCortex,
                 championship_watcher: ChampionshipBaseWatcher, sight_service: SightService) -> None:
        self._direction_cortex = direction_cortex
        self._cortex = cortex
        self._stopped = Event()
        self._dexterity_service = dexterity_service
        self._communication_service = communication_service
        self._display_service = display_service
        self._remote_service = remote_service
        self._message_translator = message_translator
        self._remote_cerebrum = remote_cerebrum
        self._championship_watcher = championship_watcher
        self._sight_service = sight_service
        self._handles = {}
        self._fill_handles()

        self._command_thread = Thread()

    def run(self) -> None:
        while not self._stopped.is_set():
            try:
                message = self._communication_service.receive_message()
            except TimeoutError:
                break
            logger.debug(message.serialize())
            try:
                self._handles[message.title](message)
            except KeyError:
                logger.warning(format("Invalid operation {}", message.title))
        self._remote_cerebrum.stop()

    def stop(self) -> None:
        self._stopped.set()

    def _fill_handles(self) -> None:
        self._handles["charge_subroutine"] = self._charge_subroutine
        self._handles["go_home_subroutine"] = self._go_home_subroutine
        self._handles["read_qr_subroutine"] = self._read_qr_subroutine
        self._handles["grab_subroutine"] = self._grab_subroutine
        self._handles["drop_subroutine"] = self._drop_subroutine
        self._handles["switch_light_subroutine"] = self._switch_light_subroutine
        self._handles["directional_movement"] = self._directional_movement
        self._handles["rotational_movement"] = self._rotational_movement
        self._handles["activate_magnet"] = self._activate_magnet
        self._handles["deactivate_magnet"] = self._deactivate_magnet
        self._handles["discharge_magnet"] = self._discharge_magnet
        self._handles["update_directions"] = self._update_directions
        self._handles["goal_pathable"] = self._championship_watcher.set_goal_pathable
        self._handles["charge_station_pathable"] = self._championship_watcher.set_charge_station_pathable
        self._handles["qr_code_pathable"] = self._championship_watcher.set_qr_code_pathable
        self._handles["home_pathable"] = self._championship_watcher.set_home_pathable
        self._handles["source_pathable"] = self._championship_watcher.set_source_pathable
        self._handles["position"] = self._championship_watcher.update_position
        self._handles["start_charging"] = self._championship_watcher.start_charging
        self._handles["lost_connection"] = self._championship_watcher.lost_connection
        self._handles["charge_done"] = self._championship_watcher.charge_done
        self._handles["championship"] = self._championship
        self._handles["look_down"] = self._look_down
        self._handles["look_ahead"] = self._look_ahead

    def _championship(self, message: Message) -> None:
        self._command_thread = Thread(target=self._championship_func, args=[message])
        self._command_thread.start()

    def _championship_func(self, message: Message) -> None:
        self._cortex.run()
        self._complete_command(message.title)

    def _charge_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._charge_subroutine_func, args=[message])
        self._command_thread.start()

    def _charge_subroutine_func(self, message: Message) -> None:
        self._cortex.charge_subroutine()
        self._complete_command(message.title)

    def _go_home_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._go_home_subroutine_func, args=[message])
        self._command_thread.start()

    def _go_home_subroutine_func(self, message: Message) -> None:
        self._cortex.go_home_subroutine()
        self._complete_command(message.title)

    def _read_qr_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._read_qr_subroutine_func, args=[message])
        self._command_thread.start()

    def _read_qr_subroutine_func(self, message: Message) -> None:
        self._cortex.read_qr_subroutine()
        self._complete_command(message.title)

    def _grab_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._grab_subroutine_func, args=[message])
        self._command_thread.start()

    def _grab_subroutine_func(self, message: Message) -> None:
        self._cortex.grab_subroutine(self._message_translator.translate_to_objective(message))
        self._complete_command(message.title)

    def _drop_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._drop_subroutine_func, args=[message])
        self._command_thread.start()

    def _drop_subroutine_func(self, message: Message) -> None:
        self._cortex.drop_subroutine(self._message_translator.translate_to_objective(message))
        self._complete_command(message.title)

    def _switch_light_subroutine(self, message: Message) -> None:
        self._command_thread = Thread(target=self._switch_light_subroutine_func, args=[message])
        self._command_thread.start()

    def _switch_light_subroutine_func(self, message: Message) -> None:
        self._display_service.switch_light()
        self._complete_command(message.title)

    def _directional_movement(self, message: Message) -> None:
        self._command_thread = Thread(target=self._directional_movement_func, args=[message])
        self._command_thread.start()

    def _directional_movement_func(self, message: Message) -> None:
        try:
            translate_operation = self._message_translator.translate_to_translate_operation(message)
            self._remote_service.execute_operation(translate_operation)
        except TranslationError:
            pass
        self._complete_command(message.title)

    def _rotational_movement(self, message: Message) -> None:
        self._command_thread = Thread(target=self._rotational_movement_func, args=[message])
        self._command_thread.start()

    def _rotational_movement_func(self, message: Message) -> None:
        try:
            rotate_operation = self._message_translator.translate_to_rotate_operation(message)
            self._remote_service.execute_operation(rotate_operation)
        except TranslationError:
            pass
        self._complete_command(message.title)

    def _activate_magnet(self, message: Message) -> None:
        self._command_thread = Thread(target=self._activate_magnet_func, args=[message])
        self._command_thread.start()

    def _activate_magnet_func(self, message: Message) -> None:
        self._dexterity_service.grab()
        self._complete_command(message.title)

    def _deactivate_magnet(self, message: Message) -> None:
        self._command_thread = Thread(target=self._deactivate_magnet_func, args=[message])
        self._command_thread.start()

    def _deactivate_magnet_func(self, message: Message) -> None:
        self._dexterity_service.let_go()
        self._complete_command(message.title)

    def _discharge_magnet(self, message: Message) -> None:
        self._command_thread = Thread(target=self._discharge_magnet_func, args=[message])
        self._command_thread.start()

    def _discharge_magnet_func(self, message: Message) -> None:
        self._dexterity_service.discharge()
        self._complete_command(message.title)

    def _update_directions(self, message: Message) -> None:
        self._command_thread = Thread(target=self._update_directions_func, args=[message])
        self._command_thread.start()

    def _update_directions_func(self, message: Message) -> None:
        self._direction_cortex.update_directions()
        self._complete_command(message.title)

    def _look_down(self, message: Message) -> None:
        self._command_thread = Thread(target=self._look_down_func, args=[message])
        self._command_thread.start()

    def _look_down_func(self, message: Message) -> None:
        self._sight_service.look_down()
        self._complete_command(message.title)

    def _look_ahead(self, message: Message) -> None:
        self._command_thread = Thread(target=self._look_ahead_func, args=[message])
        self._command_thread.start()

    def _look_ahead_func(self, message: Message) -> None:
        self._sight_service.look_ahead()
        self._complete_command(message.title)

    def _complete_command(self, command: str) -> None:
        returned_message = Message("command_completed", command=command)
        self._communication_service.send_message(returned_message)
