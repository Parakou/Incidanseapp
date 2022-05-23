# coding: utf-8
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cour(Base):
    __tablename__ = 'Cours'

    Coursid = Column(Integer, primary_key=True)
    Cours_nom = Column(String(100), nullable=False)
    Cours_temps = Column(String(10))
    Cours_jours = Column(Enum('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'))


class Prof(Base):
    __tablename__ = 'Prof'

    Prof_id = Column(Integer, primary_key=True)
    Prof_nom = Column(String(45), nullable=False)
    Prof_prenom = Column(String(45), nullable=False)
    Prof_numcontact = Column(String(45))
    Prof_mail = Column(String(45))
    Prof_nom_prenom = Column(String(80))
    Prof_datenaissance = Column(Date)
    Prof_test = Column(Enum('1', '2'))


class Province(Base):
    __tablename__ = 'Province'

    Province_id = Column(Integer, primary_key=True)
    Province_nom = Column(String(45))


class Tarif(Base):
    __tablename__ = 'Tarif'

    id_Tarif = Column(Integer, primary_key=True)
    Tarif_nom = Column(String(45))
    Tarif_prix = Column(Integer)


class CoursProf(Base):
    __tablename__ = 'Cours_Prof'

    Cours_Prof_id = Column(Integer, primary_key=True)
    Prof_Prof_id = Column(ForeignKey('Prof.Prof_id'), nullable=False, index=True)
    Cours_Coursid = Column(ForeignKey('Cours.Coursid'), nullable=False, index=True)

    Cour = relationship('Cour')
    Prof_Prof = relationship('Prof')


class Ville(Base):
    __tablename__ = 'Ville'

    Ville_ID = Column(Integer, primary_key=True)
    Ville_nom = Column(String(45, 'utf8mb4_unicode_520_ci'))
    Ville_CP = Column(Integer)
    Province_Province_id = Column(ForeignKey('Province.Province_id'), nullable=False, index=True)
    Province_Province = relationship('Province')


class Eleve(Base):
    __tablename__ = 'Eleve'

    eleve_id = Column(Integer, primary_key=True)
    eleve_prenom = Column(String(45), nullable=False)
    eleve_nom = Column(String(45), nullable=False)
    eleve_datenaissance = Column(Date)
    eleve_age = Column(Integer)
    eleve_adresse = Column(String(100))
    eleve_GSM = Column(String(45))
    eleve_fixe = Column(String(45))
    eleve_mail = Column(String(45))
    eleve_mail2 = Column(String(45))
    eleve_heure = Column(String(45))
    eleve_freresoeur = Column(Enum('1', '0'), server_default=text("'0'"))
    eleve_medic = Column(String(100))
    eleve_courst = Column(String(45))
    eleve_actif = Column(Enum('1', '0'), server_default=text("'1'"))
    Ville_id_Ville = Column(ForeignKey('Ville.Ville_ID'), nullable=False, index=True)
    eleve_nom_prenom = Column(String(100))

    Ville = relationship('Ville')


class EleveCour(Base):
    __tablename__ = 'eleve_Cours'

    eleve_Coursid = Column(Integer, primary_key=True)
    eleve_eleve_id = Column(ForeignKey('Eleve.eleve_id'), nullable=False, index=True)
    Cours_Coursid = Column(ForeignKey('Cours.Coursid'), nullable=False, index=True)

    Cour = relationship('Cour')
    eleve_eleve = relationship('Eleve')


class EleveTarif(Base):
    __tablename__ = 'eleve_Tarif'

    eleve_tarif_id = Column(Integer, primary_key=True)
    eleve_eleve_id = Column(ForeignKey('Eleve.eleve_id'), nullable=False, index=True)
    Tarif_id_Tarif = Column(ForeignKey('Tarif.id_Tarif'), nullable=False, index=True)
    Eleve_Tarif_Date = Column(Date)
    eleve_Tarif_Montant = Column(Integer)

    Tarif = relationship('Tarif')
    eleve_eleve = relationship('Eleve')
