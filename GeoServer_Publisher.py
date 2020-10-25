#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 23:31
# @Author  : WuYan
# @FileName: GeoServer_Publisher.py
# @Software: PyCharm
# @EMail   : wuyansec@qq.com

import requests
import xml.dom.minidom, xml.etree.ElementTree
import xmltodict
import ast
from bs4 import BeautifulSoup
import re
import sys
import time

USERNAME = "admin"
PASSWORD = "geoserver"

SERVER_NAME = "http://localhost:8080"
HEADERS = {'Accept': 'application/xml', 'Content-type': 'text/xml'}

# 验证账号密码及地址是否正确
def VerifyInfo():
    payload = "{  \"name\": \"nxxx\"}"

    # sent request to operate geoserver
    folderURL = "/geoserver/rest/workspaces/cite"
    headers = {"accept":"application/json" ,"content-type":"application/json"}

    try:
        # 请求修改默认工作区间：405 禁止修改，密码正确；401: 未授权，密码错误
        response = requests.post(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)
        print(response.status_code)
        if (response.status_code == 405):
            return True
        else:
            return False
    except:
        return False


# 创建工作区
def CreateWorkSpace(spaceName):
    payload = "<workspace><name>{name}</name></workspace>"
    payload = payload.format(name=spaceName)

    # sent request to operate geoserver
    folderURL = "/geoserver/rest/workspaces"

    response = requests.post(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=HEADERS, data=payload)

    # 操作结果
    if response.status_code == 201:
        print("Created")
        return spaceName
    else:
        print("Error in create work space. Use default space: cite")
        print(response.text)
        return "cite"


# 添加TIFF类型数据图层
def CreateCoverage(workspace, coveragename, filename):
    # url for request geoserver
    folderURL = "/geoserver/rest/workspaces/" + workspace + "/coveragestores/" + coveragename + "/file.geotiff"
    headers = {"Content-type": "image/tiff"}

    # 读取二进制tiff文件
    f = open(filename, 'rb')
    payload = f.read()
    response = requests.put(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)

    if(response.status_code == 201):
        print("create coverage: " + workspace + ":" + coveragename + " success!")
    elif(response.status_code == 200):
        print("update coverage: " + workspace + ":" + coveragename + " success!")
    else:
        print("error in createCoverage: " + str(response))
        raise Exception(response.text)


# 修改图层默认属性
def EditCacheLayer_GridSets(workspace,layername,girdsetname):
    # 获取当前Cache Layer的属性XML
    if workspace != "":
        folderURL = "/geoserver/gwc/rest/layers/" + workspace + ":" + layername
    else:
        folderURL = "/geoserver/gwc/rest/layers/" + layername
    headers = {"accept": "application/xml", "content-type": "application/json"}
    res = requests.get(SERVER_NAME + folderURL,auth=(USERNAME, PASSWORD), headers=headers)

    if(res.status_code == 200 ):
        print("get cache layer: "+workspace +":"+ layername+" success!")
    elif(res.status_code == 404):
        print("unknow layer: "+workspace +":"+ layername+"!")
        sys.exit(0)
    else:
        print("error in get cache xml of layer:"+workspace +":"+ layername+"!  " + str(res))
        sys.exit(0)

    ### 解析返回的切片图层的XML
    doc = xml.dom.minidom.parseString(res.text)
    gridsets = doc.getElementsByTagName("gridSubsets")[0]
    # 删除预设的切片方案
    for item in gridsets.getElementsByTagName("gridSubset"):
        gridsets.removeChild(item)
    # 添加新方案
    node_grids_sub = doc.createElement("gridSubset")
    node_grids_sub_name = doc.createElement("gridSetName")
    node_grids_sub_name.appendChild(doc.createTextNode(girdsetname))
    node_grids_sub.appendChild(node_grids_sub_name)
    gridsets.appendChild(node_grids_sub)

    # 修改Cache Layer的属性
    payload = doc.toxml(encoding="UTF-8")
    headers = {"accept": "application/json" ,"content-type": "application/xml"}
    response = requests.put(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)

    # 返回结果：操作是否成功
    if (response.status_code == 200):
        print("The cache layer was successfully updated.")
    elif (response.status_code == 201):
        print("The cache layer was successfully created.")
    else:
        print("error in edit cache layer:" + str(response))
        sys.exit(0)


