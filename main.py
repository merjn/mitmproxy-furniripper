from interceptors import FurnitureInterceptor
from handlers import FurniExistsHandler, GetFurniMetadataHandler
from dispatcher import Dispatcher
from mitmproxy import ctx

# Kill noise by setting verbosity to 0 (flow_detail)
ctx.options.flow_detail = 0

furni_exists_handler = FurniExistsHandler()
furni_metadata_handler = GetFurniMetadataHandler()

furni_exists_handler.set_next(furni_metadata_handler)

listeners = [furni_exists_handler]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}

