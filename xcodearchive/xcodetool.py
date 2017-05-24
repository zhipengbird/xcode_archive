#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/23 上午10:40
# @Author  : 袁平华
# @Site    : 
# @File    : xcodetool.py
# @Software: PyCharm Community Edition


import json
import os
import sys
import shutil

from  pick import pick

# 程序入口方式
enter_title = 'Please select a way to work!'
enter_method = ['build project', 'archive project', 'export ipa', 'clean build']

# 导出方式
export_title = 'Please choose the way to export!'
export_method = ['app-store', 'enterpris', 'ad-hoc', 'development']

export_format_title = "Please choose the format to export!"
export_format = ['IPA', 'PKG', 'APP']

# 获取根目录文件夹
root_dir = os.getcwd ( )
base_dir = os.path.join (root_dir, 'xcodebuild')

if os.path.exists (base_dir):
    shutil.rmtree (base_dir)

if not os.path.exists (base_dir):
    os.makedirs (base_dir)

work_space_file = None
project_file = None


def auto_recogonize_project():
    '''
    在当前目录下面寻找工程文件或都工作空间
    :return: 
    '''
    dirlist = os.listdir (root_dir)
    for file in dirlist:
        if os.path.splitext (file)[1] == '.xcworkspace':
            global work_space_file
            work_space_file = file
        elif os.path.splitext (file)[1] == '.xcodeproj' and os.path.splitext (file)[0] != 'Pods':
            global project_file
            project_file = file
        else:
            continue


def auto_recogonize_archive_file(path):
    '''
    识别archive 文件 返回文件路径
    :return: 
    '''
    archivepath = None
    project_name = None
    dirlist = os.listdir (path)
    for file in dirlist:
        if os.path.splitext (file)[1] == '.xcarchive':
            archivepath = file
            project_name = os.path.splitext (file)[0]
        else:
            continue

    if archivepath:
        return (os.path.join (path, archivepath), project_name)
    else:
        return (None, None)


def get_project_basic_info():
    json_list = os.popen ('xcodebuild -list -json')

    json_data = json_list.read ( )

    result = json.loads (json_data)
    project = result['project']
    # print  project
    tartgets = project['targets']
    schemes = project['schemes']
    configurations = project['configurations']
    project_name = project['name']
    target, index = pick (tartgets, 'Please select the corresponding target', '=>')
    scheme, index = pick (schemes, 'Please select the corresponding scheme', '=>')
    configuration, index = pick (configurations, 'Please select the corresponding configuration', '=>')
    return [target, scheme, configuration, project_name]


def produce_plistcontent(projectname, plistpath, method):
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
        	""" % (projectname, method)

    with open (plistpath, 'w') as file:
        file.write (plistcontent)


def build_project():
    '''
    对工程进行编译
    :return: 
    '''
    auto_recogonize_project ( )
    result = get_project_basic_info ( )
    if work_space_file:
        # 编译工作空间
        build_project_cmd = 'xcodebuild -workspace %s  -scheme %s  -configuration  %s build' % (
            os.path.join (root_dir, work_space_file), result[1], result[2])
    else:
        # 编译工程文件
        build_project_cmd = 'xcodebuild -project %s  -target %s -configuration %s build' % (
            os.path.join (root_dir, project_file), result[0], result[2])
    print
    build_project_cmd
    print
    'performing compilation operation...'
    status = os.system (build_project_cmd)
    print
    status


def clean_build():
    clean_cmd = 'xcodebuild clean'
    print (clean_cmd)
    os.system (clean_cmd)
    if os.path.exists (os.path.join (root_dir, 'build')):
        shutil.rmtree (os.path.join (root_dir, 'build'))


def archive_project():
    '''
    对当前工程进行打包操作
    :return: 
    '''
    auto_recogonize_project ( )
    result = get_project_basic_info ( )
    if work_space_file is None and project_file is None:
        print ("Not found any file (.xcworkspace or *.xcodeproj),please check it")
        sys.exit (1)

    if work_space_file:
        archive_cmd = 'xcodebuild archive -archivePath %s -workspace %s -scheme %s -configuration %s archive' % (
            os.path.join (base_dir, result[3]), os.path.join (root_dir, work_space_file), result[1], result[2])
    else:
        archive_cmd = 'xcodebuild archive -archivePath %s -project %s -scheme %s -configuration %s  archive' % (
            os.path.join (base_dir, result[3]), os.path.join (root_dir, work_space_file), result[1], result[2])

    # 选择导出方式
    method, index = pick (export_method, export_title, '=>')
    # 输出命令
    print (archive_cmd)
    # 执行命令
    os.system (archive_cmd)
    export_ipa (base_dir, method)


def export_ipa(rootpath, method):
    '''
    
    :param rootpath: 
    :param format: 
    :param method: 
    :return: 
    '''
    archivepath, project_name = auto_recogonize_archive_file (rootpath)

    if archivepath is None:
        print
        "Not found *.xcarchive file "
        sys.exit (1)
    plistpath = os.path.join (base_dir, method + '.plist')
    produce_plistcontent (project_name, plistpath=plistpath, method=method)
    export_cmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s archive' % (
        archivepath, base_dir, plistpath)
    print (export_cmd)
    print ('processing export  operation... ')
    os.system (export_cmd)


def main():
    method, index = pick (enter_method, enter_title, indicator='=>')
    if index == 0:
        # 编译工程文件
        build_project ( )

    elif index == 1:
        archive_project ( )
        # 对工程进行打包

    elif index == 2:
        # 对已有的archive文件进行导出ipa
        method, index = pick (export_method, export_title, '=>')
        export_ipa (root_dir, method)
    else:
        clean_build ( )


if __name__ == '__main__':
    main ( )
