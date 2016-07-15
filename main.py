import sys

def evalPostfix(postfixExpr):
    s = list()
    for symbol in postfixExpr:
        try:
            s.append(float(symbol))
        except:
            if len(s) > 0:
                result = None
                if symbol == '+':
                    result = s.pop() + s.pop()
                elif symbol == '-':
                    last = s.pop()
                    first = s.pop()
                    result = first - last
                elif symbol == '*':
                    result = s.pop() * s.pop()
                elif symbol == '/':
                    last = s.pop()
                    first = s.pop()
                    result = first / last
                if result:
                    s.append(result)
                else:
                    raise ValueError('Unknown symbol %s' % symbol)
    return s.pop()

def infixToPostfix(infixExpr):
    s = []
    outlst = []
    prec = {
        '/': 3,
        '*': 3,
        '+': 2,
        '-': 2,
        '(': 1,
    }

    tokenlst = infixExpr.split(' ')
    for token in tokenlst:
        if token[0] in '0123456789':
            outlst.append(token)
        elif token == '(':
            s.append(token)
        elif token == ')':
            topToken = s.pop()
            while topToken != '(':
                outlst.append(topToken)
                topToken = s.pop()
        else:
            while len(s) > 0 and prec[s[-1:][0]] >= prec[token]:
                outlst.append(s.pop())
            s.append(token)

    while len(s) > 0:
        opToken = s.pop()
        outlst.append(opToken)
    return outlst

def main():
    test()
    return 0

def test():
    assert 2.0 == evalPostfix(infixToPostfix('4 * 2 - 3 * 2'))
    assert 1.375 == evalPostfix(infixToPostfix('3 / 4 / 2 + 1'))
    assert 1.375 == evalPostfix(infixToPostfix('1.0 + 0.375'))

if __name__ == '__main__':
    sys.exit(main())
