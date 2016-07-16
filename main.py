import re
import sys
import os

import tensorflow as tf

def evalInfix(infixExpr):
    return evalPostfix(infixToPostfix(infixExpr))

def evalPostfix(postfixExpr):
    s = []
    for symbol in postfixExpr:
        try:
            s.append(tf.constant(float(symbol), name=symbol))
        except:
            if len(s) > 0:
                result = None
                if symbol == '+':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.add(first, last)
                elif symbol == '-':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.sub(last, first)
                elif symbol == '*':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.mul(first, last)
                elif symbol == '/':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.div(last, first)
                elif symbol == '^':
                    first = s.pop()
                    last = s.pop()
                    tensor = tf.pow(last, first)
                else:
                    raise ValueError('Unknown symbol %s' % symbol)
                s.append(tensor)
    sess = tf.Session()
    writer = tf.train.SummaryWriter(os.path.join(os.getcwd(), 'logs'), sess.graph)
    with sess.as_default():
        return s.pop().eval()

def infixToPostfix(infixExpr):
    # See https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    s = []
    result = []
    prec = {
        '^': 4,
        '/': 3,
        '*': 3,
        '+': 2,
        '-': 2,
        '(': 1,
    }

    tokens = re.findall('[\^+-/*//()]|[-+]?\d*\.\d+|\d+', infixExpr)
    print tokens
    for token in tokens:
        if token[0] in '0123456789':
            result.append(token)
        elif token == '(':
            s.append(token)
        elif token == ')':
            topToken = s.pop()
            while topToken != '(':
                result.append(topToken)
                topToken = s.pop()
        else:
            while len(s) > 0 and prec[s[-1:][0]] >= prec[token]:
                result.append(s.pop())
            s.append(token)

    while len(s) > 0:
        opToken = s.pop()
        result.append(opToken)
    return result

def main():
    while True:
        print '\nEnter an expression to calculate (q to exit):'
        print '> ',
        expr = raw_input().strip()
        if expr == 'q':
            break
        elif expr == 'test':
            test()
        else:
            print evalInfix(expr)
    return 0

def test():
    print 'Testing...'
    testExpr(2.0, '4 * 2 - 3 * 2')
    testExpr(1.375, '3 / 4 / 2 + 1')
    testExpr(1.375, '1.0 + 0.375')
    testExpr(25, '( 3 + 2 ) * 5')
    testExpr(126, '5 ^ 3 + 1')
    testExpr(6.3, '5.3+1')
    testExpr(6.3, '(5.3)+1')
    testExpr(4.3, '(5.3)+-1')
    print 'All tests passed.'

def testExpr(expected, expr):
    val = evalInfix(expr)
    assert abs(expected - val) < 1e-4, \
        'Expected %f but got %f instead' % (expected, val)

if __name__ == '__main__':
    sys.exit(main())
