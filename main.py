from mitmproxy import ctx

from addons import FurnitureInterceptor
from decorators import ConcurrentHandlerDecorator
from event import Dispatcher
from handlers import FurniExistsHandler, FurniIconHandler, FurniMetadataHandler, PushFurniToApiHandler

furni_exists_handler = FurniExistsHandler()
furniture_icon_handler = FurniIconHandler()
furni_metadata_handler = FurniMetadataHandler()
push_furni_to_api_handler = PushFurniToApiHandler()

furni_exists_handler.set_next(furniture_icon_handler)
furniture_icon_handler.set_next(furni_metadata_handler)
furni_metadata_handler.set_next(push_furni_to_api_handler)

ctx.options.flow_detail = 0

h = furni_exists_handler

listeners = [h]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}

