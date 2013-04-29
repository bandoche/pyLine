#!/usr/bin/env python
import io
import sys
from struct import pack, unpack
from MITMProxyReader import MITMProxyReader

class TType:
  STOP   = 0
  VOID   = 1
  BOOL   = 2
  BYTE   = 3
  I08    = 3
  DOUBLE = 4
  I16    = 6
  I32    = 8
  I64    = 10
  STRING = 11
  UTF7   = 11
  STRUCT = 12
  MAP    = 13
  SET    = 14
  LIST   = 15
  UTF8   = 16
  UTF16  = 17

class CompactType:
  STOP = 0x00
  TRUE = 0x01
  FALSE = 0x02
  BYTE = 0x03
  I16 = 0x04
  I32 = 0x05
  I64 = 0x06
  DOUBLE = 0x07
  BINARY = 0x08
  LIST = 0x09
  SET = 0x0A
  MAP = 0x0B
  STRUCT = 0x0C

CTYPES = {TType.STOP: CompactType.STOP,
          TType.BOOL: CompactType.TRUE,  # used for collection
          TType.BYTE: CompactType.BYTE,
          TType.I16: CompactType.I16,
          TType.I32: CompactType.I32,
          TType.I64: CompactType.I64,
          TType.DOUBLE: CompactType.DOUBLE,
          TType.STRING: CompactType.BINARY,
          TType.STRUCT: CompactType.STRUCT,
          TType.LIST: CompactType.LIST,
          TType.SET: CompactType.SET,
          TType.MAP: CompactType.MAP
          }

CLEAR = 0
FIELD_WRITE = 1
VALUE_WRITE = 2
CONTAINER_WRITE = 3
BOOL_WRITE = 4
FIELD_READ = 5
CONTAINER_READ = 6
VALUE_READ = 7
BOOL_READ = 8


global _VALUES_TO_NAMES
_VALUES_TO_NAMES = ('STOP',
                  'VOID',
                  'BOOL',
                  'BYTE',
                  'DOUBLE',
                  None,
                  'I16',
                  None,
                  'I32',
                  None,
                 'I64',
                 'STRING',
                 'STRUCT',
                 'MAP',
                 'SET',
                 'LIST',
                 'UTF8',
                 'UTF16')




global TTYPES
TTYPES = {}
for k, v in CTYPES.items():
  TTYPES[v] = k
TTYPES[CompactType.FALSE] = TType.BOOL

def makeZigZag(n, bits):
	return (n << 1) ^ (n >> (bits - 1))


def fromZigZag(n):
	return (n >> 1) ^ -(n & 1)

def __readZigZag(data, idx):
	v, idx= readVarint(data, idx)
	return fromZigZag(v)



def readVarint(data,idx):
	result = 0
	shift = 0
	while True:
		x = data[idx]
		byte = ord(x)
		result |= (byte & 0x7f) << shift
		if byte >> 7 == 0:
			return result, idx
		shift += 7
		idx = idx + 1
		# print "idx++"

def __getTType(byte):
	return TTYPES[byte & 0x0f]


def readFieldBegin(data, idx, __last_fid):
	# assert self.state == FIELD_READ, self.state
	type = ord(data[idx]) #self.__readUByte()
	# print type
	if type & 0x0f == TType.STOP:
	  return (0, 0, 0, __last_fid, idx)
	delta = type >> 4
	if delta == 0:
		idx = idx + 1
		# print "idx ++"
		fid = __readZigZag(data, idx)
	else:
		fid = __last_fid + delta
		__last_fid = fid
	type = type & 0x0f
	# print type
	if type == CompactType.TRUE:
	  state = BOOL_READ
	  __bool_value = True
	elif type == CompactType.FALSE:
	  state = BOOL_READ
	  __bool_value = False
	else:
	  state = VALUE_READ
	return (__getTType(type), fid, state, __last_fid, idx + 1)


def readCollectionBegin(data, idx):
	# assert self.state in (VALUE_READ, CONTAINER_READ), self.state
	size_type = ord(data[idx]) #__readUByte()
	idx = idx + 1
	size = size_type >> 4
	type = __getTType(size_type)
	if size == 15:
	  size = readVarint(data, idx)
	  idx = idx + 1
	return type, size, idx+1




def parse_thrift(raw_data):
	global TTYPES
	# print raw_data.encode('hex')
	if raw_data[0:2] == "\x82\x21" or raw_data[0:2] == "\x82\x41":
		print "correct thift TCompactProtocol"
	else:
		print "wrong TCompactProtocol"
		return
	#method name
	method_len = ord(raw_data[3])
	method_name = raw_data[4:method_len+4]
	print "method name : ",method_name
	raw_data = raw_data[method_len+4:] 

	#datas
	ptr = 0
	fid = 0
	__last_fid = 0
	while True:
		# print ptr
		print "#@", ptr,
		type, fid, state, __last_fid, ptr = readFieldBegin(raw_data, ptr, __last_fid)
		# print ptr
		# print ptr
		# print "ptr = ", ptr , ", type =", _VALUES_TO_NAMES[type], '(', type, '), fid = ', fid, ', ',
		print "#", fid, "-", _VALUES_TO_NAMES[type],  
		if type == CompactType.TRUE:
			print "bool - true"
			# ptr = ptr + 1
		elif type == CompactType.FALSE:
			print "bool - false"
			# ptr = ptr + 1
		elif type == CompactType.STOP:
			print
			return
		elif type in (TType.LIST, TType.SET):
			type2, size, ptr = readCollectionBegin(raw_data, ptr)
			print
			ptr = ptr - 2
			# print 'type2 = ',type2
		elif type in (TType.STRUCT, TType.MAP):
			# type2, fid, state, __last_fid, ptr = readFieldBegin(raw_data, ptr, __last_fid)
			type2, size, ptr = readCollectionBegin(raw_data, ptr)
			# print "ptr = ", ptr
			print
			ptr = ptr - 2
			# print 'type2 = ',type2
		elif type in (TType.I16, TType.I32):
			print "(1) = ", ord(raw_data[ptr])
			ptr = ptr + 1
		elif type == TType.I64:
			val, ptr = readVarint(raw_data, ptr)
			val = fromZigZag(val)
			print "(1) = ", val
			ptr = ptr + 1
		else:
			# ptr = ptr + 1
			# print ptr, ord(raw_data[ptr])
			# print ptr
			var_len, ptr = readVarint(raw_data, ptr) #unpack('!B', raw_data[ptr])
			ptr = ptr + 1
			if (var_len > 0):
				var_data = raw_data[ptr:ptr+var_len]
				print "(", var_len, ") = ", var_data
				ptr = ptr + var_len 
			else:
				print "(0)"


if len(sys.argv) == 1:
	print 'no filename'
else:
	filename = sys.argv[1]
	mpr = MITMProxyReader()
	clean_dict = mpr.read_file(filename)
	for clean_dict_item in clean_dict:
		# print clean_dict_item
		print clean_dict_item['request']['host'] , clean_dict_item['request']['path']
		try:
			parse_thrift(clean_dict_item['request']['content'])
			pass
		except Exception, e:
			print "[error]", e

		try:
			parse_thrift(clean_dict_item['response']['content'])
			pass
		except Exception, e:
			print "[error]", e
	# print clean_dict



