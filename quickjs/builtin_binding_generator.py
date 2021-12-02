#!/usr/bin/env python
import json, os

DIR = os.path.abspath( os.path.dirname(__file__) )
OUTPUT_FILE = os.path.join(DIR, "quickjs_builtin_binder.gen.cpp")
API = json.load(open(os.path.join(DIR, '..', 'builtin_api.gen.json'), 'r'))

VariantTypes = {
	"boolean": "Variant::BOOL",
	"number": "Variant::FLOAT",
	"string": "Variant::STRING",
	"Vector2": "Variant::VECTOR2",
	"Vector3": "Variant::VECTOR3",
	"Basis": "Variant::BASIS",
	"Quaternion": "Variant::QUATERNION",
	"Color": "Variant::COLOR",
	"Rect2": "Variant::RECT2",
	"RID": "Variant::RID",
	"Transform2D": "Variant::TRANSFORM2D",
	"Plane": "Variant::PLANE",
	"AABB": "Variant::AABB",
	"Transform3D": "Variant::TRANSFORM3D",
	"PackedByteArray": "Variant::PACKED_BYTE_ARRAY",
	"PackedInt32Array": "Variant::PACKED_INT32_ARRAY",
	"PackedInt64Array": "Variant::PACKED_INT64_ARRAY",
	"PackedFloat32Array": "Variant::PACKED_FLOAT32_ARRAY",
	"PackedFloat64Array": "Variant::PACKED_FLOAT64_ARRAY",
	"PackedStringArray": "Variant::PACKED_STRING_ARRAY",
	"PackedVector2Array": "Variant::PACKED_VECTOR2_ARRAY",
	"PackedVector3Array": "Variant::PACKED_VECTOR3_ARRAY",
	"PackedColorArray": "Variant::PACKED_COLOR_ARRAY",
  	"Variant": "Variant"
}

JSToGodotTemplates = {
	"number": 'QuickJSBinder::js_to_number(ctx, ${arg})',
	"string": 'QuickJSBinder::js_to_string(ctx, ${arg})',
	"boolean": 'QuickJSBinder::js_to_bool(ctx, ${arg})',
	"Vector2": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getVector2()',
	"Rect2": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getRect2()',
	"Color": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getColor()',
	"RID": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getRID()',
	"AABB": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getAABB()',
	"Plane": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPlane()',
	"Quaternion": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getQuaternion()',
	"Transform2D": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getTransform2D()',
	"Vector3": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getVector3()',
	"Basis": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getBasis()',
	"Transform3D": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getTransform3D()',
	"PackedByteArray": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedByteArray()',
	"PackedInt32Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedInt32Array()',
	"PackedInt64Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedInt64Array()',
	"PackedFloat32Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedFloat32Array()',
	"PackedFloat64Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedFloat64Array()',
	"PackedStringArray": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedStringArray()',
	"PackedVector2Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedVector2Array()',
	"PackedVector3Array": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedVector3Array()',
	"PackedColorArray": '*(BINDING_DATA_FROM_JS(ctx, ${arg}))->getPackedColorArray()',
	"Variant": '(BINDING_DATA_FROM_JS(ctx, ${arg}))->get_value()',
}

GodotTypeNames = {
	"number": "real_t",
	"string": "String",
	"boolean": "bool",
	"Vector2": "Vector2",
	"Rect2": "Rect2",
	"Color": "Color",
	"RID": "RID",
	"AABB": "AABB",
	"Plane": "Plane",
	"Quaternion": "Quaternion",
	"Transform2D": "Transform2D",
	"Vector3": "Vector3",
	"Basis": "Basis",
	"Transform3D": "Transform3D",
	"PackedByteArray": "PackedByteArray",
	"PackedInt32Array": "PackedInt32Array",
	"PackedInt64Array": "PackedInt64Array",
	"PackedFloat32Array": "PackedFloat32Array",
	"PackedFloat64Array": "PackedFloat64Array",
	"PackedStringArray": "PackedStringArray",
	"PackedVector2Array": "PackedVector2Array",
	"PackedVector3Array": "PackedVector3Array",
	"PackedColorArray": "PackedColorArray",
	"Variant": "Variant",
}

