from logging import getLogger
from math import pi
from typing import Union

from communication.service.message import Message
from cortex.domain.objective.color import Color
from cortex.domain.objective.objective import Objective
from cortex.domain.objective.shape import Shape
from mobility.domain.angle import Angle
from mobility.domain.distance import Distance
from mobility.domain.operation.carefulOperation import CarefulOperation
from mobility.domain.operation.rotateOperation import RotateOperation
from mobility.domain.operation.translateOperation import TranslateOperation
from remote.translationError import TranslationError

logger = getLogger(__name__)
directionAngleMapping = {
    "up": Angle(0),
    "upRight": Angle(pi / 4),
    "right": Angle(pi / 2),
    "downRight": Angle(3 * pi / 4),
    "down": Angle(pi),
    "downLeft": Angle(-3 * pi / 4),
    "left": Angle(-pi / 2),
    "upLeft": Angle(-pi / 4),
}
shapes = {
    "Shapes:triangle": Shape.Triangle,
    "Shapes:square": Shape.Square,
    "Shapes:pentagon": Shape.Pentagon,
    "Shapes:circle": Shape.Circle
}
colors = {
    "Colors:red": Color.Red,
    "Colors:green": Color.Green,
    "Colors:blue": Color.Blue,
    "Colors:yellow": Color.Yellow
}


class MessageTranslator:
    @staticmethod
    def translate_to_translate_operation(message: Message) -> Union[TranslateOperation, CarefulOperation]:
        distance = message.get_data("distance")
        speed = message.get_data("speed")
        direction = message.get_data("direction")
        try:
            angle = directionAngleMapping[direction]
        except KeyError:
            logger.warning("invalid direction {}".format(direction))
            raise TranslationError()
        try:
            distance = float(distance)
        except ValueError:
            logger.warning('Cannot translate distance to float')
            raise TranslationError()
        if speed == "fast":
            return TranslateOperation(angle, Distance(distance))
        else:
            return CarefulOperation(angle, Distance(distance))

    @staticmethod
    def translate_to_rotate_operation(message: Message) -> RotateOperation:
        try:
            angle = float(message.get_data("angle"))
        except ValueError:
            logger.warning("cannot translate angle value to float")
            raise TranslationError
        return RotateOperation(Angle(angle * (2 * pi)))

    @staticmethod
    def translate_to_objective(message: Message) -> Objective:
        target = message.get_data('target')
        if target in shapes.keys():
            shape = shapes[target]
        else:
            shape = Shape.NoShape
        if target in colors.keys():
            color = colors[target]
        else:
            color = Color.NoColor
        zone = target[-1]
        if zone in ['0', '1', '2', '3']:
            destination = int(zone)
        else:
            destination = 0
        return Objective(destination, shape, color)
