from cortex.domain.objective.color import Color
from cortex.domain.objective.objective import Objective
import re

from cortex.domain.objective.shape import Shape


class ObjectiveParser:
    def parse(self, objective_string: str) -> Objective:
        objective_string_content = objective_string.split('-')
        destination = self._get_destination(objective_string_content[2])
        shape, color = self._get_shape_or_color(objective_string_content[1])
        return Objective(destination, shape, color)

    def _get_destination(self, destination_string):
        return int(re.findall(r'\d+', destination_string)[0])

    def _get_shape_or_color(self, goal_string) -> [Shape, Color]:
        return Shape.get_from(goal_string), Color.get_from(goal_string)


if __name__ == "__main__":
    obj = ObjectiveParser()
    obj1 = obj.parse('14-orange-Zone3')
    print(obj1.color())
    print(obj1.destination())
    print(obj1.shape())