GodotToJSTemplates = {
	"number": 'QuickJSBinder::to_js_number(ctx, ${arg})',
	"string": 'QuickJSBinder::to_js_string(ctx, ${arg})',
	"boolean": 'QuickJSBinder::to_js_bool(ctx, ${arg})',
	"Vector2": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Rect2": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Color": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"RID": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"AABB": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Plane": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Quaternion": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Transform2D": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Vector3": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Basis": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Transform3D": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedByteArray": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedInt32Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedInt64Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedFloat32Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedFloat64Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedStringArray": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedVector2Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedVector3Array": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"PackedColorArray": 'QuickJSBuiltinBinder::new_object_from(ctx, ${arg})',
	"Variant": 'QuickJSBinder::variant_to_var(ctx, ${arg})',
}

def apply_pattern(template, values):
	for key in values:
		template = template.replace( '${' + key + '}', values[key])
	return template


def generate_constructor(cls):
	TemplateConstructorName = '${class}_constructor'
	TemplateConstructorDeclare = 'static JSValue ${class}_constructor(JSContext *ctx, JSValueConst new_target, int argc, JSValueConst *argv);\n'
	TemplateConstructor = '''
static JSValue ${func}(JSContext *ctx, JSValueConst new_target, int argc, JSValueConst *argv) {
	${class} tmp;
	${initializer}
	JSValue proto = JS_GetProperty(ctx, new_target, QuickJSBinder::JS_ATOM_prototype);
	JSValue obj = JS_NewObjectProtoClass(ctx, proto, QuickJSBinder::get_context_binder(ctx)->get_origin_class_id());
	QuickJSBuiltinBinder::bind_builtin_object(ctx, obj, ${type}, &tmp);
	JS_FreeValue(ctx, proto);
	return obj;
	// return QuickJSBuiltinBinder::create_builtin_value(ctx, ${type}, &tmp);
}
'''
	TemplateSimplePackedArrays = '''
	if (argc == 1) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!JS_IsArray(ctx, argv[0]), (JS_ThrowTypeError(ctx, "Array expected for argument #0 of ${class}(from)")));
#endif
		Variant arr = QuickJSBinder::var_to_variant(ctx, argv[0]);
		tmp.operator=(arr);
	}
	'''
	TemplatePackedArrays = '''
	if (argc == 1) {
		if (JS_IsArray(ctx, argv[0])) {
			Variant arr = QuickJSBinder::var_to_variant(ctx, argv[0]);
			tmp.operator=(arr);
		} else if (JS_IsArrayBuffer(argv[0])) {
			size_t size;
			uint8_t *buffer = JS_GetArrayBuffer(ctx, &size, argv[0]);
			if (size) {
				if (size % sizeof(${element}) != 0) {
					ERR_PRINT("Length of the ArrayBuffer does not match for ${class}");
				}
				tmp.resize(size / sizeof(${element}));
				memcpy(&tmp.write, buffer, size / sizeof(${element}) * sizeof(${element}));
			}
		} else if (JS_IsDataView(argv[0])) {
			JSValue byte_length = JS_GetPropertyStr(ctx, argv[0], "byteLength");
			uint64_t length = QuickJSBinder::js_to_uint64(ctx, byte_length);
			JS_FreeValue(ctx, byte_length);

			JSValue byte_offset = JS_GetPropertyStr(ctx, argv[0], "byteOffset");
			uint64_t offset = QuickJSBinder::js_to_uint64(ctx, byte_offset);
			JS_FreeValue(ctx, byte_offset);

			size_t size;
			JSValue arraybuffer = JS_GetPropertyStr(ctx, argv[0], "buffer");
			uint8_t *buffer = JS_GetArrayBuffer(ctx, &size, arraybuffer);
			JS_FreeValue(ctx, arraybuffer);
			if (length) {
				tmp.resize(length / sizeof(${element}));
				memcpy(&tmp.write, buffer + offset, length / sizeof(${element}) * sizeof(${element}));
			}
		} else {
#ifdef DEBUG_METHODS_ENABLED
			ERR_FAIL_COND_V(false, (JS_ThrowTypeError(ctx, "Array or ArrayBuffer expected for argument #0 of ${class}(from)")));
#endif
		}
	}
	'''
	ConstructorInitializers = {
		"Vector2": '''
	if (argc == 2) {
		tmp.x = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.y = QuickJSBinder::js_to_number(ctx, argv[1]);
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::VECTOR2) {
				tmp = *bind->getVector2();
			}
		} else {
			tmp.x = QuickJSBinder::js_to_number(ctx, argv[0]);
			tmp.y = tmp.x;
		}
	}
''',
		"Vector3": '''
	if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::VECTOR3)
				tmp = *bind->getVector3();
		} else {
			tmp.x = QuickJSBinder::js_to_number(ctx, argv[0]);
			tmp.z = tmp.y = tmp.x;
		}
	} else if (argc == 3) {
		tmp.x = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.y = QuickJSBinder::js_to_number(ctx, argv[1]);
		tmp.z = QuickJSBinder::js_to_number(ctx, argv[2]);
	}
''',
		"Color": '''
	if (argc >= 3) {
		tmp.r = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.g = QuickJSBinder::js_to_number(ctx, argv[1]);
		tmp.b = QuickJSBinder::js_to_number(ctx, argv[2]);
		tmp.a = (argc >= 4) ? QuickJSBinder::js_to_number(ctx, argv[3]) : 1.0f;
	} else if (argc == 1) {
		if (JS_IsNumber(argv[0])) {
			tmp = Color::hex(QuickJSBinder::js_to_uint(ctx, argv[0]));
		} else if (JS_IsString(argv[0])) {
			tmp = Color::html(QuickJSBinder::js_to_string(ctx, argv[0]));
		} else if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::COLOR) {
				tmp = *bind->getColor();
			}
		}
	}
''',
		"Rect2": '''
	if (argc == 4) {
		tmp.position.x = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.position.y = QuickJSBinder::js_to_number(ctx, argv[1]);
		tmp.size.x = QuickJSBinder::js_to_number(ctx, argv[2]);
		tmp.size.y = QuickJSBinder::js_to_number(ctx, argv[3]);
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[0]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 0 of Rect2(position, size)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[1]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 1 of Rect2(position, size)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		tmp.position = *param0->getVector2();
		tmp.size = *param1->getVector2();
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::RECT2)
				tmp = *bind->getRect2();
		}
	}
''',
		"AABB": '''
	if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of AABB(position, size)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[1]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 1 of AABB(position, size)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		tmp.position = *param0->getVector3();
		tmp.size = *param1->getVector3();
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::AABB)
				tmp = *bind->getAABB();
		}
	}
''',
		"Plane": '''
	if (argc == 4) {
		tmp.normal.x = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.normal.y = QuickJSBinder::js_to_number(ctx, argv[1]);
		tmp.normal.z = QuickJSBinder::js_to_number(ctx, argv[2]);
		tmp.d = QuickJSBinder::js_to_number(ctx, argv[3]);
	} else if (argc == 3) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Plane(v1, v2, v3)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[1]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 1 of Plane(v1, v2, v3)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[2]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 2 of Plane(v1, v2, v3)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		ECMAScriptGCHandler *param2 = BINDING_DATA_FROM_JS(ctx, argv[2]);
		tmp = Plane(*param0->getVector3(), *param1->getVector3(), *param2->getVector3());
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Plane(normal, d)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		tmp = Plane(*param0->getVector3(), QuickJSBinder::js_to_number(ctx, argv[1]));
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::PLANE)
				tmp = *bind->getPlane();
		}
	}
''',
		"Quaternion": '''
	if (argc == 4) {
		tmp.x = QuickJSBinder::js_to_number(ctx, argv[0]);
		tmp.y = QuickJSBinder::js_to_number(ctx, argv[1]);
		tmp.z = QuickJSBinder::js_to_number(ctx, argv[2]);
		tmp.w = QuickJSBinder::js_to_number(ctx, argv[3]);
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Quaternion(axis, angle)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		tmp = Quaternion(*param0->getVector3(), QuickJSBinder::js_to_number(ctx, argv[1]));
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::QUATERNION) {
				tmp = *bind->getQuaternion();
			} else if (bind->type == Variant::BASIS) {
				tmp = *bind->getBasis();
			} else if (bind->type == Variant::VECTOR3) {
				tmp = *bind->getVector3();
			}
		}
	}
''',
		"Transform2D": '''
	if (argc == 3) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[0]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 0 of Transform2D(x_axis, y_axis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[1]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 1 of Transform2D(x_axis, y_axis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[2]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 2 of Transform2D(x_axis, y_axis, origin)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		ECMAScriptGCHandler *param2 = BINDING_DATA_FROM_JS(ctx, argv[2]);
		tmp.elements[0].operator=(*param0->getVector2());
		tmp.elements[1].operator=(*param1->getVector2());
		tmp.elements[2].operator=(*param2->getVector2());
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR2, argv[1]), (JS_ThrowTypeError(ctx, "Vector2 expected for argument 1 of Transform2D(rotation, position)")));
#endif
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		tmp.set_origin(*param1->getVector2());
		tmp.set_rotation(QuickJSBinder::js_to_number(ctx, argv[0]));
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::TRANSFORM2D)
				tmp = *bind->getTransform2D();
			else if (Variant::can_convert(bind->type, Variant::TRANSFORM2D)) {
				tmp = bind->get_value();
			}
		}
	}
''',
		"Basis": '''
	if (argc == 3) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Basis(x_axis, y_axis, z_axis)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[1]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 1 of Basis(x_axis, y_axis, z_axis)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[2]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 2 of Basis(x_axis, y_axis, z_axis)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		ECMAScriptGCHandler *param2 = BINDING_DATA_FROM_JS(ctx, argv[2]);
		tmp.elements[0].operator=(*param0->getVector3());
		tmp.elements[1].operator=(*param1->getVector3());
		tmp.elements[2].operator=(*param2->getVector3());
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Basis(axis, phi)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		tmp.set_axis_angle(*param0->getVector3(), QuickJSBinder::js_to_number(ctx, argv[1]));
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::VECTOR3) {
				tmp.set_euler(*bind->getVector3());
			} else if (bind->type == Variant::QUATERNION) {
				tmp.set_quaternion(*bind->getQuaternion());
			} else if (bind->type == Variant::BASIS) {
				tmp.operator=(*bind->getBasis());
			}
		}
	}
''',
		"Transform3D": '''
	if (argc == 4) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[0]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 0 of Transform3D(x_axis, y_axis, z_axis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[1]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 1 of Transform3D(x_axis, y_axis, z_axis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[2]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 2 of Transform3D(x_axis, y_axis, z_axis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[3]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 3 of Transform3D(x_axis, y_axis, z_axis, origin)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		ECMAScriptGCHandler *param2 = BINDING_DATA_FROM_JS(ctx, argv[2]);
		ECMAScriptGCHandler *param3 = BINDING_DATA_FROM_JS(ctx, argv[3]);

		tmp.basis.elements[0].operator=(*param0->getVector3());
		tmp.basis.elements[1].operator=(*param1->getVector3());
		tmp.basis.elements[2].operator=(*param2->getVector3());
		tmp.origin.operator=(*param3->getVector3());
	} else if (argc == 2) {
#ifdef DEBUG_METHODS_ENABLED
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::BASIS, argv[0]), (JS_ThrowTypeError(ctx, "Basis expected for argument 0 of Transform3D(basis, origin)")));
		ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, Variant::VECTOR3, argv[1]), (JS_ThrowTypeError(ctx, "Vector3 expected for argument 1 of Transform3D(basis, origin)")));
#endif
		ECMAScriptGCHandler *param0 = BINDING_DATA_FROM_JS(ctx, argv[0]);
		ECMAScriptGCHandler *param1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
		tmp.basis.operator=(*param0->getBasis());
		tmp.origin.operator=(*param1->getVector3());
	} else if (argc == 1) {
		if (ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0])) {
			if (bind->type == Variant::TRANSFORM3D) {
				tmp.operator=(*bind->getTransform3D());
			} else if (Variant::can_convert(bind->type, Variant::TRANSFORM3D)) {
				tmp.operator=(bind->get_value());
			}
		}
	}
''',
		"PackedByteArray": apply_pattern(TemplatePackedArrays, {"class": "PackedByteArray", "type": "Variant::PACKED_BYTE_ARRAY", "element": "uint8_t"}),
		"PackedInt32Array": apply_pattern(TemplatePackedArrays, {"class": "PackedInt32Array", "type": "Variant::PACKED_INT32_ARRAY", "element": "int"}),
		"PackedFloat32Array": apply_pattern(TemplatePackedArrays, {"class": "PackedFloat32Array", "type": "Variant::PACKED_FLOAT32_ARRAY", "element": "real_t"}),
		"PackedVector2Array": apply_pattern(TemplatePackedArrays, {"class": "PackedVector2Array", "type": "Variant::PACKED_VECTOR2_ARRAY", "element": "Vector2"}),
		"PackedVector3Array": apply_pattern(TemplatePackedArrays, {"class": "PackedVector3Array", "type": "Variant::PACKED_VECTOR3_ARRAY", "element": "Vector3"}),
		"PackedColorArray": apply_pattern(TemplatePackedArrays, {"class": "PackedColorArray", "type": "Variant::PACKED_COLOR_ARRAY", "element": "Color"}),
		"PackedStringArray": apply_pattern(TemplateSimplePackedArrays,{"class": "PackedStringArray", "type": "Variant::PACKED_STRING_ARRAY", "element": "String"}),
	}
	class_name = cls['name']
	constructor_name = apply_pattern(TemplateConstructorName, {"class": class_name})
	constructor_declare = apply_pattern(TemplateConstructorDeclare, {"class": class_name})
	
	initializer = ''
	if class_name in ConstructorInitializers:
		initializer = ConstructorInitializers[class_name]
	consturctor = apply_pattern(TemplateConstructor, {
		'class': class_name,
		'type': VariantTypes[class_name],
		'func': constructor_name,
		'initializer': initializer
	})
	return constructor_name, constructor_declare, consturctor

