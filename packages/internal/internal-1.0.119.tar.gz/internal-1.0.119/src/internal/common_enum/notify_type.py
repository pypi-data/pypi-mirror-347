from enum import Enum


class NotifyTypeEnum(str, Enum):
    LINE = "line"
    SMS = "sms"
    APP = "app"
    NOTIFICATION = "notification"
    WEBSOCKET = "websocket"