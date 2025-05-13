from enum import Enum


# 討論是否廢
class NotifyTypeEnum(str, Enum):
    APP = "app"
    LINE = "line"
    SMS = "sms"
    NOTIFICATION = "notification"
    WEBSOCKET = "websocket"
