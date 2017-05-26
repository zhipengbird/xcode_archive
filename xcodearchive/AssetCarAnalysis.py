#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/16 下午1:36
# @Author  : 袁平华
# @Site    : 
# @File    : AssetCarAnalysis.py
# @Software: PyCharm Community Edition


"""
在包文件中找出图片编码为srbg16的图片，并将他们写入单个结果文件
"""

import json
import os


class AssetImageAnalysis:
    def __init__(self, archive_path, result_path):
        '''
        
        :param archive_path:  .xcarchive 文件路径，
        :param result_path:     解析结果存放文件夹
        '''
        self.archive_path = archive_path
        self.resultpath = result_path
        carpath = self.find_asset_scar (archive_path)
        self.asset_property (carpath)

    def find_asset_scar(self, baseroot):
        for root, dirs, files in os.walk (baseroot):
            for file in files:
                if os.path.splitext (file)[1] == '.car':
                    print (os.path.join (root, file))
                    return os.path.join (root, file)
        return None

    def asset_property(self, carpath):
        jsonpath = os.path.join (self.resultpath, 'assetcar.json')
        xrun_cmd = "xcrun --sdk iphoneos assetutil --info %s > %s " % (carpath, jsonpath)
        os.system (xrun_cmd)
        self.parse_json (jsonpath)

    def parse_json(self, jsonpath):
        with open (jsonpath, 'r')as file:
            data = file.read ( )
            if data:
                data = json.loads (data)

        # 寻找不符合规则的图片名字
        result = []
        for dic in data:
            if 'DisplayGamut' in dic:
                if dic['DisplayGamut'] == 'P3':
                    item = {"Name": dic['Name'], 'DisplayGamut': dic['DisplayGamut'], 'Encoding': dic['Encoding']}
                    result.append (item)

        # 若有不符合规则的图片，则它们写入json文件
        if len (result) > 0:
            print ("warning ,these picture code are illegal,please checked !!")
            for item in result:
                print ('Name :'+ item['Name'] + "Ecodeing :"+item["Encoding"])
            print ("all counts : %s" % (len (result)))
        else:
            print ("OK!! No problem")
            result.append (u'OK!! No problem')

        # 序列化成json字符，写入文件
        jsonobject = json.dumps (result)
        with open (os.path.join (self.resultpath, 'analysis.json'), 'w') as file:
            file.write (jsonobject)
