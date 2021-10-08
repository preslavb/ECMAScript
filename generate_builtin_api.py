#!/usr/bin/env python
import json, os, sys
import xml.etree.ElementTree as ET

BUILTIN_CLASSES = [
	'Vector2',
	'Rect2',
	'Color',
	'Vector3',
	'Basis',
	'Quaternion',
	'RID',
	'Transform2D',
	'Plane',
	'AABB',
	"Transform3D",
	"PackedByteArray",
	"PackedInt32Array",
	"PackedInt64Array",
	"PackedFloat32Array",
	"PackedFloat64Array",
	"PackedStringArray",
	"PackedVector2Array",
	"PackedVector3Array",
	"PackedColorArray",
]

MAX_CONSTRUCTOR_ARGC = {
	'Vector2': 2,
	'Rect2': 4,
	'Color': 4,
	'Vector3': 3,
	'Basis': 0,
	'Quaternion': 0,
	'RID': 0,
	'Transform2D': 0,
	'Plane': 0,
	'AABB': 0,
	"Transform3D": 0,
	"PackedByteArray": 0,
	"PackedInt32Array": 0,
	"PackedInt64Array": 0,
	"PackedFloat32Array": 0,
	"PackedFloat64Array": 0,
	"PackedStringArray": 0,
	"PackedVector2Array": 0,
	"PackedVector3Array": 0,
	"PackedColorArray": 0,
}

TYPE_MAP = {
	'int': 'number',
	'float': 'number',
	'bool': 'boolean',
	'String': 'string',
	'NodePath': 'string',
}

METHOD_OP_EQUALS = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "equals",
	"native_method": "Variant::OP_EQUAL",
	"return": "boolean"
}

METHOD_OP_NOT_EQUALS = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "not_equals",
	"native_method": "Variant::OP_NOT_EQUAL",
	"return": "boolean"
}

METHOD_OP_LESS = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "less",
	"native_method": "Variant::OP_LESS",
	"return": "boolean"
}

METHOD_OP_LESS_EQAUL = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "less_equals",
	"native_method": "Variant::OP_LESS_EQUAL",
	"return": "boolean"
}

METHOD_OP_GREATER = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "greater",
	"native_method": "Variant::OP_GREATER",
	"return": "boolean"
}

METHOD_OP_GREATER_EQAUL = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "greater_equals",
	"native_method": "Variant::OP_GREATER_EQUAL",
	"return": "boolean"
}

METHOD_OP_ADD = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "add",
	"native_method": "Variant::OP_ADD",
	"return": "${class_name}"
}

METHOD_OP_ADD_ASSIGN = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "add_assign",
	"native_method": "Variant::OP_ADD",
  "assign": True,
	"return": "this"
}

METHOD_OP_SUB = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "subtract",
	"native_method": "Variant::OP_SUBTRACT",
	"return": "${class_name}"
}

METHOD_OP_SUB_ASSIGN = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "subtract_assign",
	"native_method": "Variant::OP_SUBTRACT",
  "assign": True,
	"return": "this"
}

METHOD_OP_MUL = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "multiply",
	"native_method": "Variant::OP_MULTIPLY",
	"return": "${class_name}"
}

METHOD_OP_MUL_ASSIGN = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "multiply_assign",
	"native_method": "Variant::OP_MULTIPLY",
  "assign": True,
	"return": "this"
}

METHOD_OP_DIV = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "multiply",
	"native_method": "Variant::OP_DIVIDE",
	"return": "${class_name}"
}

METHOD_OP_DIV_ASSIGN = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "${class_name}"
		}
	],
	"name": "multiply_assign",
	"native_method": "Variant::OP_DIVIDE",
  "assign": True,
	"return": "this"
}

METHOD_OP_NEG = {
	"arguments": [],
	"name": "negate",
	"native_method": "Variant::OP_NEGATE",
	"return": "${class_name}"
}

METHOD_OP_POS = {
	"arguments": [],
	"name": "negate",
	"native_method": "Variant::OP_POSITIVE",
	"return": "${class_name}"
}

