from ply.lex import lex
import re

tokens = (
    'ADD',          # +
    'MINUS',        # -
    'TIMES',        # *
    'DIVIDE',       # /
    'MOD',          # %
    'OR',           # |
    'AND',          # &
    'NUMBER',       # INT FLOAT
    'BOOL',         # true false
    'LIST',         # [(...)] 
    'FUNABRE',      # deff
    'FUNFECHA',     # end
    'ABREP',        # (
    'FECHAP',       # )
    'VIR',          # , -> argumentos
    'VAR',          # palavra
    'IF',           # if
    'THEN',         # then
    'ELSE',         # else
    'CHAMADAFUN',   # palavra(
    'ABREFP',       # """FPYTHON
    'FECHAFP',      # """
    'MENOR',        # <
    'MAIOR',        # > 
    'IGUAL',        # ==
    'DIFERENTE',    # != 
    'MAIORIGUAL',   # >=
    'MENORIGUAL',   # <=
    'IN',           # in
    'NOT',          # not
    'CONDAND',      # and
    'CONDOR',       # or
    'RETURN',       # return
    'ABREL',        # [
    'FECHAL'        # ]
)

states = (
    ('FPYTHON','inclusive'),
    ('CORPOFUN','inclusive'),
    ('ARGSFUN','inclusive'),
    ('IFTHENELSE','inclusive'),
    ('COND','inclusive'),
    ('INVOCACAOFUN','inclusive'),
    ('RETURNFUN','inclusive'),
    ('LISTSTATE','inclusive')
)

t_VIR = r','

def t_RETURNFUN_INVOCACAOFUN_COND_ADD(t):
    r'\+'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\+\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_MINUS(t):
    r'\-'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\-\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_OR(t):
    r'\|'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\|\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_AND(t):
    r'&'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*&\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_DIVIDE(t):
    r'\/'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\/\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_TIMES(t):
    r'\*'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\*\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_RETURNFUN_INVOCACAOFUN_COND_MOD(t):
    r'%'
    # r'(\w+|(\+|\-)?\d+(\.d+)?)\s*\%\s*(\w+|(\+|\-)?\d+(\.d+)?)'
    print(t.value)
    return t

def t_INITIAL_ABREFP(t):
    r'"""(?i:FPYTHON)'
    t.lexer.begin('FPYTHON')
    print('INICIALIZA FPYTHON')
    return t

def t_FPYTHON_FECHAFP(t):
    r'"""'
    t.lexer.begin('INITIAL')
    print('Acaba FPYTHON')
    return t

def t_FPYTHON_FUNABRE(t):
    r'deff\s+[A-Za-z]\w+\s*\('
    t.lexer.begin('ARGSFUN')
    print('Nome funcão: ' + re.search('deff\s+(\w+)',t.value).group(1))
    return t

def t_ARGSFUN_BOOL(t):
    r'(true|false)'
    print('Argumento booleano ' + re.search('\w+',t.value).group())
    return t


def t_ARGSFUN_NUMBER(t):
    r'\d+(\.d+)?'
    print('Argumento número ' + re.search('((\+|\-)?\d+(\.d+)?)',t.value).group())
    return t

def t_ARGSFUN_VAR(t):
    r'\w+'
    print('Argumento ' + re.search('\w+',t.value).group())
    return t

def t_ARGSFUN_LIST(t):
    r'(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])'
    print('Argumento lista ' + re.search('(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])',t.value).group())
    return t

def t_ARGSFUN_ABREL(t):
    r'\['
    t.lexer.begin('LISTSTATE')
    t.lexer.stack.append('ARGSFUN')
    print(f'Stack atual: {t.lexer.stack}')
    print('Argumento Lista')
    return t

def t_ARGSFUN_FECHAP(t):
    r'\)'
    t.lexer.begin('CORPOFUN')
    print('comeca corpo fun')
    return t

def t_RETURNFUN_FUNFECHA(t):
    r'end'
    state = 'FPYTHON'
    if len(t.lexer.stack) > 0:
        state = t.lexer.stack.pop()
    print('fecha funcão ' + state)
    print(f'Stack atual: {t.lexer.stack}')
    if state == 'FPYTHON':
        print('========================')
    t.lexer.begin(state)
    return t

