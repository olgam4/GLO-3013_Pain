from unittest import TestCase

from communication.service.message import Message


class TestMessage(TestCase):
    def setUp(self) -> None:
        self.message = Message("test_message", variable1="variable1")

    def test_when_deserializing_then_message_is_equivalent(self) -> None:
        original_data = self.message.serialize()

        deserialized_message = Message.deserialize(original_data)

        self.assertEqual(self.message, deserialized_message)
