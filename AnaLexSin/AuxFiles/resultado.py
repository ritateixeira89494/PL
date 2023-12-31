import re
from AnaLexSin.AuxFiles.auxfunctions import getImut
import AnaLexSin.AuxFiles.liststructs as ls

class Resultado:

    def __init__(self, ret, valorRet, pv):
        self.struct = (ret, valorRet, pv)

    def toPython(self, numtabs=2):
        flattened = []
        for item in self.struct[1]:
            if isinstance(item, list):
                flattened.extend(Resultado(None, item, None).toPython(0)[7:])
            elif isinstance(item, ls.ListVar) or isinstance(item,ls.ListStatic):
                flattened.append(item.toPythonRes())
            else:
                flattened.append(item)
        res = ""
        # print("FLATTENED: "+str(flattened)) tirar de comentário para debug
        for elem in flattened:
            m = re.match("-\['(.*)']", elem)
            if m != None:
                elem = '-' + m.group(1)
            res = res + elem
        t = '\t' * numtabs
        return t + 'return ' + res
    def __str__(self):
        return self.toPython()