def t_CORPOFUN_IF(t):
    r'if\s*\('
    print('Inicializa if')
    t.lexer.begin('COND')
    return t

def t_COND_RETURNFUN_MENOR(t):
    r'<'
    print('menor')
    return t

def t_COND_RETURNFUN_MAIOR(t):
    r'>'
    print('maior')
    return t

def t_COND_RETURNFUN_MENORIGUAL(t):
    r'<='
    print('menor igual')
    return t

def t_COND_RETURNFUN_MAIORIGUAL(t):
    r'>='
    print('maior igual')
    return t

def t_COND_RETURNFUN_IGUAL(t):
    r'=='
    print('igual')
    return t

def t_COND_RETURNFUN_IN(t):
    r'in'
    print('in')
    return t

def t_COND_RETURNFUN_NOT(t):
    r'not'
    print('not')
    return t

def t_COND_RETURNFUN_DIFERENTE(t):
    r'!='
    print('diferente')
    return t

def t_COND_RETURNFUN_AND(t):
    r'and'
    print('and')
    return t

def t_COND_RETURNFUN_OR(t):
    r'or'
    print('or')
    return t

def t_COND_NUMBER(t):
    r'\d+(\.d+)?'
    print('cond number')
    return t

def t_COND_BOOL(t):
    r'(true|false)'
    print('bool cond')
    return t

def t_COND_LIST(t):
    r'(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])'
    print('condicao lista')
    return t

def t_COND_CHAMADAFUN(t):
    r'\w+\('
    print('Chamada função ' + re.match('(\w+)',t.value).group(1))
    t.lexer.begin('INVOCACAOFUN')
    t.lexer.stack.append('COND')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_COND_VAR(t):
    r'\w+'
    print('Condicao variável ' + re.match(r'(\w+)',t.value).group(1))
    return t

def t_COND_FECHAP(t):
    r'\)'
    t.lexer.begin('IFTHENELSE')
    print('Acaba condição')
    return t

def t_COND_ABREP(t):
    r'\('
    print('Condição aninhada')
    t.lexer.stack.append('COND')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_COND_ABREL(t):
    r'\['
    t.lexer.begin('LISTSTATE')
    t.lexer.stack.append('COND')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_IFTHENELSE_THEN(t):
    r'then'
    print('then')
    t.lexer.stack.append('IFTHENELSE')
    print(f'Stack atual: {t.lexer.stack}')
    t.lexer.begin('CORPOFUN')
    return t

def t_IFTHENELSE_ELSE(t):
    r'else'
    print('else')
    t.lexer.begin('CORPOFUN')
    return t

def t_CORPOFUN_RETURN(t):
    r'return'
    print('Entrou estado return')
    t.lexer.begin('RETURNFUN')
    return t

def t_INVOCACAOFUN_NUMBER(t):
    r'\d+(\.d+)?'
    print('Invocacação fun número')
    return t

def t_INVOCACAOFUN_CHAMADAFUN(t):
    r'\w+\('
    print('Chamada função ' + re.match('(\w+)',t.value).group(1))
    t.lexer.stack.append('INVOCACAOFUN')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_INVOCACAOFUN_VAR(t):
    r'\w+'
    print('Invocacação fun variavel')
    return t

def t_INVOCACAOFUN_ABREL(t):
    r'\['
    print('Invocacação fun Lista')
    t.lexer.begin('LISTSTATE')
    t.lexer.stack.append('INVOCACAOFUN')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_INVOCACAOFUN_FECHAP(t):
    r'\)'
    pop = t.lexer.stack.pop(-1)
    t.lexer.begin(pop)
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_INVOCACAOFUN_ABREP(t):
    r'\('
    t.lexer.stack.append('INVOCACAOFUN')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_RETURNFUN_CHAMADAFUN(t):
    r'\w+\('
    print('Retorno chamada função ' + re.match('(\w+)',t.value).group(1))
    t.lexer.begin('INVOCACAOFUN')
    t.lexer.stack.append('RETURNFUN')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_RETURNFUN_ABREP(t):
    r'\('
    print('(')
    return t

