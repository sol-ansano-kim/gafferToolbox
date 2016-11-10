import arnold
import GafferArnold
import os
import IECore


class ArnoldFunctions:
    @staticmethod
    def AiBegin():
        arnold.AiBegin()
        arnold.AiLoadPlugins(os.environ["ARNOLD_PLUGIN_PATH"])

    @staticmethod
    def ReadAss(ass_file):
        arnold.AiASSLoad(ass_file)

    @staticmethod
    def AiEnd():
        arnold.AiEnd()

    @staticmethod
    def ScratchNodes(node_mask, exclude_list=[]):
        return_dict = {}

        # node iterator
        node_it = arnold.AiUniverseGetNodeIterator(node_mask)
        while (not arnold.AiNodeIteratorFinished(node_it)):
            node = arnold.AiNodeIteratorGetNext(node_it)
            entry = arnold.AiNodeGetNodeEntry(node)
            node_name = arnold.AiNodeGetStr(node, "name")
            entry_name = arnold.AiNodeEntryGetName(entry)
            dict_name = node_name.replace(":", "_")

            if entry_name in exclude_list:
                continue

            params = {}
            return_dict[dict_name] = {"params": params, "type": entry_name}

            # parameter iterator
            param_it = arnold.AiNodeEntryGetParamIterator(entry)
            while (not arnold.AiParamIteratorFinished(param_it)):
                try:
                    param_entry = arnold.AiParamIteratorGetNext(param_it)
                    param_name = arnold.AiParamGetName(param_entry)
                    param_type = arnold.AiParamGetType(param_entry)
                    (param_link, parm_value) = ArnoldFunctions.ParamValue(node, param_name, param_type, param_entry)

                    params[param_name] = {"link": param_link, "value": parm_value, "type": arnold.AiParamGetTypeName(param_type)}

                except Exception as e:
                    print "[ArnoldFunctions.ScratchNodes] Warning parameter reading : %s" % e

            arnold.AiParamIteratorDestroy(param_it)

        arnold.AiNodeIteratorDestroy(node_it)

        return return_dict

    @staticmethod
    def ParamValue(node, param_name, param_type, param_entry):
        value = None
        linked_name = None
        if arnold.AiNodeIsLinked(node, param_name):
            linked_node = arnold.AiNodeGetLink(node, param_name)
            linked_name = arnold.AiNodeGetName(linked_node).replace(":", "_")

        else:
            if arnold.AI_TYPE_BYTE == param_type:
                value = arnold.AiNodeGetByte(node, param_name)

            elif arnold.AI_TYPE_INT == param_type:
                value = arnold.AiNodeGetInt(node, param_name)

            elif arnold.AI_TYPE_UINT == param_type:
                value = arnold.AiNodeGetUInt(node, param_name)

            elif arnold.AI_TYPE_BOOLEAN == param_type:
                value = arnold.AiNodeGetBool(node, param_name)

            elif arnold.AI_TYPE_FLOAT == param_type:
                value = arnold.AiNodeGetFlt(node, param_name)

            elif arnold.AI_TYPE_RGB == param_type:
                rgb = arnold.AiNodeGetRGB(node, param_name)
                value = IECore.Color3f(rgb.r, rgb.g, rgb.b)

            elif arnold.AI_TYPE_RGBA == param_type:
                rgba = arnold.AiNodeGetRGBA(node, param_name)
                value = IECore.Color4f(rgba.r, rgba.g, rgba.b, rgba.a)

            elif arnold.AI_TYPE_VECTOR == param_type:
                vec = arnold.AiNodeGetVec(node, param_name)
                value = IECore.V3f(vec.x, vec.y, vec.z)

            elif arnold.AI_TYPE_POINT == param_type:
                pnt = arnold.AiNodeGetPnt(node, param_name)
                value = IECore.V3f(pnt.x, pnt.y, pnt.z)

            elif arnold.AI_TYPE_ENUM == param_type:
                enm = arnold.AiParamGetEnum(param_entry)
                value = arnold.AiEnumGetString(enm, arnold.AiNodeGetInt(node, param_name))

            elif arnold.AI_TYPE_STRING == param_type:
                value = arnold.AiNodeGetStr(node, param_name)

            elif arnold.AI_TYPE_NODE == param_type:
                value = None

            elif arnold.AI_TYPE_POINT2 == param_type:
                pnt2 = arnold.AiNodeGetPnt2(node, param_name)
                value = IECore.V2f(pnt2.x, pnt2.y)

            elif arnold.AI_TYPE_ARRAY == param_type:
                arry = arnold.AiNodeGetArray(node, param_name)

                if arry.contents.type == arnold.AI_TYPE_INT:
                    value = IECore.IntVectorData()
                    for i in range(arry.contents.nelements):
                        value.append(arnold.AiArrayGetInt(arry, i))
                elif arry.contents.type == arnold.AI_TYPE_UINT:
                    value = IECore.IntVectorData()
                    for i in range(arry.contents.nelements):
                        value.append(arnold.AiArrayGetUInt(arry, i))
                elif arry.contents.type == arnold.AI_TYPE_BYTE:
                    value = IECore.IntVectorData()
                    for i in range(arry.contents.nelements):
                        value.append(arnold.AiArrayGetByte(arry, i))

                elif arry.contents.type == arnold.AI_TYPE_FLOAT:
                    value = IECore.FloatVectorData()
                    for i in range(arry.contents.nelements):
                        value.append(arnold.AiArrayGetFlt(arry, i))

                elif arry.contents.type == arnold.AI_TYPE_BOOLEAN:
                    value = IECore.BoolVectorData()
                    for i in range(arry.contents.nelements):
                        value.append(arnold.AiArrayGetBool(arry, i))

                elif arry.contents.type == arnold.AI_TYPE_RGB:
                    value = IECore.V3fVectorData()
                    for i in range(arry.contents.nelements):
                        rgb = arnold.AiArrayGetRGB(arry, i)
                        value.append(IECore.V3f(rgb.r, rgb.g, rgb.b))
                elif arry.contents.type == arnold.AI_TYPE_RGBA:
                    value = IECore.V3fVectorData()
                    for i in range(arry.contents.nelements):
                        rgba = arnold.AiArrayGetRGBA(arry, i)
                        value.append(IECore.V3f(rgba.r, rgba.g, rgba.b))
                elif arry.contents.type == arnold.AI_TYPE_VECTOR:
                    value = IECore.V3fVectorData()
                    for i in range(arry.contents.nelements):
                        vec = arnold.AiArrayGetVec(arry, i)
                        value.append(IECore.V3f(vec.r, vec.g, vec.b))
                elif arry.contents.type == arnold.AI_TYPE_POINT:
                    value = IECore.V3fVectorData()
                    for i in range(arry.contents.nelements):
                        pnt = arnold.AiArrayGetPnt(arry, i)
                        value.append(IECore.V3f(pnt.r, pnt.g, pnt.b))

                elif arry.contents.type == arnold.AI_TYPE_STRING:
                    value = IECore.StringVectorData()
                    for i in range(arry.contents.nelements):
                        txt = arnold.AiArrayGetStr(arry, i)
                        value.append(txt)

                else:
                    value = None

            else:
                # todo : AI_TYPE_POINTER, AI_TYPE_MATRIX, AI_TYPE_UNDEFINED, AI_TYPE_NONE
                print "[CreateShaderFromASS] Not supported type : %s - %s %s" % (arnold.AiParamGetTypeName(param_type), arnold.AiNodeGetStr(node, "name"), param_name)
                value = None

        return (linked_name, value)


