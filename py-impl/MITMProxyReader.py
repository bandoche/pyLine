#!/usr/bin/env python
import io
import sys


class MITMProxyReader(object):
	"""docstring for MITMProxyReader"""
	def __init__(self, arg = None):
		super(MITMProxyReader, self).__init__()
		# self.read_file = read_file
		self.arg = arg

	def read_file(self, filename):
		f = io.open(filename, 'rb')
		data = f.read()
		clean_list, modified = self.read_data(data)
		clean_dict = []

		# to treat multiple req / resp
		for clean_list_item in clean_list:
			clean_dict.append(self.convert_cleanlist_to_dict(clean_list_item))
		return clean_dict

	def read_data(self, raw_data):
		start = 0
		clean_list = []
		modified = False

		while True:
			idx = raw_data.find(':', start+1)
			if (idx > 0):
				length = raw_data[start:idx]
				if length == '':
					break
				try:
					length = int(length)
					pass
				except Exception, e:
					# it is clean data
					return (raw_data, False) 
					raise e
				if length > 0:
					clean_data = raw_data[idx + 1:length + idx + 1]
					test_list, test_modified = self.read_data(clean_data)
					if test_modified:
						clean_list.append(test_list)
					else: 
						clean_list.append(clean_data)
					start = length + idx + 2
				elif length == 0:
					clean_list.append('')
					start = start + 3
				else:
					print "weird!"
					modified = False
					break
				if (start >= len(raw_data)):
					break
				modified = True
			else:
				modified = False
				break
		# print clean_list
		return (clean_list, modified)

	def convert_cleanlist_to_dict(self, clean_list):
		key_flag = True
		key_name = ''
		idx = 0

		clean_dict = {}
		for item in clean_list:
			if key_flag:
				if isinstance(item, str):
					key_name = item
				else:
					return self.convert_cleanlist_to_dict(item)
			else:
				if isinstance(item, str):
					clean_dict[key_name] = item
				else:
					converted = self.convert_cleanlist_to_dict(item)
					clean_dict[key_name] = converted
			key_flag = not key_flag
		return clean_dict


