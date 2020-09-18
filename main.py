from interceptors import FurnitureInterceptor
from handlers import CheckIfFurniExists
from dispatcher import Dispatcher
from mitmproxy import ctx

# Kill noise by setting verbosity to 0 (flow_detail)
ctx.options.flow_detail = 0

listeners = [CheckIfFurniExists()]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}

