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


class ResourceGetListCards(DAMCoreResource):
    def on_get(self,req,resp,*args,**kwargs):
        super(ResourceGetListCards, self).on_get(req,resp, *args,**kwargs)

        if "imatge" in kwargs:

            try:
                valor_img = kwargs["imatge"]
                list_letters = list(valor_img)

                print(list_letters) 

                array_lletres = []

                for letter in list_letters:
                    aux_letter = self.db_session.query(Card).filter(Card.letter == letter).one()
                    array_lletres.append(aux_letter.public_profile)
                    
                
                array_lletres_static = ["r","w","x","m"]
                #dicciinari amb lletres abc, fer random, random entre 0 i llargadamax
                #TODO


                x = 0

                for i in range(len(array_lletres),8): 
                    print(i)
                    aux_letter = self.db_session.query(Card).filter(Card.letter == array_lletres_static[x]).one()
                    array_lletres.append(aux_letter.public_profile)
                    x = x+1


                #aux_letter = self.db_session.query(Card).filter(Card.letter == kwargs["letter"]).one()
                #resp.media = aux_letter.public_profile
                
                print(array_lletres)
                resp.media = array_lletres
                
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

 