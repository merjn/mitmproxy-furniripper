from requests import Session

from handlers import AbstractHandler, FurniExistsHandler, FurniMetadataHandler, HotelAuthenticationHandler, \
    StoreFurnitureHandler, FurniIconHandler

# Just treat session as a singleton.
session = Session()


def chain_handlers() -> AbstractHandler:
    """
    Chains the handlers in the 'handlers' directory.
    :return: the first handler in the chain.
    """
    furni_exists_handler = FurniExistsHandler()
    furni_metadata_handler = FurniMetadataHandler()

    hotel_authentication_handler = HotelAuthenticationHandler(session)
    store_furni_handler = StoreFurnitureHandler(session)
    furniture_icon_handler = FurniIconHandler()

    furni_exists_handler.set_next(furni_metadata_handler)
    furni_metadata_handler.set_next(furniture_icon_handler)

    furniture_icon_handler.set_next(hotel_authentication_handler)

    hotel_authentication_handler.set_next(store_furni_handler)

    return furni_exists_handler