# 获取图层的bounds: [xmin,xmax,ymin,ymax]
def GetCoverageBounds(workspace, coverage):
    folderURL = "/geoserver/rest/workspaces/" + workspace + "/coverages/" + coverage
    headers = {"accept": "text/html"}
    bounds = []

    response = requests.get(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers)

    if (response.status_code == 200):
        print("begin to parse bounds: " + coverage)
        try:
            # 解析返回的结果
            soup = BeautifulSoup(response.text, 'html.parser')
            # bounds位于最后一个li标签
            lists = soup.findAll("li")
            bs = lists[len(lists) - 1].get_text()
            for i in re.findall(r"-?\d+\.?\d*", bs):
                bounds.append(float(i))
            print(coverage + ": " + str(bs))
        except Exception:
            print("error in parse bounds info: " + workspace + ":" + coverage + " bounds!")
    else:
        print(response.text)

    return bounds


# 生成缓存切片策略——GridSets
def CreateGridSet_WKID4508(gridname, workspace, coverage, resolutions_level, wkid, size):
    # 获取bounds
    bounds = GetCoverageBounds(workspace, coverage)

    # 计算图像长宽
    bounds_x = bounds[1] - bounds[0]
    bounds_y = bounds[3] - bounds[2]

    # y方向是否需要先分割(geoserver始终为true)
    yCoordinateFirst = True

    # 第一层分辨率
    res = 1.0 * bounds_y / int(size)

    resolutions = [res]

    for i in range(resolutions_level - 1):
        res = res / 2.0
        resolutions.append(res)

    # GridSet参数
    arg = {
        "name": gridname,
        "description": "none",
        "wkid": wkid,
        "bounds": [bounds[0], bounds[2], bounds[1], bounds[3]],
        "resolutions": resolutions,
        "alignTopLeft": "false",
        "metersPerUnit": 1,
        "pixelSize": 2.8E-4,
        "tileHeight": size,
        "tileWidth": size,
        "yCoordinateFirst": "true" if yCoordinateFirst else "false"
    }

    # 生成xml格式GridSet
    gridset = CreateGridSetXML(arg).toxml(encoding="UTF-8")
    #print(gridset)

    # sent request to operate geoserver
    folderURL = "/geoserver/gwc/rest/gridsets/" + gridname
    headers = {"accept": "text/html", "content-type": "application/xml"}

    response = requests.put(SERVER_NAME + folderURL, headers=headers, data=gridset, auth=(USERNAME, PASSWORD))

    # 返回结果：操作是否成功
    if (response.status_code == 200):
        print("The gridset was successfully updated.")
    elif (response.status_code == 201):
        print("The gridset was successfully created.")
    else:
        print(response.text)

    return


# 生成GridSets的XML
def CreateGridSetXML(arg):
    doc = xml.dom.minidom.Document()
    root = doc.createElement("gridSet")
    doc.appendChild(root)

    node_name = doc.createElement("name")
    node_name.appendChild(doc.createTextNode(arg["name"]))
    root.appendChild(node_name)

    node_dscrp = doc.createElement("description")
    node_dscrp.appendChild(doc.createTextNode(arg["description"]))
    root.appendChild(node_dscrp)

    node_srs = doc.createElement("srs")
    node_srs_wkid = doc.createElement("number")
    node_srs_wkid.appendChild(doc.createTextNode(str(arg["wkid"])))
    node_srs.appendChild(node_srs_wkid)
    root.appendChild(node_srs)

    node_extent = doc.createElement("extent")
    node_coords = doc.createElement("coords")
    for coord in arg["bounds"]:
        node_double = doc.createElement("double")
        node_double.appendChild(doc.createTextNode(str(coord)))
        node_coords.appendChild(node_double)
    node_extent.appendChild(node_coords)
    root.appendChild(node_extent)

    node_alignTopLeft = doc.createElement("alignTopLeft")
    node_alignTopLeft.appendChild(doc.createTextNode(str(arg["alignTopLeft"])))
    root.appendChild(node_alignTopLeft)

    node_resolutions = doc.createElement("resolutions")
    for resultion in arg["resolutions"]:
        node_res = doc.createElement("double")
        node_res.appendChild(doc.createTextNode(str(resultion)))
        node_resolutions.appendChild(node_res)
    root.appendChild(node_resolutions)

    node_metersPerUnit = doc.createElement("metersPerUnit")
    node_metersPerUnit.appendChild(doc.createTextNode(str(arg["metersPerUnit"])))
    root.appendChild(node_metersPerUnit)

    node_pixelSize = doc.createElement("pixelSize")
    node_pixelSize.appendChild(doc.createTextNode(str(arg["pixelSize"])))
    root.appendChild(node_pixelSize)

    node_scaleNames = doc.createElement("scaleNames")
    for i in range(len(arg["resolutions"])):
        node_s_name = doc.createElement("string")
        node_s_name.appendChild(doc.createTextNode(arg["name"] + ":" + str(i)))
        node_scaleNames.appendChild(node_s_name)
    root.appendChild(node_scaleNames)

    node_tileHeight = doc.createElement("tileHeight")
    node_tileHeight.appendChild(doc.createTextNode(str(arg["tileHeight"])))
    root.appendChild(node_tileHeight)

    node_tileWidth = doc.createElement("tileWidth")
    node_tileWidth.appendChild(doc.createTextNode(str(arg["tileWidth"])))
    root.appendChild(node_tileWidth)

    node_yCoordinateFirst = doc.createElement("yCoordinateFirst")
    node_yCoordinateFirst.appendChild(doc.createTextNode(str(arg["yCoordinateFirst"])))
    root.appendChild(node_yCoordinateFirst)

    return doc


