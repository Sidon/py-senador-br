from datetime import datetime
from urllib.request import urlopen
import xmltodict

from model import Session, Parlamentar, Mandato, Exercicio


class GetXMLandSave:

    __url_str = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
    __dict_data = xmltodict.parse(urlopen(__url_str).read())
    __fmt = '%Y-%m-%d'

    def __init__(self):
        self.__save_to_db()

    @property
    def get_url(self):
        return self.__url_str


    @property
    def get_data(self):
        return self.__dict_data


    def __save_to_db(self):

        def __save_exercicio(mdex, id_parlamentar, id_mandato):

            exercicio = Exercicio()

            exercicio.codigo = mdex['CodigoExercicio']
            exercicio.parlamentar_id = id_parlamentar
            exercicio.mandato_id = id_mandato
            exercicio.inicio = datetime.strptime(mdex['DataInicio'], self.__fmt)

            if 'DataFim' in mdex.keys():
                exercicio.fim = datetime.strptime(mdex['DataFim'], self.__fmt)
                exercicio.sigla_afastamento = mdex['SiglaCausaAfastamento']
                exercicio.causa_afastamento = mdex['DescricaoCausaAfastamento']

            session = Session()
            session.add(exercicio)
            session.commit()
            session.close()

        for p in self.__dict_data['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']:
            parlamentar = Parlamentar()
            id = p['IdentificacaoParlamentar']
            parlamentar.codigo = id['CodigoParlamentar']
            parlamentar.name = id['NomeParlamentar']
            parlamentar.fullname = id['NomeCompletoParlamentar']
            parlamentar.sexo = id['SexoParlamentar']
            parlamentar.tratamento = id['FormaTratamento']
            parlamentar.urlfoto = id['UrlFotoParlamentar']
            parlamentar.urlpagina = id['UrlPaginaParlamentar']
            parlamentar.email = id['EmailParlamentar']
            parlamentar.partido = id['SiglaPartidoParlamentar']
            parlamentar.uf = id['UfParlamentar']

            session = Session()
            session.add(parlamentar)
            session.commit()
            id_parlamentar = parlamentar.id
            session.close()

            mandato = Mandato()
            md = p['Mandato']
            md1 = md['PrimeiraLegislaturaDoMandato']
            md2 = md['SegundaLegislaturaDoMandato']
            mandato.codigo = md['CodigoMandato']
            mandato.uf = md['UfParlamentar']

            mandato.num_legis1 = md1['NumeroLegislatura']
            mandato.inicio_legis1 = datetime.strptime(md1['DataInicio'], self.__fmt)
            mandato.fim_legis1 = datetime.strptime(md1['DataFim'], self.__fmt)

            mandato.num_legis2 = md2['NumeroLegislatura']
            mandato.inicio_legis2 = datetime.strptime(md2['DataInicio'], self.__fmt)
            mandato.fim_legis2 = datetime.strptime(md2['DataFim'], self.__fmt)

            mds = md['Suplentes']
            for suplente in mds.keys():
                if type(mds[suplente]) == list:
                    mandato.nome_suplente1 = mds[suplente][0]['NomeParlamentar']
                    mandato.codigo_suplente1 = mds[suplente][0]['CodigoParlamentar']
                    mandato.participacao_suplente1 = mds[suplente][0]['DescricaoParticipacao']
                    mandato.nome_suplente2 = mds[suplente][1]['NomeParlamentar']
                    mandato.codigo_suplente2 = mds[suplente][1]['CodigoParlamentar']
                    mandato.participacao_suplente2 = mds[suplente][1]['DescricaoParticipacao']
                else:
                    mandato.nome_suplente1 = mds[suplente]['NomeParlamentar']
                    mandato.codigo_suplente1 = mds[suplente]['CodigoParlamentar']
                    mandato.participacao_suplente1 = mds[suplente]['DescricaoParticipacao']

            mandato.parlamentar_id = id_parlamentar

            session = Session()
            session.add(mandato)
            session.commit()
            id_mandato = mandato.id
            session.close()
            
            mde = md['Exercicios']
            for ex in mde.keys():
                if type(md['Exercicios'][ex]) != list:
                    __save_exercicio(md['Exercicios'][ex], id_parlamentar, id_mandato)
                else:
                    for e in md['Exercicios'][ex]:
                        __save_exercicio(e, id_parlamentar, id_mandato)


    def get_parlamentar(self, _name, scope=None):
        session = Session()
    
        if scope is None:
            parlamentar = session.query(Parlamentar).filter_by(name=_name)[0]
            mandato = session.query(Mandato).filter_by(parlamentar_id=parlamentar.id)[0]
            ex = session.query(Exercicio).filter_by(parlamentar_id=parlamentar.id)
            exercicios = [e for e in ex]
            dictp = dict(parlamentar = parlamentar, mandato = mandato, exercicios = exercicios)
        else:
            qry = session.query(Parlamentar).filter(Parlamentar.name.like('%'+_name+'%')).all()
            dictp=[]
            for p in qry:
                dict_temp = dict()
                dict_temp['parlamentar'] = p
                dict_temp['mandato'] =  session.query(Mandato).filter_by(parlamentar_id=p.id)
                dictp.append(dict_temp)

        return dictp