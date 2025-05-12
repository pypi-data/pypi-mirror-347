import asyncio
from typing import Callable, Any, Dict, Coroutine

class NoHandlerRegisteredError(Exception):
    """
    Exception raised when no handler is registered for a specific topic,
    or if no handler is registered at all.
    """
    def __init__(self, topic: str = None):
        if topic:
            super().__init__(f"No handler registered for topic: '{topic}'. "
                             f"Use @qtask.handler('{topic}') to decorate your processing function.")
        else:
            super().__init__("No message handler registered. "
                             "Use @qtask.handler('topic_name') to decorate your processing function.")
        self.topic = topic

class QTask:
    """
    Manager for registering and obtaining message handlers based on topics
    for task processing.
    """
    def __init__(self):
        # The registration now is a dictionary: {str_topic: handler_function}
        self._topic_handlers: Dict[str, Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]] = {}
        print("QTASK: QTask manager initialized. Ready to register topic-specific handlers.")

    def handler(self, topic: str):
        """
        Decorator to register a function as the handler for a specific topic.
        The decorated function must be a coroutine (async def) and accept
        a dictionary (the deserialized message payload).

        Example of use:
            from qtask import qtask # Assuming that qtask is the package name

            @qtask.handler("EMAIL")
            async def mi_procesador_de_emails(payload: dict):
                # ... processing logic for email ...
                return {"resultado_email": "ok"}
        """
        if not isinstance(topic, str) or not topic.strip(): # Ensure that the topic is not only spaces
            raise ValueError("The topic for the handler must be a non-empty and meaningful string.")

        # The actual decorator that takes the function
        def decorator(func: Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(
                    f"The handler for topic '{topic}' ({func.__name__}) must be a coroutine (async def)."
                )
            
            # Check if a handler already exists for this topic and warn/error if it is redefined
            if topic in self._topic_handlers:
                # You can decide if this is an error or a warning.
                # For now, it is a warning and overwrites.
                print(f"QTASK WARNING: Overwriting previously registered handler "
                      f"for topic '{topic}' ('{self._topic_handlers[topic].__name__}') "
                      f"with a new handler ('{func.__name__}').")

            print(f"QTASK: Registering handler '{func.__name__}' for topic: '{topic}'")
            self._topic_handlers[topic] = func
            return func # Return the original function so that the decorator works
        return decorator

    def get_message_handler(self, topic: str) -> Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]:
        """
        Returns the message handler registered for a specific topic.
        Raises NoHandlerRegisteredError if no handler is registered for that topic.
        """
        if not isinstance(topic, str):
            # This could happen if the 'topic' field in the message is not a string
            raise TypeError(f"The topic searched must be a string, received: {type(topic)} ('{topic}')")

        handler_func = self._topic_handlers.get(topic)
        if handler_func is None:
            raise NoHandlerRegisteredError(topic=topic)
        return handler_func

    def is_any_handler_registered(self) -> bool:
        """Checks if at least one handler has been registered in the system."""
        return bool(self._topic_handlers)

# Create a global instance so that users can use:
# from qtask import qtask  (if your package is called qtask)
# and then:
# @qtask.handler("topic_name")
qtask = QTask()