# 创建切片缓存任务
def CreateSeedsTask(workspace, layer, zoomLevel, threadCount, type="reseed"):
    # 生成切片策略
    args = {
        "name": layer if workspace == "" else workspace + ":" + layer,
        "srs": "4508",
        "zoomStart": 0,
        "zoomStop": zoomLevel-1,
        "format": "image/png",
        "type": type,
        "threadCount": threadCount
    }
    cacheSchema = CreateSeedsXML(args).toxml(encoding="UTF-8")

    #print(cacheSchema)

    # sent request to operate geoserver
    if workspace != "":
        folderURL = "/geoserver/gwc/rest/seed/" + workspace + ":" + layer + ".xml"
    else:
        folderURL = "/geoserver/gwc/rest/seed/" + layer + ".xml"

    headers = {'Accept': 'application/xml', 'Content-type': 'text/xml'}

    response = requests.post(SERVER_NAME + folderURL, headers=headers, data=cacheSchema, auth=(USERNAME, PASSWORD))

    # 返回结果：操作是否成功
    if (response.status_code == 200):
        print("The Seeds Task was successfully updated.")
    else:
        print(response.text)


# 创建生成图层组的xml layers_Formate ["workspace:layer"]
def CreateLayerGroupXML(groupname, layers):
    doc = xml.dom.minidom.Document()
    root = doc.createElement("layerGroup")
    doc.appendChild(root)

    node_name = doc.createElement("name")
    node_name.appendChild(doc.createTextNode(groupname))
    root.appendChild(node_name)

    node_layers = doc.createElement("layers")
    for item in layers:
        # layer
        node_layer = doc.createElement("layer")
        node_layer.appendChild(doc.createTextNode(item))
        node_layers.appendChild(node_layer)
    root.appendChild(node_layers)

    node_styles = doc.createElement("styles")
    for item in layers:

        # style
        node_style = doc.createElement("style")
        node_style.appendChild(doc.createTextNode("raster"))
        node_styles.appendChild(node_style)
    root.appendChild(node_styles)

    return doc


# 生成用于初始化Seed任务的XML
def CreateSeedsXML(arg):
    doc = xml.dom.minidom.Document()
    root = doc.createElement("seedRequest")
    doc.appendChild(root)

    node_name = doc.createElement("name")
    node_name.appendChild(doc.createTextNode(str(arg["name"])))
    root.appendChild(node_name)

    node_srs = doc.createElement("srs")
    node_srs_num = doc.createElement("number")
    node_srs_num.appendChild(doc.createTextNode(str(arg["srs"])))
    node_srs.appendChild(node_srs_num)
    root.appendChild(node_srs)

    node_zoomStart = doc.createElement("zoomStart")
    node_zoomStart.appendChild(doc.createTextNode(str(arg["zoomStart"])))
    root.appendChild(node_zoomStart)

    node_zoomStop = doc.createElement("zoomStop")
    node_zoomStop.appendChild(doc.createTextNode(str(arg["zoomStop"])))
    root.appendChild(node_zoomStop)

    node_zoomFormat = doc.createElement("format")
    node_zoomFormat.appendChild(doc.createTextNode(str(arg["format"])))
    root.appendChild(node_zoomFormat)

    node_zoomType = doc.createElement("type")
    node_zoomType.appendChild(doc.createTextNode(str(arg["type"])))
    root.appendChild(node_zoomType)

    node_zoomThreadCount = doc.createElement("threadCount")
    node_zoomThreadCount.appendChild(doc.createTextNode(str(arg["threadCount"])))
    root.appendChild(node_zoomThreadCount)

    return doc


