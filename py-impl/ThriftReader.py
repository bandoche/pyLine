#!/usr/bin/env python
import io
import sys
from struct import pack, unpack


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

def readVarint(data,idx):
	result = 0
	shift = 0
	while True:
		x = data[idx]
		byte = ord(x)
		result |= (byte & 0x7f) << shift
		if byte >> 7 == 0:
			return result
		shift += 7
		idx = idx + 1


def convert_mitmproxy_flow_to_object(raw_data):
	start = 0
	clean_list = []
	modified = False

	while True:
		# print raw_data
		idx = raw_data.find(':', start+1)
		# print
		# print 'idx = ', idx
		if (idx > 0):
			length = raw_data[start:idx]
			if length == '':
				# print 'wrong length - start, idx = ', start, ',' , idx #,raw_data
				break
			try:
				length = int(length)
				pass
			except Exception, e:
				# it is clean data
				return (raw_data, False) 
				raise e
			# print "length - (", length , ')'
			if length > 0:
				clean_data = raw_data[idx + 1:length + idx + 1]
				# print clean_data
				test_list, test_modified = convert_mitmproxy_flow_to_object(clean_data)
				if test_modified:
					# print "test return modified"
					clean_list.append(test_list)
				else: 
					# print "test return not modified"
					clean_list.append(clean_data)
					# print clean_data
				start = length + idx + 2
			elif length == 0:
				# print "0 length"
				clean_list.append('')
				start = start + 3
			else:
				print "weird!"
				modified = False
				break
			if (start >= len(raw_data)):
				# print "debug: start(", start, ") overflow data length(", len(raw_data), ")"
				break
			modified = True

		else:
			# print "debug: just clean!"
			modified = False
			break

	return (clean_list, modified)

def convert_cleanlist_to_dict(clean_list):
	key_flag = True
	key_name = ''

	clean_dict = {}
	for item in clean_list:
		if key_flag:
			if isinstance(item, str):
				key_name = item
				# print "key_name - ", key_name
			else:
				return convert_cleanlist_to_dict(item)
		else:
			if isinstance(item, str):
				clean_dict[key_name] = item
				# print "val(str) - ", item
			else:
				converted = convert_cleanlist_to_dict(item)
				clean_dict[key_name] = converted
				# print "val(dict) - ", converted
		key_flag = not key_flag
	return clean_dict



# def __readUByte(self):
# 	result, = unpack('!B', self.trans.readAll(1))
# 	return result

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
	print method_name
	raw_data = raw_data[method_len+4:] 

	#datas
	ptr = 0
	fid = 0
	while True:
		type, = unpack('!B', raw_data[ptr])
		print ord(raw_data[ptr]), type & 0x0f
		if type & 0x0f == TType.STOP:
		  return #(None, 0, 0)
		delta = type >> 4
		print "delta = ",delta
		if delta == 0:
			ptr = ptr + 1
			fid, = unpack('!B', raw_data[ptr])
			# fid = ord(raw_data[ptr])
		else:
			fid = fid + delta
		type = type & 0x0f

		print type
		if type == CompactType.TRUE:
			print "bool - true"
		elif type == CompactType.FALSE:
			print "bool - false"
		else:
			print "type = " ,TTYPES[type & 0x0f]

		ptr = ptr + 1
		var_len, = unpack('!B', raw_data[ptr])
		ptr = ptr + 1
		var_data = raw_data[ptr:ptr+var_len]
		print "var(", var_len, ") = ", var_data
		ptr = ptr + var_len - 1


if len(sys.argv) == 1:
	print 'no filename'
else:
	filename = sys.argv[1]
	f = io.open(filename, 'rb')
	data = f.read()
	clean_list, modified = convert_mitmproxy_flow_to_object(data)
	# print clean_list
	clean_dict = convert_cleanlist_to_dict(clean_list[0])
	# print
	# print clean_dict
	parse_thrift(clean_dict['request']['content'])


