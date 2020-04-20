if __name__ == "__main__":
    from events.Event import Event
    from events.EventDispatcher import EventDispatcher
    from events.EventListener import EventListener

    EventDispatcher.setup() \
                    .addListener(EventListener(), "test_type")
    EventDispatcher.instance.dispatchEvent(Event("test_type"))
