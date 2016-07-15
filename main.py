import sys

import tensorflow as tf

def evalPostfix(postfixExpr):
    s = []
    for symbol in postfixExpr:
        try:
            s.append(float(symbol))
        except:
            if len(s) > 0:
                result = None
                if symbol == '+':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.add(tf.constant(first), tf.constant(last))
                    result = first + last
                elif symbol == '-':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.subtract(tf.constant(first), tf.constant(last))
                    result = first - last
                elif symbol == '*':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.mul(tf.constant(first), tf.constant(last))
                    result = first * last
                elif symbol == '/':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.div(tf.constant(first), tf.constant(last))
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
    print 'Testing...'
    assert 2.0 == evalPostfix(infixToPostfix('4 * 2 - 3 * 2'))
    assert 1.375 == evalPostfix(infixToPostfix('3 / 4 / 2 + 1'))
    assert 1.375 == evalPostfix(infixToPostfix('1.0 + 0.375'))
    print 'All tests passed.'

if __name__ == '__main__':
    sys.exit(main())
