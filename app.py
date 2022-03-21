#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging.config

import falcon

import messages
import middlewares
from falcon_multipart.middleware import MultipartMiddleware
from resources import common_resources, partida_resource
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
application.add_route("/", common_resources.ResourceHome())

#application.add_route("/account/profile", account_resources.ResourceAccountUserProfile())
#application.add_route("/account/profile/update_profile_image", account_resources.ResourceAccountUpdateProfileImage())
#application.add_route("/account/create_token", account_resources.ResourceCreateUserToken())
#application.add_route("/account/delete_token", account_resources.ResourceDeleteUserToken())

#application.add_route("/users/register", user_resources.ResourceRegisterUser())
#application.add_route("/users/show/{username}", user_resources.ResourceGetUserProfile())

'start peticions noves...'

application.add_route("/partida",partida_resource.ResourceGetPartida())
application.add_route("/player",partida_resource.ResourceGetPlayer())


'end peticions noves'

application.add_sink(handle_404, "")
