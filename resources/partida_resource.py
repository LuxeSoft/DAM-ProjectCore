import falcon
from sqlalchemy.orm.exc import NoResultFound

import messages
from db.models import Partida, Player
from resources.base_resources import DAMCoreResource


class ResourceGetPartida(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetPartida, self).on_get(req,resp, *args,**kwargs)

        response_partida = list()

        if "username" in kwargs:
            try:
                aux_user = self.db_session.query(Player).filter(Player.username == kwargs["username"]).one()

                resp.media = aux_user.public_profile
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found)
            
        else:    
            aux_events = self.db_session.query(Partida)

            if aux_events is not None:
                for current_event in aux_events.all():
                    response_partida.append(current_event.json_model)
            
            resp.media = response_partida
            resp.status = falcon.HTTP_200
    