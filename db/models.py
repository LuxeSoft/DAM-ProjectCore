#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import datetime
import enum
import logging
import os

from _operator import and_
from builtins import getattr
from urllib.parse import urljoin

import falcon
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Unicode, \
    UnicodeText, Table, type_coerce, case, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_i18n import make_translatable

import messages
from db.json_model import JSONModel
import settings

mylogger = logging.getLogger(__name__)

SQLAlchemyBase = declarative_base()
make_translatable(options={"locales": settings.get_accepted_languages()})


def _generate_media_url(class_instance, class_attibute_name, default_image=False):
    class_base_url = urljoin(urljoin(urljoin("http://{}".format(settings.STATIC_HOSTNAME), settings.STATIC_URL),
                                     settings.MEDIA_PREFIX),
                             class_instance.__tablename__ + "/")
    class_attribute = getattr(class_instance, class_attibute_name)
    if class_attribute is not None:
        return urljoin(urljoin(urljoin(urljoin(class_base_url, class_attribute), str(class_instance.id) + "/"),
                               class_attibute_name + "/"), class_attribute)
    else:
        if default_image:
            return urljoin(urljoin(class_base_url, class_attibute_name + "/"), settings.DEFAULT_IMAGE_NAME)
        else:
            return class_attribute


def _generate_media_path(class_instance, class_attibute_name):
    class_path = "/{0}{1}{2}/{3}/{4}/".format(settings.STATIC_URL, settings.MEDIA_PREFIX, class_instance.__tablename__,
                                              str(class_instance.id), class_attibute_name)
    return class_path


class GenereEnum(enum.Enum):
    male = "M"
    female = "F"


class EventTypeEnum(enum.Enum):
    hackathon = "H"
    lanparty = "LP"
    livecoding = "LC"


class EventStatusEnum(enum.Enum):
    open = "O"
    closed = "C"
    ongoing = "G"
    undefined = "U"


class Imatge(SQLAlchemyBase, JSONModel):
    __tablename__ = "imatges"
    nom_imatge = Column(Unicode(200), primary_key=True, unique=True)
    imatge_nivell = Column(Unicode(200))
    nivell = Column(Integer)

    @hybrid_property
    def photo_url(self):
        return _generate_media_url(self, "photo")

    @hybrid_property
    def photo_path(self):
        return _generate_media_path(self, "photo")

class Partida(SQLAlchemyBase, JSONModel):
    __tablename__ = "partides"
    id_partida = Column(Integer, primary_key=True)
    username = Column(Unicode(200), nullable=False, unique=True)
    #username = Column(Integer, ForeignKey("players.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    temps = Column(Integer)
    guanyat = Column(Boolean)

    @hybrid_property
    def json_model(self):
            return {
                "id_partida": self.id_partida,
                "username": self.username,
                "temps": self.temps,
                "guanyat": self.guanyat,
            }

class Player(SQLAlchemyBase, JSONModel):
    __tablename__ = "players"
    username = Column(Unicode(200),primary_key=True, unique=True)
    #tokens = relationship("PlayeToken", back_populates="player", cascade="all, delete-orphan")
    password = Column(Unicode(200), nullable=False)
    pic_coins = Column(Integer, default=0)
    wins = Column(Integer, default = 0)
    xp = Column(Integer, default=0)


    @hybrid_property
    def json_model(self):
        return {
            "username": self.username,
            "password": self.password,
            "pic_coins": self.pic_coins,
            "wins": self.wins,
            "xp": self.xp,
        }

    @hybrid_property
    def public_profile(self):
        return {
            "username": self.username,
            "pic_coins": self.pic_coins,
            "wins": self.wins,
            "xp": self.xp
        }

class Card(SQLAlchemyBase, JSONModel):
    __tablename__ = "cards"
    letter = Column(Unicode(200),primary_key=True, unique=True)
    imatge_lletra = Column(Unicode(50))
    
#class posicio(SQLAlchemyBase, JSONModel):
#    __tablename__ = "posicio"
#    id_partida = Column(Integer,ForeignKey("partida.username"))
#    letter = Column(UnicodeText, ForeignKey("cards.letter"))
# FER COM EventParticipantsAssociation