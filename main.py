import sys

class Stack:
    def __init__(self, itemlist=[]):
        self.items = itemlist

    def isEmpty(self):
        if self.items == []:
            return True
        else:
            return False

    def peek(self):
        return self.items[-1:][0]

    def pop(self):
        return self.items.pop()

    def push(self, item):
        self.items.append(item)
        return 0

def evalpostfix(postfixexpr):
    s = list()
    for symbol in postfixexpr:
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

def infixtopostfix(infixexpr):
    s = Stack()
    outlst = []
    prec = {}
    prec['/'] = 3
    prec['*'] = 3
    prec['+'] = 2
    prec['-'] = 2
    prec['('] = 1
    oplst = ['/','*','+','-']

    tokenlst = infixexpr.split(' ')
    for token in tokenlst:
        if token in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or token in '0123456789':
            outlst.append(token)

        elif token == '(':
            s.push(token)

        elif token == ')':
            topToken = s.pop()
            while topToken != '(':
                outlst.append(topToken)
                topToken=s.pop()
        else:
            while (not s.isEmpty()) and (prec[s.peek()] >= prec[token]):
                outlst.append(s.pop())
            s.push(token)

    while not s.isEmpty():
        opToken=s.pop()
        outlst.append(opToken)
    return outlst

def main():
    print evalpostfix(infixtopostfix('3 / 4 / 2 + 1'))
    return 0

def test():
    assert 2.0 == evalpostfix(infixtopostfix('4 * 2 - 3 * 2'))
    assert 1.375 == evalpostfix(infixtopostfix('3 / 4 / 2 + 1'))

if __name__ == '__main__':
    sys.exit(main())
