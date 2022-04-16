from email.mime import image
import falcon
from sqlalchemy.orm.exc import NoResultFound
from resources import utils
import messages
from db.models import Imatge
from resources.base_resources import DAMCoreResource
from sqlalchemy.exc import IntegrityError

class ResourceGetImageByName(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetImageByName, self).on_get(req,resp, *args,**kwargs)

        if "nom_imatge" in kwargs:
            try:
                aux_user = self.db_session.query(Imatge).filter(Imatge.username == kwargs["nom_imatge"]).one()

                resp.media = aux_user.public_profile
                resp.status = falcon.HTTP_200
            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found)
            
        else:    
            raise falcon.HTTPMissingParam("nom_imatge")

class ResourceAddImage(DAMCoreResource): #guarda imatge
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourceAddImage, self).on_post(req, resp, *args, **kwargs)

        #ruta imatge
        image = Imatge()
        resource_path = image.photo_path

        #recuperar imatge
        incoming_file = req.get_param("image_file")
        name_file = req.get_param("name_file")
        nivell = req.get_param("nivell")

        # Run the common part for storing
        filename = utils.save_static_media_file(incoming_file, resource_path)
        image.nom_imatge = name_file  #nom q li passo x parametre al metode de adalt
        image.nivell = nivell
        
        # Update db model
        image.imatge_nivell = filename
        self.db_session.add(image)
        self.db_session.commit()

        resp.status = falcon.HTTP_200

 