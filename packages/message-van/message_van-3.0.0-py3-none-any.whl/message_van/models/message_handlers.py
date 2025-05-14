from collections import defaultdict

from message_van.exceptions import UnknownHandlerError
from message_van.models import (
    Command,
    CommandHandler,
    Event,
    EventHandler,
    MessageHandlerSignature,
    MessageHandlerType,
    Message,
)


class MessageHandlers:
    _command_handlers: dict[str, CommandHandler]
    _event_handlers: dict[str, list[EventHandler]]

    def __init__(self):
        self._command_handlers = {}
        self._event_handlers = defaultdict(list)

    def get_handler_for_command(self, command: Command) -> CommandHandler:
        command_name = _get_message_name(command)

        return self._get_handler_for_command(command_name)

    def _get_handler_for_command(self, command_name: str) -> CommandHandler:
        try:
            return self._command_handlers[command_name]
        except KeyError:
            raise UnknownHandlerError(command_name)

    def get_handlers_for_event(self, event: Event) -> list[EventHandler]:
        event_name = _get_message_name(event)

        name_handlers = self._get_handlers_by_name(event_name)
        base_handlers = self._get_handlers_by_base_classes(event)

        return name_handlers + base_handlers

    def _get_handlers_by_name(self, event_name: str) -> list[EventHandler]:
        return self._event_handlers[event_name]

    def _get_handlers_by_base_classes(
        self, event: Event
    ) -> list[EventHandler]:
        handlers = []
        base_class_names = get_base_class_names(event)

        for base_class_name in base_class_names:
            handlers.extend(self._event_handlers[base_class_name])

        return handlers

    def register(self, signature: MessageHandlerSignature) -> None:
        type_ = signature.type
        class_name = signature.message_class_name
        handler = signature.message_handler

        if type_ == MessageHandlerType.COMMAND:
            self._register_command(class_name, handler)
        else:
            self._register_event(class_name, handler)

    def _register_command(
        self,
        class_name: str,
        handler: CommandHandler,
    ) -> None:
        self._command_handlers[class_name] = handler

    def _register_event(self, class_name: str, handler: EventHandler) -> None:
        self._event_handlers[class_name].append(handler)

    @property
    def __bool__(self) -> None:
        if self._command_handlers:
            return True
        if len(self._event_handlers) > 0:
            return True

        return False


def _get_message_name(message: Message) -> str:
    message_class = message.__class__

    return message_class.__name__


def get_base_class_names(message: Message) -> set[str]:
    bases = set()

    def _get_bases(c):
        for base in c.__bases__:
            if base not in bases:
                bases.add(base.__name__)
                _get_bases(base)

    _get_bases(message.__class__)

    return bases
