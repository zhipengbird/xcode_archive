# xcodearchive

  一个方便快捷的xcode编译打包工具脚本 ，一个命令行，搞定你的所有需求。


 在使用中遇到什么问题，或有什么新的需求，请邮件联系 yuanpinghua@yeah.net



# 使用说明
作为命令行工具使用的安装方式：
1. 下载本工程源文件
打开命令行工具，切换置工程目录，执行如下命令：
`python setup.py install`
2. 使用pip安装(**推荐使用方法安装**)
   打开命令行工具，执行如下命令：
   `pip install xcoodearchive`
   > 如果你已安装该工具，需要更新的话，请执行如下命令：
    `pip install -u xcodearchive`

>ps:  我不安装，可以使用吗，当然可以
  将本工程源文件放置到你项目录下，在命令行输入'python xcodearchive/xcodetool.py'即可，后续操作请见后续说明。


如何使用该工具进行xcode工程打包：
在命令行中切换置你的项目工程录，输入`xcodearchive`回车即可
输入回车后，你会看到一个命令行交互菜单：
```
 Please select a way to work!

 => build project
    archive project
    export ipa
    clean build
```
这里有四个入口分别是：
1. 编译工程文件
2. 对项目工程进行打包
3. 对已经archive好的项目进行导出相应的ipa
4. 清理编译文件

根据你的需要进行选择相应的入口。
这里将其他可以可能遇到界面菜单稍作说明：
```
 Please select the corresponding target

 => Mask
    MaskTests
    MaskUITests
    MaskRandomUITests

```
在上面的交互里要列出了你项目中所有可用的target，你选择相应的target即可。


```
 Please select the corresponding scheme

 => Mask
```
在上面的交互里列出了你项目中所有可用的schem文件，选择相应的schem文件即可

```
 Please select the corresponding configuration

 => Debug
    Release
```
在上面的交互里列出了要打包或都编译的模式（debug/release），根据你的需要进行选择。


```
 Please choose the way to export!

 => app-store
    enterpris
    ad-hoc
    development

```
在上面的交互里列出需要导出包的用途，上传至商店／企业包／测试包／开发包，根据你的需要进行选择。






