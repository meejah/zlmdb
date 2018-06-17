#############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################


import six


class Registration(object):

    def __init__(self, slot, name, pmap):
        self.slot = slot
        self.name = name
        self.pmap = pmap


class Schema(object):
    """

    """

    SLOT_DATA_EMPTY = 0
    """
    Database slot is empty (unused, not necessarily zero'ed, but uninitialized).
    """

    SLOT_DATA_METADATA = 1
    """
    """

    SLOT_DATA_TYPE = 2
    """
    """

    SLOT_DATA_SEQUENCE = 3
    """
    """

    SLOT_DATA_TABLE = 4
    """
    Database slot contains a persistent map, for example a map of type OID->Pickle.
    """

    SLOT_DATA_INDEX = 5
    """
    """

    SLOT_DATA_REPLICATION = 6
    """
    """

    SLOT_DATA_MATERIALIZATION = 7
    """
    """

    def __init__(self):
        self._slot_to_reg = {}
        self._name_to_reg = {}

    def open(self, *args, **kwargs):
        from zlmdb._database import Database

        db = Database(self, *args, **kwargs)
        return db

    def register(self, slot, name, pmap):
        if slot in self._slot_to_reg:
            raise Exception('pmap slot "{}" already registered'.format(slot))
        if name in self._name_to_reg:
            raise Exception('pmap name "{}" already registered'.format(name))

        reg = Registration(slot, name, pmap)
        self._slot_to_reg[slot] = reg
        self._name_to_reg[name] = reg
        return pmap

    def unregister(self, key):
        if type(key) == six.text_type:
            if key in self._name_to_reg:
                reg = self._name_to_reg[key]
                del self._slot_to_reg[reg.slot]
                del self._name_to_reg[reg.name]
            else:
                raise KeyError('no pmap registered for name "{}"'.format(key))
        elif type(key) in six.integer_types:
            if key in self._slot_to_reg:
                reg = self._slot_to_reg[key]
                del self._slot_to_reg[reg.slot]
                del self._name_to_reg[reg.name]
            else:
                raise KeyError('no pmap registered for slot "{}"'.format(key))

    def __getattr__(self, key):
        if type(key) == six.text_type:
            if key in self._name_to_reg:
                return self._name_to_reg[key]
            else:
                raise KeyError('no pmap registered for name "{}"'.format(key))
        elif type(key) in six.integer_types:
            if key in self._slot_to_reg:
                return self._slot_to_reg[key]
            else:
                raise KeyError('no pmap registered for slot "{}"'.format(key))