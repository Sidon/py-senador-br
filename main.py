from popula_db import GetXMLandSave
from datetime import datetime as dt
from tabulate import tabulate

gxml  = GetXMLandSave()

print ('# Busca pelo nome exato')
print ('-----------------------')

nome = input ('Entre com o nome: ')
pl = gxml.get_parlamentar(nome)

headers = ['Full Namme', 'UF', 'Incio']
prl = [pl['parlamentar'].fullname, pl['mandato'].uf, dt.date(pl['mandato'].inicio_legis1)]
print (tabulate([prl], tablefmt="fancy_grid", headers=headers))


print ('\n# Busca no estilo like')
print ('----------------------')

nome = input ('Entre com o nome: ')
pl = gxml.get_parlamentar(nome, 'like')


prl = []
#print (len(pl))
for p in pl:
    #print (p['parlamentar'].fullnamep)
    list_temp = []
    list_temp.append(p['parlamentar'].fullname)
    list_temp.append(p['mandato'][0].uf)
    list_temp.append(dt.date(p['mandato'][0].inicio_legis1))
    prl.append(list_temp)

print (tabulate(prl, tablefmt="fancy_grid", headers=headers))