class GafferFunctions:
    @staticmethod
    def SetUniqueName(script, node, name):
        node_names = script.keys()
        check_name = name
        index = 0
        while (check_name in node_names):
            index += 1
            check_name = "%s_%d" % (name, index)

        node.setName(check_name)


def CreateShaderFromASS(ass_file, script=None, exclude_list=["utility"], hook_functions={}):
    shaders = {}
    shader_dict = {}

    # ASS read
    ArnoldFunctions.AiBegin()
    ArnoldFunctions.ReadAss(ass_file)
    try:
        shader_dict = ArnoldFunctions.ScratchNodes(arnold.AI_NODE_SHADER, exclude_list)
    except Exception as e:
        print "[CreateShaderFromASS] Error : ArnoldFunctions.ScratchNodes failed."

    ArnoldFunctions.AiEnd()

    # create shaders
    for shader_name, shader_value in shader_dict.items():
        shader_type = shader_value.get("type")
        shader_node = GafferArnold.ArnoldShader(shader_type)
        shader_node.loadShader(shader_type, keepExistingValues=True)

        shader_node.setName(shader_name)

        if script:
            GafferFunctions.SetUniqueName(script, shader_node, shader_name)
            script.addChild(shader_node)

        shaders[shader_name] = shader_node

    # set values
    for shader_name, shader_value in shader_dict.items():
        shader_node = shaders.get(shader_name)
        shader_type = shader_value.get("type")
        existing_parms = shader_node["parameters"].keys()
        for param_name, parm_data in shader_value["params"].items():
            if param_name == "name":
                continue

            if not param_name in existing_parms:
                continue

            value = parm_data.get("value")
            linked = parm_data.get("link")
            param_type = parm_data.get("type")

            if not linked is None:
                linked_node = shaders.get(linked)

                if linked_node and "out" in linked_node.keys():
                    shader_node["parameters"][param_name].setInput(linked_node["out"])
                else:
                    print "[CreateShaderFromASS] Warning : cannot find link node : %s" % linked_node

            elif not value is None:
                shader_node["parameters"][param_name].setValue(value)

        hook = hook_functions.get(shader_type)
        if hook:
            hook(shader_node)

    return shaders
