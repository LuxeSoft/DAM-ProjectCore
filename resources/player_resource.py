import falcon
from sqlalchemy.orm.exc import NoResultFound

import messages
from db.models import Partida, Player
from resources.base_resources import DAMCoreResource
from sqlalchemy.exc import IntegrityError

class ResourceGetPlayer(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetPlayer, self).on_get(req,resp, *args,**kwargs)

        if "username" in kwargs:
            try:
                aux_user = self.db_session.query(Player).filter(Player.username == kwargs["username"]).one()

                resp.media = aux_user.public_profile
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found)
            
        else:    
            raise falcon.HTTPMissingParam("username")



class ResourceRegisterPlayer(DAMCoreResource):
    #@jsonschema.validate(SchemaRegisterUser)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceRegisterPlayer, self).on_post(req, resp, *args, **kwargs)
        aux_player = Player()

        try:
            aux_player.username = req.media["username"]
            aux_player.password = req.media["password"]
            aux_player.pic_coins = req.media["pic_coins"]
            aux_player.wins = req.media["wins"]
            aux_player.xp = req.media["xp"]

            self.db_session.add(aux_player)

            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest(description=messages.user_exists)

        except KeyError:
            raise falcon.HTTPBadRequest(description=messages.parameters_invalid)

        resp.status = falcon.HTTP_200

class ResourceGetAllPlayers(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetAllPlayers, self).on_get(req,resp, *args,**kwargs)

        response_player = list()

        aux_events = self.db_session.query(Player)

        if aux_events is not None:
            for current_event in aux_events.all():
                print("Insert for")
                response_player.append(current_event.json_model)
        
        resp.media = response_player
        resp.status = falcon.HTTP_200