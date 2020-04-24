import csv
import re
from pathlib import Path


class Node:
	def __init__(self):
		self.properties = None
		self.instance_type = []

	def add_property(self, property_name: str, property_value: str) -> None:
		if not self.properties:
			self.properties = Properties()
		self.properties.add_property(property_name, property_value)

	def add_instance_type(self, instance_type):
		self.instance_type.append(instance_type)

	def serialize(self, node_id):
		if self.properties:
			serialized_properties = self.properties.serialize_node_properties()
		else:
			serialized_properties = ""
		serialized_instance_type = ':'.join(self.instance_type)
		if self.instance_type:
			serialized_node = "CREATE ({}:{} {})".format(node_id, serialized_instance_type, serialized_properties)
		else:
			serialized_node = "CREATE ({} {})".format(node_id, serialized_properties)
		return serialized_node


class NodeStore:
	def __init__(self):
		self.directory = dict()

	def get_or_create(self, node_id: str) -> Node:
		if node_id not in self.directory:
			self.directory[node_id] = Node()
		return self.directory[node_id]

	def serialize(self):
		for node_id, node in self.directory.items():
			yield node.serialize(node_id)


class Relationship:
	def __init__(self):
		self.name = None
		self.src_node = None
		self.dst_node = None
		self.properties = None

	def add_names(self, name, src_node_id, dst_node_id):
		self.name = name
		self.src_node = src_node_id
		self.dst_node = dst_node_id

	def add_property(self, property_name, property_value):
		if not self.properties:
			self.properties = Properties()
		self.properties.add_property(property_name, property_value)

	def serialize(self):
		if self.properties:
			serialized_properties = self.properties.serialize_qualifier_properties()
		else:
			serialized_properties = ""
		serialized_relationship = "({})-[:{} {}]->({}),".format(self.src_node, self.name, serialized_properties, self.dst_node)
		return serialized_relationship


class RelationshipStore:
	def __init__(self):
		self.directory = dict()

	def get(self, relationship_id) -> Relationship:
		return self.directory.get(relationship_id, None)

	def get_or_create(self, relationship_id: str) -> Relationship:
		if relationship_id not in self.directory:
			self.directory[relationship_id] = Relationship()
		return self.directory[relationship_id]

	def serialize(self):
		yield "CREATE"
		total_relationships = len(self.directory)
		i = 0
		for relationship_id, relationship in self.directory.items():
			if i >= total_relationships - 1:
				yield relationship.serialize().rstrip(",")
			else:
				yield relationship.serialize()
			i += 1


class Properties:
	def __init__(self):
		self.property_map = dict()

	def add_property(self, property_name: str, property_value: str) -> None:
		if property_name not in self.property_map:
			self.property_map[property_name] = list()
		self.property_map[property_name].append(property_value)

	def serialize_node_properties(self):
		serialized_properties = """{"""
		for property_name, property_value in self.property_map.items():
			property_name = clean_string(property_name)
			property_value = [clean_string(v) for v in property_value]
			if is_property(property_name):
				serialized_property = "{}: ".format(property_name)
			else:
				serialized_property = "{}: ".format(property_name)
			if len(property_value) == 1:
				serialized_property += "\"{}\"".format(str(property_value[0]))
			else:
				serialized_property += "["
				for value in property_value:
					serialized_property += "\"{}\", ".format(str(value))
				serialized_property = serialized_property[:-2] + "]"
			serialized_properties += serialized_property + ", "
		serialized_properties = serialized_properties[:-2] + "}"
		return serialized_properties

	def serialize_qualifier_properties(self):
		serialized_properties = ["{"]
		for property_name, property_value in self.property_map.items():
			property_name = clean_string(property_name)
			property_value = [clean_string(v) for v in property_value]
			if is_property(property_name):
				serialized_properties.append("{}: ".format(property_name))
			else:
				serialized_properties.append("{}: ".format(property_name))
			serialized_properties.append("[")
			for value in property_value:
				if is_item(value) or is_property(value):
					serialized_properties.append("{}, ".format(str(value)))
				else:
					serialized_properties.append("\"{}\", ".format(str(value)))
			serialized_properties[-1] = serialized_properties[-1][:-2]
			serialized_properties.append("], ")
		serialized_properties[-1] = serialized_properties[-1][:-2]
		serialized_properties_as_string = ''.join(serialized_properties)
		return serialized_properties_as_string


