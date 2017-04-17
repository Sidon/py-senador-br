import unittest
from popula_db import GetXMLandSave


FACM = ('4525', 'Fernando Affonso Collor de Mello')
LLFF = ('3695', 'Luiz Lindbergh Farias Filho')
RRMS = ('72','Roberto Requião de Mello e Silva')
gxml  = GetXMLandSave()

class Test_Get(unittest.TestCase):

    def test_collor(self):
        pl = gxml.get_parlamentar('Fernando Collor')
        self.assertEqual((pl['parlamentar'].codigo,pl['parlamentar'].fullname), FACM )

    def test_lindbergh(self):
        pl = gxml.get_parlamentar('Lindbergh Farias')
        self.assertEqual((pl['parlamentar'].codigo,pl['parlamentar'].fullname), LLFF )


    def test_requiao(self):
        pl = gxml.get_parlamentar('Roberto Requião')
        self.assertEqual((pl['parlamentar'].codigo,pl['parlamentar'].fullname), RRMS )


unittest.main()