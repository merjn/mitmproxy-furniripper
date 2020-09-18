from interceptors import FurnitureInterceptor
from handlers import FurniExistsHandler, GetFurniMetadataHandler, StoreFurnitureHandler, HotelAuthenticationHandler
from dispatcher import Dispatcher
from mitmproxy import ctx

# Kill noise by setting verbosity to 0 (flow_detail)
ctx.options.flow_detail = 0

furni_exists_handler = FurniExistsHandler()
furni_metadata_handler = GetFurniMetadataHandler()
hotel_authentication_handler = HotelAuthenticationHandler()
store_furni_handler = StoreFurnitureHandler()

furni_exists_handler.set_next(furni_metadata_handler)
furni_metadata_handler.set_next(hotel_authentication_handler)
hotel_authentication_handler.set_next(store_furni_handler)

listeners = [furni_exists_handler]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}

