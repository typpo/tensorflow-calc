import re
import sys
import os

import tensorflow as tf

OPERATOR_PRECEDENCE = {
    '^': 4,
    '/': 3,
    '*': 3,
    '+': 2,
    '-': 2,
    '(': 1,
}

TF_OPERATORS = {
    '+': tf.add,
    '-': tf.sub,
    '*': tf.mul,
    '/': tf.div,
    '^': tf.pow,
}

class TensorflowCalculator(object):
    def evalInfix(self, infixExpr):
        return self.evalPostfix(self.infixToPostfix(infixExpr))

    def evalPostfix(self, postfixExpr):
        stack = []
        for symbol in postfixExpr:
            try:
                stack.append(tf.constant(float(symbol), name='Number_%s' % symbol))
            except ValueError:
                result = None
                tensor = self.getTensorForSymbol(symbol, stack)
                stack.append(tensor)
        sess = tf.Session()
        writer = tf.train.SummaryWriter(os.path.join(os.getcwd(), 'logs'), sess.graph)
        with sess.as_default():
            return stack.pop().eval()

    def getTensorForSymbol(self, symbol, stack):
        tfOp = TF_OPERATORS.get(symbol)
        if not tfOp:
            raise ValueError('Unknown symbol %s' % symbol)
        second = stack.pop()
        first = stack.pop()
        return tfOp(first, second)

    def tokenize(self, infixExpr):
        tokens = re.findall('[\^+-/*//()]|[-+]?\d*\.\d+|\d+', infixExpr)
        result = []
        # Starts True to handle case where first symbol is unary operator.
        prevWasToken = True
        addUnaryPrefixToNextToken = None
        for token in tokens:
            if token == '-':
                # Move unary negative operator into the symbol.
                if prevWasToken:
                    addUnaryPrefixToNextToken = token
                    continue

            prevWasToken = False
            if token in OPERATOR_PRECEDENCE.keys():
                prevWasToken = True

            if addUnaryPrefixToNextToken:
                token = addUnaryPrefixToNextToken + token
                addUnaryPrefixToNextToken = None

            result.append(token)
        return result

    def infixToPostfix(self, infixExpr):
        # See https://en.wikipedia.org/wiki/Shunting-yard_algorithm
        tokens = self.tokenize(infixExpr)
        stack = []
        result = []
        for token in tokens:
            if re.match(r'[\d\.-]', token) and token != '-':
                result.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                topToken = stack.pop()
                while topToken != '(':
                    result.append(topToken)
                    topToken = stack.pop()
            else:
                while len(stack) > 0 and OPERATOR_PRECEDENCE[stack[-1:][0]] >= OPERATOR_PRECEDENCE[token]:
                    result.append(stack.pop())
                stack.append(token)

        while len(stack) > 0:
            opToken = stack.pop()
            result.append(opToken)

        return result

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        return test()

    while True:
        print '\nEnter an expression to calculate (t to test, q to exit):'
        print '> ',
        expr = raw_input().strip()
        if expr == 'q':
            break
        elif expr == 'test' or expr == 't':
            test()
        else:
            calc = TensorflowCalculator()
            print calc.evalInfix(expr)
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
    testExpr(1, '-1 + 2')
    testExpr(4.3, '(5.3)+-1')
    testExpr(107, '5 + 10 * 9 + (5 + -1) * 9 / 3 ')
    print 'All tests passed.'
    return 0

def testExpr(expected, expr):
    calc = TensorflowCalculator()
    val = calc.evalInfix(expr)
    assert abs(expected - val) < 1e-4, \
        'Expected %f but got %f instead' % (expected, val)

if __name__ == '__main__':
    sys.exit(main())
