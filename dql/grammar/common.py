""" Common use grammars """
from pyparsing import (Word, Upcase, Optional, Combine, Group, alphas, nums,
                       alphanums, quotedString, Keyword, Suppress,
                       delimitedList)


def upkey(name):
    """ Shortcut for creating an uppercase keyword """
    return Upcase(Keyword(name, caseless=True))

# pylint: disable=C0103

and_, from_, into, in_, table_key, null, where_ = \
    map(upkey, ['and', 'from', 'into', 'in', 'table', 'null', 'where'])

var = Word(alphas, alphanums + '_-').setName('variable')
table = var.setResultsName('table')
type_ = (upkey('string') |
         upkey('number') |
         upkey('binary'))\
    .setName('type').setResultsName('type')

_sign = Word('+-', exact=1)
num = Combine(Optional(_sign) + Word(nums) +
              Optional('.' + Optional(Word(nums)))).setName('number')

primitive = (null.setResultsName('null') |
             num.setResultsName('number') |
             quotedString.setResultsName('str') |
             Combine('b' + quotedString).setResultsName('binary') |
             var.setResultsName('var'))
set_ = (Suppress('(') + delimitedList(Group(primitive)) +
        Suppress(')')).setResultsName('set')
value = Group(primitive | set_).setName('value')
# Wrap these in a group so they can be used independently
primitive = Group(primitive).setName('primitive')
set_ = Group(set_).setName('set')
