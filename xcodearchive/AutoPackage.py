#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/16 上午11:07
# @Author  : 袁平华
# @Site    : 
# @File    : AutoPackage.py
# @Software: PyCharm Community Edition



import os
import time

from AssetCarAnalysis import AssetImageAnalysis
from  pick import pick


class AutoArhive (object):
    def __init__(self, method='app-store', rootdir=None):
        self.work_space = None
        self.project = None
        self.projectName = None
        self.method = method
        self.rootdir = rootdir
        # 获取当前桌面路径
        self.desktop = os.path.join (os.path.expanduser ('~'), "Desktop")
        self.recognition_project_type ( )

    def recognition_project_type(self):
        '''
        识别项目类型
        :return: 
        '''
        # 获取工程目录路径
        if self.rootdir == None:
            self.rootdir = os.getcwd ( )
        dirlist = os.listdir (self.rootdir)
        for file in dirlist:

            if os.path.splitext (file)[1] == '.xcworkspace':
                self.projectName = os.path.splitext (file)[0]
                self.work_space = file
            elif os.path.splitext (file)[1] == '.xcodeproj' and os.path.splitext (file)[0] != 'Pods':
                self.projectName = os.path.splitext (file)[0]
                self.project = file
            else:
                continue

        self.configBase ( )

    def configBase(self):

        # 获取当前时间并格式化
        datetime = time.strftime ('%m-%d-%H-%M', time.localtime ( ))
        # 生成基础目录
        basePath = os.path.join (self.desktop, datetime)

        # archivePath
        archivePath = os.path.join (basePath, 'archive')
        if not os.path.exists (archivePath):
            os.makedirs (archivePath)

        # exportPath
        exportPath = os.path.join (basePath, 'ipa')
        if not os.path.exists (exportPath):
            os.makedirs (exportPath)

        configurationName = "Release"
        # debug版本[Debug|Release]，使用xcodebuild -list查看configuration支持的类型

        # baseCommand
        if self.work_space:
            baseCommand = ' -workspace ' + os.path.join (self.rootdir,
                                                         self.work_space) + ' -scheme ' + self.projectName + ' -configuration ' + configurationName
        elif self.project:
            baseCommand = ' -project ' + os.path.join (self.rootdir,
                                                       self.project) + '  -scheme ' + self.projectName + ' -configuration ' + configurationName
        else:
            print ("Not found project or workspace ,please check the project's position ")
            return  # 没找到工程文件或workspace文件

        # archive cmd
        archivePathOption = ' -archivePath ' + os.path.join (archivePath, self.projectName)

        # export cmd
        exportPathOption = ' -exportPath ' + exportPath

        plistpath = os.path.join (basePath, self.method + '.plist')
        self.produce_plistcontent (plistpath)

        exportPlistOptions = ' -exportOptionsPlist ' + plistpath

        xcodebuild_archive = 'xcodebuild archive ' + archivePathOption + baseCommand

        print ('archive %s' % (xcodebuild_archive))
        xcodebuild_export = 'xcodebuild -exportArchive ' + archivePathOption + '.xcarchive' + exportPathOption + exportPlistOptions

        os.system (xcodebuild_archive)
        os.system (xcodebuild_export)

        AssetImageAnalysis (archive_path=os.path.join (archivePath, self.projectName + '.xcarchive'),
                            result_path=archivePath)

    def produce_plistcontent(self, plistpath):
        '''
        生成打包需要的plist文件
        :param plistpath:  文件路径
        :return: 
        '''
        plistcontent = """
        	<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
        	<key>items</key>
        	<array>
        		<dict>
        			<key>metadata</key>
        			<dict>
        				<key>kind</key>
        				<string>software</string>
        				<key>title</key>
        				<string>%s</string>
        				<key>method</key>
        				<string>%s</string>
        			</dict>
        		</dict>
        	</array>
        </dict>
        </plist>
        	""" % (self.projectName, self.method)

        with open (plistpath, 'w') as file:
            file.write (plistcontent)

            #
            # if __name__ == '__main__':
            #     AutoArhive (rootdir=u'/Users/yuanpinghua/Documents/MASK/Code/Mask')
            # AutoArhive (method='ad-hoc',rootdir=u'/Users/yuanpinghua/Documents/IOS/ActionSheet2')
            #
            # if len(argv) == 1:
            #     AutoArhive()
            # elif len(argv)==2:
            #     AutoArhive(method=argv[1])
            # else:
            #     print("使用方法：在工程目录下运行该脚本. \n"
            #           "1. 打发布包  python Autopackage.y\n"
            #           "2. 打测试包  python Autopackage.y ad-hoc\n"
            #           "3. 打企业包  python Autopackage.y enterprise\n"
            #           "4. 打开发包  python Autopackage.y development\n")


            # if __name__ == '__main__':


def choose(index):
    if int (index) == 0:
        AutoArhive ( )
    elif int (index) == 1:
        AutoArhive (method='ad-hoc')

    elif int (index) == 2:
        AutoArhive (method='enterprise')

    elif int (index) == 3:
        AutoArhive (method='development')


title = 'please choose archive method:'
options = [u'1. App-store ', u'2. ad-hoc', u'3. enterprise', u'4. development']
option, index = pick (options, title, indicator='=>')
choose (index)
