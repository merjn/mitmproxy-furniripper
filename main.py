from mitmproxy import ctx

from addons import FurnitureInterceptor
from bootstrap import chain_handlers
from decorators import ConcurrentHandlerDecorator
from event import Dispatcher

ctx.options.flow_detail = 0

handler = ConcurrentHandlerDecorator(chain_handlers())

listeners = [handler]
dispatcher = Dispatcher(listeners)

addons = {
    FurnitureInterceptor(dispatcher)
}
