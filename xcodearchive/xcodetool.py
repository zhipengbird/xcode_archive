#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/23 上午10:40
# @Author  : 袁平华
# @Site    : 
# @File    : xcodetool.py
# @Software: PyCharm Community Edition


import json
import os
import shutil
import sys

from AssetCarAnalysis import AssetImageAnalysis
from  pick import pick

__default_path_keychain = '~/Library/Keychains/login.keychain'

altool = '/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool'
# altool 路径

# 程序入口方式
enter_title = 'Please select a way to work!'
enter_method = ['build project', 'archive project', 'export ipa', 'clean build', 'Check Asset.car', 'upload ipa']

# 导出方式
export_title = 'Please choose the way to export!'
export_method = ['app-store', 'enterprise', 'ad-hoc', 'development']

export_format_title = "Please choose the format to export!"
export_format = ['IPA', 'PKG', 'APP']

# 苹果账号
appid_username = None
appid_password = None

# 获取根目录文件夹
root_dir = os.path.realpath ('.')
base_dir = os.path.join (root_dir, 'xcodebuild')

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


def auto_recogonize_ipa_file(path):
    """
    搜索当前文件前下的所有ipa包
    :param path: 
    :return: ipa数组包 
    """
    ipa_list = []
    dirlist = os.listdir (path)
    for file in dirlist:
        if os.path.splitext (file)[1] == '.ipa':
            ipa_list.append (file)
        else:
            continue
    return ipa_list


def get_project_basic_info():
    json_list = os.popen ('xcodebuild -list -json')

    json_data = json_list.read ( )

    result = json.loads (json_data)
    project = result['project']
    # sys.exit(1)
    tartgets = project['targets']
    schemes = project['schemes']
    configurations = project['configurations']
    project_name = project['name']
    if len (schemes) == 0:
        schemes = [project_name]

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
				<key>method</key>
				<string>%s</string>
				<key>title</key>
				<string>%s</string>
				<key>kind</key>
				<string>software</string>
				<key>uploadSymbols</key>
				<true/>
				<key>iCloudContainerEnvironment</key>
				<string>Production</string>
            </dict>
            </plist>
            """ % (method, projectname)

    with open (plistpath, 'w') as file:
        file.write (plistcontent)


def export_dsyms(archive_path, scheme, export_path):
    """
    导出项目DSYMs文件
    :param archive_path:  项目包路径
    :param scheme: 项目名
    :param export_path: 导出路径
    :return: 
    """
    dysm_path = os.path.join (archive_path, 'DSYMs', '{}.app.DSYM'.format (scheme))
    try:
        shutil.move (dysm_path, export_path)
    except Exception as e:
        print e.__str__ ( )


def build_project():
    """
    对工程进行编译
    :return: 
    """
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
    print (build_project_cmd)
    print ('performing compilation operation...')
    status = os.system (build_project_cmd)
    print (status)


def clean_build():
    clean_cmd = 'xcodebuild clean'
    print (clean_cmd)
    os.system (clean_cmd)
    if os.path.exists (os.path.join (root_dir, 'build')):
        shutil.rmtree (os.path.join (root_dir, 'build'))


def archive_project():
    """
    对当前工程进行打包操作
    :return: 
    """
    auto_recogonize_project ( )
    result = get_project_basic_info ( )
    if work_space_file is None and project_file is None:
        print ("Not found any file (.xcworkspace or *.xcodeproj),please check it")
        sys.exit (1)

    if work_space_file:
        archive_cmd = 'xcodebuild archive -archivePath %s -workspace %s -scheme %s -configuration %s ' % (
            os.path.join (base_dir, result[3]), os.path.join (root_dir, work_space_file), result[1], result[2])
    else:
        archive_cmd = 'xcodebuild archive -archivePath %s -project %s -scheme %s -configuration %s  ' % (
            os.path.join (base_dir, result[3]), os.path.join (root_dir, work_space_file), result[1], result[2])

    if check_upload_ipa ( ):

        # 选择导出方式
        method, index = pick (export_method, export_title, '=>')
        # 输出命令
        print (archive_cmd)
        # 执行命令
        print (os.system (archive_cmd))
        # 导出ipa
        export_ipa (base_dir, method)
        ipa_list = auto_recogonize_ipa_file (base_dir)
        if len (ipa_list) > 0:
            ipa_path = os.path.join (base_dir, ipa_list[0])
            upload_ipa_appstore (ipa_path)
    else:
        # 选择导出方式
        method, index = pick (export_method, export_title, '=>')
        # 输出命令
        print (archive_cmd)
        # 执行命令
        print (os.system (archive_cmd))
        # 导出ipa
        export_ipa (base_dir, method)


def enter_username_password():
    """
    要求用户输入账号和密码
    :return: 
    """
    # 要求用户输入账号和密码：
    global appid_password, appid_username
    appid_username = raw_input ('Please input your accout of appid:').strip ( )
    appid_password = raw_input ('Please input your password of appid:').strip ( )


def check_upload_ipa():
    """
    寻问用户是否需要上传app_store
    :return: 导问结果
    """
    like = raw_input ('Do you want to upload to Appstore?(y/n)').strip ( ).lower ( )
    if like == 'y':
        enter_username_password ( )
        return True
    else:
        return False


def export_ipa(rootpath, method):
    """
    导出ipa包
    :param rootpath:  .archive文件所在目录
    :param method: 
    :return: 
    """
    archivepath, project_name = auto_recogonize_archive_file (rootpath)

    if archivepath is None:
        print ("Not found *.xcarchive file ")
        sys.exit (1)
    plistpath = os.path.join (base_dir, method + '.plist')
    produce_plistcontent (project_name, plistpath=plistpath, method=method)
    export_cmd = 'xcodebuild  -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s  ' % (
        archivepath, base_dir, plistpath)
    print (export_cmd)
    print ('processing export  operation... ')
    print (os.system (export_cmd))
    export_dsyms (archivepath, project_name, base_dir)


def upload_ipa_appstore(ipa_path):
    """
    上传ipa到appstore
    :param ipa_path: 
    :return: 
    """

    # username = raw_input('please enter the APPid:').strip()
    # password = raw_input('Please enter the password:').strip()
    validate_cmd = '%s --validate-app -f %s -u %s -p %s --output-format xml' % (
        altool, ipa_path, appid_username, appid_password)

    upload_cmd = '%s --upload-app -f %s -u %s -p %s --output-format xml' % (
        altool, ipa_path, appid_username, appid_password)

    print (validate_cmd)
    print (upload_cmd)
    print (os.system (validate_cmd))
    print (os.system (upload_cmd))


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

    elif index == 3:
        clean_build ( )

    elif index == 4:
        # 分析asset.car里的图片资源
        archive_path, _ = auto_recogonize_archive_file (root_dir)
        AssetImageAnalysis (archive_path, base_dir)

    else:
        # 上传ipa

        security_cmd = "security unlock-keychain"
        os.system (security_cmd)
        ipa_list = auto_recogonize_ipa_file (base_dir)
        if len (ipa_list) > 0:
            ipa, _ = pick (ipa_list, "current ipa list", '=>')
            ipa_path = os.path.join (base_dir, ipa)
            print (ipa_path)
            if check_upload_ipa ( ):
                upload_ipa_appstore (ipa_path)
        else:
            print ("Not any ipa files !")


if __name__ == '__main__':
    main ( )
