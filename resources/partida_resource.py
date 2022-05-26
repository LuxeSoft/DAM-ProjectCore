import falcon
from sqlalchemy.orm.exc import NoResultFound

import messages
from db.models import Partida
from resources.base_resources import DAMCoreResource
from sqlalchemy.exc import IntegrityError



class ResourceGetPartida(DAMCoreResource): #ok
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetPartida, self).on_get(req,resp, *args,**kwargs)

        response_partida = list()
    
        aux_events = self.db_session.query(Partida)

        if aux_events is not None:
            for current_event in aux_events.all():
                response_partida.append(current_event.json_model)
        
        resp.media = response_partida
        resp.status = falcon.HTTP_200

class ResourceSavePartida(DAMCoreResource):
    #@jsonschema.validate(SchemaRegisterUser)
    '''
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceSavePartida, self).on_post(req, resp, *args, **kwargs)
        aux_partida = Partida()

        try:

            aux_partida.username = req.media["username"]
            aux_partida.temps = req.media["temps"]
            aux_partida.guanyat = req.media["guanyat"]

            self.db_session.add(aux_partida)

            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest(description=messages.error_partida_ex)

        except KeyError:
            raise falcon.HTTPBadRequest(description=messages.parameters_invalid)

        resp.status = falcon.HTTP_200

class ResourceGetPartidaById(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceGetPartidaById, self).on_get(req, resp, *args, **kwargs)

        if "id" in kwargs:
            try:
                response_event = self.db_session.query(Partida).filter(Partida.id == kwargs["id"]).one()

                resp.media = response_event.json_model
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.error_partida_no_ex)
        else:
            raise falcon.HTTPMissingParam("id")
'''
