#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging.config

import falcon

import messages
import middlewares
from falcon_multipart.middleware import MultipartMiddleware
from resources import imatge_resource, partida_resource, player_resource, card_resource
from settings import configure_logging

# LOGGING
mylogger = logging.getLogger(__name__)
configure_logging()


# DEFAULT 404
# noinspection PyUnusedLocal
def handle_404(req, resp):
    resp.media = messages.resource_not_found
    resp.status = falcon.HTTP_404


# FALCON
app = application = falcon.API(
    middleware=[
        middlewares.DBSessionManager(),
        middlewares.Falconi18n(),
        MultipartMiddleware()
    ]
)
#application.add_route("/", common_resources.ResourceHome())

'start peticions noves...'

application.add_route("/partida",partida_resource.ResourceGetPartida())
application.add_route("/partida",partida_resource.ResourceGetPartidaById)
application.add_route("/partida",partida_resource.ResourceSavePartida())

application.add_route("/player",player_resource.ResourceGetAllPlayers())
application.add_route("/player/show/{username}", player_resource.ResourceGetPlayer())
application.add_route("/player/add", player_resource.ResourceRegisterPlayer())

application.add_route("/imatges/show/nivell/{nivell}", imatge_resource.ResourceGetImageByLevel())
application.add_route("/imatges/show/{nom_imatge}", imatge_resource.ResourceGetImageByName())
application.add_route("/imatges/add", imatge_resource.ResourceAddImage())

application.add_route("/cards/show/{letter}", card_resource.ResourceCardByName())
application.add_route("/cards/add", card_resource.ResourceAddImageCard())


'end peticions noves'

application.add_sink(handle_404, "")