METHOD_OP_MOD = {
	"arguments": [],
	"name": "negate",
	"native_method": "Variant::OP_MODULE",
	"return": "${class_name}"
}

METHOD_PACKED_ARRAY_GET = {
	"arguments": [
		{
			"default_value": None,
			"has_default_value": False,
			"type": "number"
		}
	],
	"name": "get",
  "array": True,
	"native_method": "operator[]",
	"return": "Variant"
}

IGNORED_PROPS = {
	"Rect2": ['end', 'grow_side'],
	"Color": ['h', 's', 'v', 'r8', 'g8', 'b8', 'a8'],
	"Transform2D": ['xform', 'xform_inv'],
	"Basis": ['is_equal_approx'],
	"Plane": ['intersects_segment', 'intersects_ray', 'intersect_3'],
	"AABB": ['end'],
	"Transform3D": ['xform', 'xform_inv'],
	"PackedByteArray": ['compress', 'decompress', 'decompress_dynamic', 'get_string_from_ascii', 'get_string_from_utf8', 'get_string_from_utf16', 'get_string_from_utf32', 'hex_encode'],
}

PROPERTY_REMAP = {
	"Transform2D": {
		"x": "elements[0]",
		"y": "elements[1]",
		"origin": "elements[2]",
	},
	"Basis": {
		"x": "elements[0]",
		"y": "elements[1]",
		"z": "elements[2]",
	},
	"Plane": {
		"x": "normal.x",
		"y": "normal.y",
		"z": "normal.z",
	}
}

OPERATOR_METHODS = {
	"Vector2": [
		METHOD_OP_NEG,
		METHOD_OP_EQUALS,
		METHOD_OP_LESS,
		METHOD_OP_LESS_EQAUL,
		METHOD_OP_ADD,
		METHOD_OP_ADD_ASSIGN,
		METHOD_OP_SUB,
		METHOD_OP_SUB_ASSIGN,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
		METHOD_OP_DIV,
		METHOD_OP_DIV_ASSIGN,
	],
	"Vector3": [
		METHOD_OP_NEG,
		METHOD_OP_EQUALS,
		METHOD_OP_LESS,
		METHOD_OP_LESS_EQAUL,
		METHOD_OP_ADD,
		METHOD_OP_ADD_ASSIGN,
		METHOD_OP_SUB,
		METHOD_OP_SUB_ASSIGN,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
		METHOD_OP_DIV,
		METHOD_OP_DIV_ASSIGN,
	],
	"Basis": [
		METHOD_OP_EQUALS,
		METHOD_OP_ADD,
		METHOD_OP_ADD_ASSIGN,
		METHOD_OP_SUB,
		METHOD_OP_SUB_ASSIGN,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
	],
	"Quataternion": [
		METHOD_OP_NEG,
		METHOD_OP_EQUALS,
		METHOD_OP_ADD,
		METHOD_OP_ADD_ASSIGN,
		METHOD_OP_SUB,
		METHOD_OP_SUB_ASSIGN,
	],
	"Rect2": [
		METHOD_OP_EQUALS
	],
	"Transform2D": [
		METHOD_OP_EQUALS,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
	],
	"Color": [
		METHOD_OP_NEG,
		METHOD_OP_EQUALS,
		METHOD_OP_LESS,
		METHOD_OP_ADD,
		METHOD_OP_ADD_ASSIGN,
		METHOD_OP_SUB,
		METHOD_OP_SUB_ASSIGN,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
		METHOD_OP_DIV,
		METHOD_OP_DIV_ASSIGN,
	],
	"RID": [
		METHOD_OP_EQUALS,
		METHOD_OP_LESS,
		METHOD_OP_LESS_EQAUL,
	],
	"Plane": [
		METHOD_OP_NEG,
		METHOD_OP_EQUALS,
	],
	"AABB": [
		METHOD_OP_EQUALS,
	],
	"Transform3D": [
		METHOD_OP_EQUALS,
		METHOD_OP_MUL,
		METHOD_OP_MUL_ASSIGN,
	]
}

