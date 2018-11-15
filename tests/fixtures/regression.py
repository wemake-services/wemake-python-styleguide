class MqttListener:
    """MqttListener is a wrapper for (hb)mqtt connection."""

    def __init__(self, user: str, password: str, topic: str):
        """Init (hb)mqtt client."""
        self.mqtt_client = MQTTClient()
        self.user = user
        self.password = password
        self.topic = topic