def generate_property_bindings(cls):
	class_name = cls['name']
	TemplateDeclar = 'static void bind_${class}_properties(JSContext *ctx);\n'
	TemplateBind = '\tbind_${class}_properties(ctx);\n'
	def generate_members(cls):
		Template = '''
	JSCFunctionMagic *getter = [](JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv, int magic) -> JSValue {
		ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, this_val);
		const ${class} *ptr = bind->get${class}();
		switch (magic) {\
${getters}
		}
		return JS_UNDEFINED;
	};
	
	JSCFunctionMagic *setter = [](JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv, int magic) -> JSValue {
		ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, this_val);
		${class} *ptr = bind->get${class}();\
${validation}
		switch (magic) {\
${setters}
		}
		return JS_DupValue(ctx, argv[0]);
	};
${bindings}
		'''
		TemplateGetterItem = '''
			case ${index}:
				return ${value};'''
		TemplateSetterItem = '''
			case ${index}:
#ifdef DEBUG_METHODS_ENABLED
				ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, ${type}, argv[0]), (JS_ThrowTypeError(ctx, "${type_name} expected for ${class}.${name}")));
#endif
				ptr->${native} = ${value};
				break;'''
		TemplateItemBinding = '\tbinder->get_builtin_binder().register_property(${type}, "${name}", getter, setter, ${index});\n'
		getters = ''
		setters = ''
		bindings = ''
		for i in range(len(cls['properties'])):
			p = cls['properties'][i]
			type = p['type']
			name = p['name']
			native_name = p['native']
			getters += apply_pattern(TemplateGetterItem, {
				'index': str(i),
				'value': apply_pattern(GodotToJSTemplates[type], { 'arg': apply_pattern('ptr->${native}', {'native': native_name}) })
			})
			setters += apply_pattern(TemplateSetterItem, {
				'index': str(i),
				'name': name,
				'native': native_name,
				'type': VariantTypes[type],
				'type_name': type,
				'class': class_name,
				'value': apply_pattern(JSToGodotTemplates[type], {'arg': 'argv[0]'})
			})
			bindings += apply_pattern(TemplateItemBinding, {'index': str(i), 'name': name, 'type': VariantTypes[class_name]})
		return apply_pattern(Template, {
			'class': class_name,
			'getters': getters,
			'setters': setters,
			'bindings': bindings,
			'validation': ''
		})
	
	def generate_methods(cls):
		TemplateMethod = '''
	binder->get_builtin_binder().register_method(
		${type},
		"${name}",
		[](JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv) {
			ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, this_val);
			${class} *ptr = bind->get${class}();\
${arg_declares}
			${call}
			return ${return};
		},
		${argc});'''
		TemplateArgDeclare = '''
#ifdef DEBUG_METHODS_ENABLED
			ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, ${type}, argv[${index}]), (JS_ThrowTypeError(ctx, "${type_name} expected for argument ${index} of ${class}.${name}")));
#endif
			const ${godot_type} &arg${index} = ${arg};
'''
		TemplateReturnValue = '${godot_type} ret = '
		bindings = ''
		for m in cls['methods']:
			args = ''
			arg_declares = ''
			for i in range(len(m['arguments'])):
				arg = m['arguments'][i]
				arg_type = arg['type']
				templateArgDeclare = TemplateArgDeclare if VariantTypes[arg_type] != "Variant" else '''
			const ${godot_type} &arg${index} = ${arg};
'''
				arg_declares += apply_pattern(templateArgDeclare, {
					'index': str(i),
					'type': VariantTypes[arg_type],
					'type_name': arg_type,
					'class': class_name,
					'name': m['name'],
					'arg': apply_pattern(JSToGodotTemplates[arg_type], {'arg': 'argv[' + str(i) +']'}),
					'godot_type': GodotTypeNames[arg_type],
				})
				if i > 0: args += ', '
				args += 'arg' + str(i)

			CallTemplate = ''
			native_method = m['native_method']
			if m.get('variant_call'):
				if native_method.startswith('to_int'): 
					native_method = native_method.replace('to_int', 'decode_s')
				if native_method.startswith('to_float32'): 
					native_method = native_method.replace('to_float32', 'decode_float')
				if native_method.startswith('to_float64'): 
					native_method = native_method.replace('to_float64', 'decode_double')
				CallTemplate = ('' if m['return'] == 'void' else (apply_pattern(TemplateReturnValue, {"godot_type": GodotTypeNames[m['return']]}))) + 'Variant(ptr).call(\"${native_method}\"' + (', ${args});' if args else ');')
			elif m['name'] == 'grow_side':
				args = args.replace("arg0", "Side(arg0)")
				CallTemplate = ('' if m['return'] == 'void' else (apply_pattern(TemplateReturnValue, {"godot_type": GodotTypeNames[m['return']]}))) + 'ptr->${native_method}(${args});'
			else:
				CallTemplate = ('' if m['return'] == 'void' else (apply_pattern(TemplateReturnValue, {"godot_type": GodotTypeNames[m['return']]}))) + 'ptr->${native_method}(${args});'
			call = apply_pattern(CallTemplate, {'native_method': native_method, 'args': args})
			bindings += apply_pattern(TemplateMethod, {
				"class": class_name,
				"type": VariantTypes[class_name],
				"name": m['name'],
				"call": call,
				"arg_declares": arg_declares,
				"argc": str(len(m['arguments'])),
				"return": 'JS_UNDEFINED' if m['return'] == 'void' else apply_pattern(GodotToJSTemplates[m['return']], {'arg': 'ret'}),
			})
		return bindings
		
	def generate_constants(cls):
		ConstTemplate = '\tbinder->get_builtin_binder().register_constant(${type}, "${name}", ${value});\n'
		bindings = ''
		for c in cls['constants']:
			bindings += apply_pattern(ConstTemplate, {
				"name": c['name'],
				"type": VariantTypes[class_name],
				"value": c['value']
			})
		return bindings
	
	def genertate_operators(cls):
		OperatorMap = {
			'Variant::OP_ADD': '+',
			'Variant::OP_SUBTRACT': '-',
			'Variant::OP_MULTIPLY': '*',
			'Variant::OP_DIVIDE': '/',
			'Variant::OP_EQUAL': '==',
			'Variant::OP_LESS': '<'
		}
		TargetDeclareTemplate = '''
#ifdef DEBUG_METHODS_ENABLED
			ERR_FAIL_COND_V(!QuickJSBinder::validate_type(ctx, ${type}, argv[1]), (JS_ThrowTypeError(ctx, "${target_class} expected for ${class}.${operator}")));
#endif
			ECMAScriptGCHandler *bind1 = BINDING_DATA_FROM_JS(ctx, argv[1]);
			${target_class} *target = bind1->get${target_class}();\
'''
		OperatorTemplate = '''
	JS_SetPropertyStr(ctx, base_operators, "${js_op}",
		JS_NewCFunction(ctx, [](JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv) {
			ECMAScriptGCHandler *bind = BINDING_DATA_FROM_JS(ctx, argv[0]);
			${class} *ptr = bind->get${class}();\
${target_declare}
			${call}
			return ${return};
		},
		"${name}",
		${argc})
	);
	'''
		TemplateReturnValue = '${godot_type} ret = '
		bindings = '''\
	Vector<JSValue> operators;
	JSValue base_operators = JS_NewObject(ctx);
'''
		for o in cls['operators']:
			op = o['native_method']
			assign = o.get('assign')
			if op in OperatorMap:
				argc = len(o['arguments']) + 1
				js_op = OperatorMap[op] + ('=' if assign else '')
				if argc <= 1:
					if op in ['operator-']:
						js_op = 'neg'
					
				args = ''
				target_declare = ''
				if argc > 1:
					arg_class = o['arguments'][0]['type']
					target_declare = apply_pattern(TargetDeclareTemplate, {
						'target_class': arg_class,
						'type': VariantTypes[arg_class],
						'class': class_name,
						'operator': o['native_method'],
					})
					args = '*target'
				
				EvaluateOperator = ('*ptr = ' if assign else '') + 'Variant::evaluate(${op}, Variant(*ptr), Variant(${args}));'

				if o['return'] == 'void':
					CallTemplate = ''
				elif o['return'] == 'this':
					CallTemplate = apply_pattern(TemplateReturnValue, {'godot_type': GodotTypeNames[cls['name']]}) + EvaluateOperator
				else:
					CallTemplate = apply_pattern(TemplateReturnValue, {'godot_type': GodotTypeNames[o['return']] }) + EvaluateOperator

				call = apply_pattern(CallTemplate, {'op': op, 'args': args})

				if o['return'] == 'void':
					return_str = 'JS_UNDEFINED'
				elif o['return'] == 'this':
					return_str = apply_pattern(GodotToJSTemplates[cls['name']], {'arg': '*ptr'})
				else:
					return_str = apply_pattern(GodotToJSTemplates[o['return']], {'arg': 'ret'})

				bindings += apply_pattern(OperatorTemplate, {
					'type': VariantTypes[class_name],
					'class': class_name,
					'js_op': js_op,
					'call': call,
					'name': o['name'],
					'target_declare': target_declare,
					"return": return_str,
					'argc': str(argc)
				})
		bindings += apply_pattern('''
	operators.push_back(base_operators);
	binder->get_builtin_binder().get_cross_type_operators(${type}, operators);
	binder->get_builtin_binder().register_operators(${type}, operators);
''', {'type': VariantTypes[class_name]})
		return bindings
	
	TemplateBindDefine = '''
static void bind_${class}_properties(JSContext *ctx) {
	QuickJSBinder *binder = QuickJSBinder::get_context_binder(ctx);
${members}
${operators}
${constants}
${methods}
}
'''
	class_name = cls['name']
	property_declare = apply_pattern(TemplateDeclar, {"class": class_name})
	property_defines = apply_pattern(TemplateBindDefine, {
		"class": class_name,
		"members": generate_members(cls) if len(cls['properties']) else '',
		"methods": generate_methods(cls),
		"constants": generate_constants(cls),
		"operators": genertate_operators(cls),
	})
	property_bind = apply_pattern(TemplateBind, {"class": class_name})
	return property_declare, property_defines, property_bind