def apply_pattern(template, values):
	for key in values:
		template = template.replace( '${' + key + '}', values[key])
	return template

def parse_class(cls):
	class_name = cls.get('name')
	ret = {'name': class_name}
	members = []
	methods = []
	operators = []
	constants = []
	ret['properties'] = members
	ret['methods'] = methods
	ret['operators'] = operators
	ret['constants'] = constants
	ret['constructor_argc'] = MAX_CONSTRUCTOR_ARGC[class_name]
	
	for m in (cls.find("members") if cls.find("members") is not None else []):
		m_dict = dict(m.attrib)
		type = m_dict['type']
		name = m_dict['name']
		if (class_name in IGNORED_PROPS) and (name in IGNORED_PROPS[class_name]):
			continue
		if type in TYPE_MAP:
			type = TYPE_MAP[type]
		native_prop = name
		if class_name in PROPERTY_REMAP:
			if name in PROPERTY_REMAP[class_name]:
				native_prop = PROPERTY_REMAP[class_name][name]
		members.append({'name': name, 'type': type, 'native': native_prop})
	
	for m in (cls.find("methods") if cls.find("methods") is not None else []):
		m_dict = dict(m.attrib)
		method_name = m_dict['name']
		variant_call = class_name.startswith("PackedByte") and method_name.startswith("encode") or method_name.startswith("decode") or method_name.startswith("to_int") or method_name.startswith("to_float") or method_name.startswith("has_encoded_var")
		if method_name == class_name:
			continue# ignore constructors
		if class_name in IGNORED_PROPS and method_name in IGNORED_PROPS[class_name]:
			continue# ignored methods
		if method_name.startswith("operator"):
			continue
		return_type = m.find("return").attrib["type"] if m.find("return") != None else "void"
		if return_type in TYPE_MAP:
			return_type = TYPE_MAP[return_type]
		arguments = []
		for arg in m.iter('argument'):
			dictArg = dict(arg.attrib)
			if "dictArg" in dictArg: dictArg.pop("index")
			dictArg["default_value"] = dictArg["default"] if "default" in dictArg else None
			if "default" in dictArg: dictArg.pop("default")
			type = dictArg['type']
			if type in TYPE_MAP:
				type = TYPE_MAP[type]
			arguments.append({
				'type': type,
				'default_value': dictArg['default_value'],
				'has_default_value': "default" in dictArg
			})
		methods.append({
			'name': method_name,
			'native_method': method_name,
			'return': return_type,
			'arguments': arguments,
			'variant_call': variant_call
		})
	if class_name.startswith("Packed") and class_name.endswith("Array"):
		methods.append(METHOD_PACKED_ARRAY_GET)
	# add operator methods
	if class_name in OPERATOR_METHODS:
		for em in OPERATOR_METHODS[class_name]:
			operators.append(em)
	
	for c in (cls.find("constants") if cls.find("constants") is not None else []):
		const_name = c.get("name")
		if class_name in IGNORED_PROPS and const_name in IGNORED_PROPS[class_name]:
			continue
		constants.append(dict(c.attrib))
	return json.loads(apply_pattern(json.dumps(ret), {
		'class_name': class_name,
	}))

def generate_api_json(MODULE_DIR, ENGINE_DIR):
	DOCS_DIR = os.path.abspath(os.path.join(ENGINE_DIR, "doc/classes"))
	print(MODULE_DIR)
	print(DOCS_DIR)
	OUTPUT_FILE = os.path.join(MODULE_DIR, "builtin_api.gen.json")

	classes = []
	for cls in BUILTIN_CLASSES:
		tree = ET.parse(open(os.path.join(DOCS_DIR, cls + '.xml'), 'r'))
		data = tree.getroot()
		classes.append(parse_class(data))
	json.dump(classes, open(OUTPUT_FILE, 'w'), ensure_ascii=False, indent=2, sort_keys=True)
	
if __name__ == "__main__":
	generate_api_json()