class Graph:
	def __init__(self):
		self.node_store = NodeStore()
		self.relationship_store = RelationshipStore()

	def serialize(self, output_directory):
		file_name = str(Path(output_directory) / "results.cql")
		with open(file_name, 'w', encoding='utf8') as output_file:
			for node in self.node_store.serialize():
				output_file.write(node)
				output_file.write("\n")
			is_first_relationship = True
			for relationship in self.relationship_store.serialize():
				if is_first_relationship:
					is_first_relationship = False
				else:
					output_file.write("\t")
				output_file.write(relationship)
				output_file.write("\n")


def is_item(string: str) -> bool:
	item_pattern = "^Q[0-9]+$"
	match = re.match(item_pattern, string)
	if match:
		return True
	else:
		return False


def is_property(string: str) -> bool:
	property_pattern = "^P[0-9]+$"
	match = re.match(property_pattern, string)
	if match:
		return True
	else:
		return False


def clean_string(string):
	string = string.strip("\"")
	string = string.replace("\"", "'")
	return string


def clean_label(label):
	cleaned_label_list = [""] * len(label)
	for index, char in enumerate(label):
		if char.isalnum():
			cleaned_label_list[index] = label[index]
		else:
			cleaned_label_list[index] = "_"
	cleaned_label = ''.join(cleaned_label_list)
	return cleaned_label


def create_graph(statement_file_name: str, qualifier_file_name: str, statement_file_encoding: str, qualifier_file_encoding: str):
	# required tsv format headers for statements(unordered):
	# id, node1, property, node2
	# or
	# node1, property, node2, id, node1_label, node2_label, property_label
	# required tsv format headers for qualifiers(unordered):
	# node1, property, node2, id
	if not statement_file_encoding:
		statement_file_encoding = "UTF-8"
	if not qualifier_file_encoding:
		qualifier_file_encoding = "UTF-8"

	graph = Graph()
	node_store = graph.node_store
	relationship_store = graph.relationship_store
	if statement_file_name:
		with open(statement_file_name, 'r', encoding=statement_file_encoding) as input_file:
			statements = csv.DictReader(input_file, dialect='excel-tab', restval="")
			for statement in statements:
				src_node = node_store.get_or_create(clean_label(statement['node1']))
				if is_item(statement['node2']):
					if statement['property'] == 'P31':
						src_node.add_instance_type(clean_label(statement['node2']))
					else:
						dst_node = node_store.get_or_create(clean_label(statement['node2']))
						if 'node2_label' in statement and statement['node2_label']:
							dst_node.add_property("label", statement["node2_label"])
						relationship = relationship_store.get_or_create(clean_label(statement['id']))
						relationship.add_names(clean_label(statement['property']), clean_label(statement['node1']), clean_label(statement['node2']))
						if 'property_label' in statement and statement['property_label']:
							relationship.add_property("label", statement["property_label"])
				else:
					src_node.add_property(clean_label(statement['property']), statement['node2'])
				if 'node1_label' in statement and statement['node1_label']:
					src_node.add_property("label", statement["node1_label"])

	if qualifier_file_name:
		with open(qualifier_file_name, 'r', encoding=qualifier_file_encoding) as input_file:
			qualifiers = csv.DictReader(input_file, dialect='excel-tab', restval="")
			for qualifier in qualifiers:
				relationship = relationship_store.get(clean_label(qualifier['node1']))
				if relationship:
					relationship.add_property(clean_label(qualifier['property']), qualifier['node2'])
	return graph


def parser():
	return {'help': 'Exports data to Neo4J Cypher Query Language statements.'}


def add_arguments(parser):
	"""
	Parse arguments
	Args:
		parser (argparse.ArgumentParser)
	"""
	parser.add_argument('-sf', "--statement_file_path", action="store", type=str, dest="statement_file_path", help="Filepath of the statement file", default="")
	parser.add_argument('-qf', '--qualifier_file_path', type=str, dest="qualifier_file_path", help="Filepath of the qualifier file", default="")
	parser.add_argument('-o', '--output_directory', action="store", type=str, dest='output_directory', help="Directory where the result file will be saved", default="")
	parser.add_argument('-se', '--statement_file_encoding', type=str, dest='statement_file_encoding', help="Encoding of the statement file, eg.: UTF-8", default="")
	parser.add_argument('-qe', '--qualifier_file_encoding', type=str, dest='qualifier_file_encoding', help="Encoding of the qualifier file, eg.: UTF-8", default="")


def run(statement_file_path: str, qualifier_file_path: str, output_directory: str, statement_file_encoding: str, qualifier_file_encoding: str):
	try:
		graph = create_graph(statement_file_path, qualifier_file_path, statement_file_encoding, qualifier_file_encoding)
		graph.serialize(output_directory)
	except FileNotFoundError as exception:
		raise exception
	except Exception as ex:
		raise ex
