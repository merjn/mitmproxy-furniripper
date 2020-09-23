from interceptors import FurnitureInterceptor
from handlers import FurniExistsHandler
from handlers import GetFurniMetadataHandler
from handlers import StoreFurnitureHandler
from handlers import GetFurnitureIconHandler
from handlers import HotelAuthenticationHandler
from decorators import ConcurrentHandlerDecorator
from dispatcher import Dispatcher
from mitmproxy import ctx
from requests import Session


# Kill noise by setting verbosity to 0 (flow_detail)
ctx.options.flow_detail = 0

furni_exists_handler = FurniExistsHandler()
furni_metadata_handler = GetFurniMetadataHandler()

session = Session()

hotel_authentication_handler = HotelAuthenticationHandler(session)
store_furni_handler = StoreFurnitureHandler(session)
furniture_icon_handler = GetFurnitureIconHandler()

furni_exists_handler.set_next(furni_metadata_handler)
furni_metadata_handler.set_next(furniture_icon_handler)

furniture_icon_handler.set_next(hotel_authentication_handler)

hotel_authentication_handler.set_next(store_furni_handler)

listeners = [ConcurrentHandlerDecorator(furni_exists_handler)]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}

