from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
import os

# Variaveis para conexão ao BD em disco
__BASE_DIR = os.path.dirname(__file__)
__BASE_DB = 'sqlite:///' + __BASE_DIR
__BASE_DB = 'sqlite:///' + __BASE_DIR
__FILE_MEMO = 'sqlite://'
__file = os.path.join(__BASE_DB, 'senadobr.sqlite3')

# BD em memoria (SQLite), comente para gravação em disco
__file = __FILE_MEMO


__engine = create_engine(__file, echo=False)
Session = sessionmaker(bind=__engine)
__session = Session
__Base = declarative_base(__engine)


class Parlamentar(__Base):
    __tablename__ = 'parlamentar'
    id = Column(Integer, primary_key=True)
    name = Column(String(70))
    codigo = Column(String(4))
    fullname = Column(String(70))
    sexo = Column(String(1))
    tratamento = Column(String(5))
    urlfoto = Column(String(255))
    urlpagina = Column(String(255))
    email = Column(String(255))
    partido = Column(String(6))
    uf = Column(String(2))

    def __repr__(self):
        return self.fullname


class Mandato(__Base):
    __tablename__ = 'mandato'
    id = Column(Integer, primary_key=True)
    parlamentar_id = Column(Integer, ForeignKey('parlamentar.id'))
    codigo = Column(String(3))
    uf = Column(String(2))
    num_legis1 = Column(String(5))
    inicio_legis1 = Column(DateTime)
    fim_legis1 = Column(DateTime)
    num_legis2 = Column(String(5))
    inicio_legis2 = Column(DateTime)
    fim_legis2 = Column(DateTime)
    desc_participacao = Column(String(30))
    nome_suplente1 = Column(String(70))
    codigo_suplente1 = Column(String(6))
    participacao_suplente1 = Column(String(20))
    nome_suplente2 = Column(String(70))
    codigo_suplente2 = Column(String(6))
    participacao_suplente2 = Column(String(20))



class Exercicio(__Base):
    __tablename__ = 'exercicio'
    id = Column(Integer, primary_key=True)
    parlamentar_id = Column(Integer, ForeignKey('parlamentar.id'))
    mandato_id = Column(Integer, ForeignKey('mandato.id'))
    codigo = Column(String(6))
    inicio = Column(DateTime)
    fim = Column(DateTime)
    sigla_afastamento = Column(String(6))
    causa_afastamento = Column(String(255))


# Criação das tabelas
if os.path.isfile(__BASE_DIR+'/senadobr.sqlite3'):
    os.remove(__BASE_DIR+'/senadobr.sqlite3')

__Base.metadata.create_all()