def generate_class_bind_action(cls, constructor):
	Template = '\tregister_builtin_class(${type}, "${class}", ${constructor}, ${argc});\n'
	return apply_pattern(Template, {
		'class': cls['name'],
		'constructor': constructor,
		'type': VariantTypes[cls['name']],
		'argc': str(cls['constructor_argc'])
	})



def generate_builtin_bindings():
	Template = '''\
#include "core/variant/variant.h"
#include "quickjs_binder.h"
#include "quickjs_builtin_binder.h"

#ifndef inf
#define inf INFINITY
#endif

${declarations}

void QuickJSBuiltinBinder::bind_builtin_classes_gen() {

${bindings}
}

${definitions}
'''
	
	declarations = ''
	definitions = ''
	bindings = ''
	for cls in API:
		constructor_name, constructor_declare, consturctor = generate_constructor(cls)
		declarations += constructor_declare
		definitions += consturctor
		bindings += generate_class_bind_action(cls, constructor_name)
		
		property_declare, property_defines, property_bind= generate_property_bindings(cls)
		declarations += property_declare
		definitions += property_defines
		bindings += property_bind
	
	output = apply_pattern(Template, {
		'declarations': declarations,
		'bindings': bindings,
		'definitions': definitions,
	})
	file = open(OUTPUT_FILE, 'w')
	file.write(output)

if __name__ == "__main__":
	generate_builtin_bindings()
