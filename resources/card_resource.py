from email.mime import image
import falcon
from sqlalchemy.orm.exc import NoResultFound
from resources import utils
import messages
from db.models import Card
from resources.base_resources import DAMCoreResource
from sqlalchemy.exc import IntegrityError

class ResourceCardByName(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceCardByName, self).on_get(req,resp, *args,**kwargs)

        if "letter" in kwargs:
            try:
                aux_letter = self.db_session.query(Card).filter(Card.letter == kwargs["letter"]).one()

                resp.media = aux_letter.public_profile
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description="letter not found")
            
        else:    
            raise falcon.HTTPMissingParam("letter")


class ResourceCard(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceCard, self).on_get(req,resp, *args,**kwargs)

        try:
            aux_letter = self.db_session.query(Card).filter(Card.letter == "a").one()

            resp.media = aux_letter.public_profile
            resp.status = falcon.HTTP_200
        except NoResultFound:
            raise falcon.HTTPBadRequest(description="letter not found")
    

class ResourceAddImageCard(DAMCoreResource): #guarda imatge
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceAddImageCard, self).on_post(req, resp, *args, **kwargs)

        #ruta imatge
        card = Card()
        resource_path = card.photo_path

        #recuperar imatge
        incoming_file = req.get_param("image_file")
        name_file = req.get_param("name_file")


        # Run the common part for storing
        filename = utils.save_static_media_file(incoming_file, resource_path)
        card.letter = name_file #letter q li passo x parametre al metode de adalt

        # Update db model
        card.imatge_lletra = filename
        self.db_session.add(card)
        self.db_session.commit()

        resp.status = falcon.HTTP_200

 