def t_RETURNFUN_FECHAP(t):
    r'\)'
    print(')')
    return t

def t_RETURNFUN_BOOL(t):
    r'(true|false)'
    print('Retorno booleano ' + re.search('\w+',t.value).group())
    return t

def t_RETURNFUN_NUMBER(t):
    r'\d+(\.d+)?'
    print('Retorno número ' + re.search('((\+|\-)?\d+(\.d+)?)',t.value).group())
    return t

def t_RETURNFUN_LIST(t):
    r'(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])'
    print('Retorno lista ' + re.search('(\[\s*\]|\[\s*((\w+|\d+)\s*,\s*)*(\w+|\d+)\s*\])',t.value).group())
    return t

def t_RETURNFUN_ABREL(t):
    r'\['
    print('Return Lista')
    t.lexer.begin('LISTSTATE')
    t.lexer.stack.append('RETURNFUN')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_RETURNFUN_VAR(t):
    r'\w+'
    print('Retorno var ' + re.search('\w+',t.value).group())
    return t

def t_LISTSTATE_FECHAL(t):
    r'\]'
    pop = t.lexer.stack.pop(-1)
    t.lexer.begin(pop)
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_LISTSTATE_CHAMADAFUN(t):
    r'\w+\('
    print('Chamada função lista ' + re.match('(\w+)',t.value).group(1))
    t.lexer.begin('INVOCACAOFUN')
    t.lexer.stack.append('LISTSTATE')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_LISTSTATE_VAR(t):
    r'\w+'
    print('Var lista')
    return t

def t_LISTSTATE_OR(t):
    r'\|'
    print('+1 elemento')
    return t

def t_LISTSTATE_ABREL(t):
    r'\['
    print('Lista de Lista')
    t.lexer.stack.append('LISTSTATE')
    print(f'Stack atual: {t.lexer.stack}')
    return t

def t_error(t):
    t.lexer.skip(1)
    return t

lexer = lex()
lexer.stack = []

inp2 = '''
"""FPYTHON
deff pertence([],_)
    return false
end

deff pertence([h|t],num)
    if (h == num) then 
        return true end
    else 
        return pertence(t,num) end
end

deff append([],num)
    return [num]
end

deff append([h|t],num)
    return [h|append(t,num)]
end

deff adiciona(l,num)
    if (not pertence(l,num)) then
        return append(l,num) end
    else
        return l end
end

deff eliminarepetidos([])
    return []
end
deff eliminarepetidos([h|t])
    return adiciona(eliminarepetidos(t),h)
end
"""

lista = [1,2,3,4,5,6,3,4,51,243,13,53,32]
soma = f_eliminarepetidos_(lista)
print(soma)
'''

inp = '''

"""FPYTHON
deff mais_um(x)
    return x + 1
end

deff sum([])
    return 0
end

deff div(n,0)
    return 0
end

deff div(0,n)
    return 0
end

deff div(n,-1)
    return n*(-1)
end

deff sum([h | t])
    return h + sum(t)
end

deff cond(x)
    if (x < 1) then
           return 2
        end
    else
            return 3
        end
end

deff con2([],_)
    return false
end

deff con2([h|t],n)
    if (n == h) then
        if (not con2(t,n)) then
            if(true) then
                return true end
            else
                return false end
        else
            return false end
    else 
        if (con2(t,n)) then
            if(true) then
                return true end
            else
                return false end
        else
            return false end
end

deff seila([1,2],0,true)
    return 4 end

deff seila([],num,true)
    return num+1 end

deff seila([],num,false)
    return num end

deff seila([h|t],num,true)
    return h + seila(t) + num + 1 end

deff seila([h|t],num,false)
    return h + seila3(seila(t)) + num end

deff seila3(d)
    return seila4(5+(3*d)) end
"""

x = 4
y = f_mais_um_(x)
print(y)
l = [1,2,3,4,5]
sum_l = f_sum_(l)
print(sum_l)
'''
lexer.input(inp)
t = lexer.token()
while(t):
    t = lexer.token()