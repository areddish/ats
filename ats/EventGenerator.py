class EventGenerator:
    def __init__(self):
        self.events = {}

    def subscribe(self, eventName, callback):
        event_listeners = self.events.get(eventName, [])
        event_listeners.append(callback)
        self.events[eventName] = event_listeners

    def unsubscribe(self, eventName, callback):
        event_listeners = self.events.get(eventName, [])
        listener_count = len(event_listeners)
        event_listeners.remove(callback)
        if len(event_listeners) == listener_count:
            raise KeyError #, f"Coudln't remove {eventName}"

    def raise_event(self, eventName, data):
        event_listeners = self.events.get(eventName, [])
        for cb in event_listeners:
            event_listeners[cb](data)