# 查询切片缓存状态
def HasCacheFinished():
    # sent request to operate geoserver
    folderURL = "/geoserver/gwc/rest/seed.json"
    response = requests.get(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD))

    # 所有切片任务是否完成
    finshStatus = False

    # 返回结果
    if(response.status_code != 200 ):
        print("error:" + str(response))
    else:
        try:
            res = ast.literal_eval(response.text)
            # 返回的数组结构：[tiles processed, total of tiles to process, total of remaining tiles, Task ID, Task status]
            status = ["PENDING", "RUNNING", "DONE"]
            print(res["long-array-array"])
            for task in res["long-array-array"]:
                sts = "ABORTED" if task[4] == -1 else status[task[4]]
                print("task "+str(task[3]) + " is " + sts + ": tatal " + str(task[1]) + " / finished " + str(task[0]) + " / remaining "+str(task[2]))
                if (task[4] == 2):
                    finshStatus = True
                    print("cache for task " + str(task[3]) + " finished!")
        except Exception as e:
            print("error in query seeds status: " + str(response))

    return finshStatus


# 发布一TIFF同时生成切片
def PublishGeoTIFF(workspace, layername, filepath, zoomlevel, threadCount, wkid, size):
    # 1.创建Geoserver工作区
    workspace = CreateWorkSpace(workspace)

    # 2.发布TIFF图层
    CreateCoverage(workspace, layername, filepath)

    # 3.创建图层的切片方案
    gridname = layername + "_cache"
    CreateGridSet_WKID4508(gridname, workspace, layername, zoomlevel, wkid, size)

    # 4.修改图层的切片方案
    EditCacheLayer_GridSets(workspace,layername,gridname)

    # 5.开始切片
    CreateSeedsTask(workspace,layername,zoomlevel, threadCount)

    # 6.获取切片运行状态
    while (not HasCacheFinished()):
        time.sleep(2)

    return


def trans_dict_to_xml(jsdict):
    xml = ''
    try:
        xml = xmltodict.unparse(jsdict, encoding='utf-8')
    except Exception:
        xml = xmltodict.unparse({'layerGroup': jsdict}, encoding='utf-8')
    finally:
        return xml


# 发布为图层组_Simple  layers:["workspace:layername"]
def PublishLayerGroup_S(groupname, layers):
    folderURL = "/geoserver/rest/layergroups"

    headers = {"accept": "application/xml", "content-type": "text/xml"}

    payload = CreateLayerGroupXML(groupname, layers).toxml(encoding="UTF-8")

    print(payload)

    response = requests.post(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)

    if(response.status_code == 201):
        print("success")
    else:
        print(response)


# 发布为图层组_Complicted  invalid：该方式需要的layer的URL未知
def PublishLayerGroup(workspace, layername, mode, wkid, layers, bounds):
    arg = {
      "name": layername,
      "mode": mode,
      "title": layername,
      "abstractTxt": "",
      "workspace": {
        "name": workspace
      },
      "publishables": {
        "published": layers
      },
      "styles": {
        "style": []
      },
      "bounds": {
        "minx": bounds[0],
        "maxx": bounds[1],
        "miny": bounds[2],
        "maxy": bounds[3],
        "crs": "EPSG:" + str(wkid)
      }
    }

    for i in range(len(layers)):
        arg["styles"]["style"].append({"name":"raster", "link": SERVER_NAME + "/geoserver/rest/styles/raster.xml"})


    # payload = "<workspace><name>{name}</name></workspace>"
    # payload = payload.format(name=spaceName)

    # sent request to operate geoserver
    folderURL = "/geoserver/rest/workspaces/cite/layergroups"

    headers = {"accept":"application/xml",  "content-type":"application/xml"}

    payload = trans_dict_to_xml(arg)

    response = requests.post(SERVER_NAME + folderURL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)


    print(payload)
    if response.status_code == 201:
        print("success")
    else:
        print(response)
        print("faild")

    return



# Script start
if __name__ == "__main__":
    if "sx" != "":
        print("right")
    sys.exit(0)
    #PublishLayerGroup_S("Gx2", ["cite:t1", "cite:t2"])



    # *******************   publish process test   ********************
    #PublishGeoTIFF("wuhan_atlas", "wuhan2", r"C:\testdata\wuhan2.tif", 7,1,"4508","256")
    #PublishGeoTIFF("wuhan_atlas", "wuhan2", r"C:\testdata\wuhan2.tif", 7)
    #print(VerifyInfo())

    # *******************   test for publish layergroup by function PublishLayerGroup   ********************
    # layers = [{"name":"cite:t1","link":"http://localhost:8080/geoserver/rest/workspaces/cite/layers/t1"},
    #           {"name":"cite:t2","link":"http://localhost:8080/geoserver/rest/workspaces/cite/layers/t2"}]
    # PublishLayerGroup("cite","txtx23000","SINGLE","4508",layers,[-0.5,6612.5,-9352.5,0.5])













