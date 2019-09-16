#!/usr/bin/python
#-= coding:utf-8 =-
import os, sys
import argparse
import getopt

from scripting_utils import *
# import build_sdk_android    as android
import build_sdk_ios        as ios
# import build_sdk_windows    as windows

set_log_tag('BUILD-SDK')

if __name__ != "__main__":
    error('Error. Do not import this script, but run it explicitly.')
    exit()
#------------------------------------------------------------------
# python ci-build.py  action  option
#
# [action]
#     build          normal
#     release        release
# [option]
# --platform  [iOS,Android,windows]
# --version  指定版本号（详见版本号说明）1.iOS平台，版本号需要同步给plist配置文件。2.Android平台，版本号需要同步给gradle.properise
# --output_dir
# --macro_arg

# 例如：
# 日常build
#     python ci-build.py  build --platform iOS  --version 1.2.0-dev --output_dir  artifacts  --macro_arg xxxxx
# 发布build
#     python ci-build.py  release  --platform iOS  --version 1.2.0 --output_dir  artifacts  --macro_arg xxxxx
# ------------------------------------------------------------------
####=-------


#
# parser = argparse.ArgumentParser()
# #
# # parser.add_argument('', '', action='version',
# #                     version='%(prog)s version : v 0.01', help='build or release')
# parser.add_argument('build', help="---build------")
# parser.add_argument('release', help="---release----")
# parser.add_argument('--platform', '-p',
#
#                     help='iOS,Android,windows')
#
# args = parser.parse_args()
# print("=== end ===")


# get arguments
#usage_message = 'Usage: python build_sdk.py [ios | android | windows] [otpional, to build test library too: --with-testlib | -tl]\n';
usage_message = 'Usage: python build_sdk.py  [build | release ] , --platform [ios | android | windows] [otpional \n';
if len(sys.argv) < 2:
    error('Error. action not provided.')
    debug(usage_message)
    exit()
action = sys.argv[1]

if action != 'build' and action != 'release':
    error('Error. Unknown action provided: [{0}]'.format(action))
    debug(usage_message)
    exit()
debug_green('Script start. action=[{0}]...'.format(action))

# arg = getopt.getopt(sys.argv[2:],'',['help'])
#print(arg)


platform_opt = sys.argv[2]
if platform_opt != '--platform':
    error('Error. Unknown platform_opt provided: [{0}]'.format(platform_opt))
    exit()
platform = sys.argv[3]
if platform != 'iOS' and platform != 'android' and platform != 'windows':
    error('Error. Unknown platform provided: [{0}]'.format(platform))
    debug(usage_message)
    exit()


version_opt = sys.argv[4]
if version_opt != '--version':
    error('Error. Unknown version_opt provided: [{0}]'.format(version_opt))
    exit()



version = sys.argv[5]
# if version != '--version':
#     error('Error. Unknown version_opt provided: [{0}]'.format(version_opt))
#     exit()
debug_green('Script start. version=[{0}]...'.format(version))

output_dir_opt = sys.argv[6]
if output_dir_opt != '--output_dir':
    error('Error. Unknown output_dir_opt provided: [{0}]'.format(output_dir_opt))
    exit()

output_dir = sys.argv[7]
debug_green('Script start. output_dir=[{0}]...'.format(output_dir))

macro_arg_opt = sys.argv[8]
if macro_arg_opt != '--macro_arg':
    error('Error. Unknown macro_arg_opt provided: [{0}]'.format(macro_arg_opt))
    exit()

macro_arg = sys.argv[9]
if macro_arg != 'NONE':
    error('Warning. CIX gives  macro_arg : [{0}]'.format(macro_arg))
    exit()
#--------------------------------
#develop version.ios默认会加-dev;android默认会加-SNAPSHOT
#获取ios的真实版本号
if platform == "iOS" and  version.endswith('-dev'):
    index = version.find('-dev')
    real_version = version[:index]

# 获取android的真实版本号
if platform == "Android" and  version.endswith('-SNAPSHOT'):
    index = version.find('-SNAPSHOT')
    real_version = version[:index]
debug_green('Script start. real_version=[{0}]...'.format(real_version))

#------------------------------



with_test_lib = False
# if len(sys.argv) == 3 and (sys.argv[2] == '--with-testlib' or sys.argv[2] == '-tl'):
#     with_test_lib = True
# elif len(sys.argv) == 3:
#     error('Unknown 2nd parameter.')
#     debug(usage_message)
#     exit()
#
# debug_green('Script start. Platform=[{0}]. With Test Library=[{1}]. Build Adjust EduBase SDK ...'.format(platform, with_test_lib))

# ------------------------------------------------------------------
# Paths
script_dir              = os.path.dirname(os.path.realpath(__file__))
root_dir                = os.path.dirname(os.path.normpath(script_dir))
android_submodule_dir   = '{0}/ext/android'.format(root_dir)
ios_submodule_dir       = '{0}\\build\\ios'.format(script_dir)
windows_submodule_dir   = '{0}/ext/windows'.format(root_dir)
debug_green('Script start. script_dir=[{0}]. root_dir=[{1}]. ios_submodule_dir=[{2}]'.format(script_dir, root_dir,ios_submodule_dir))
# ------------------------------------------------------------------
# Call platform specific build method.
if platform == 'iOS':
    set_log_tag('IOS-SDK-BUILD')
    ####check ios build script folder
    check_submodule_dir('iOS', ios_submodule_dir)
    ios.build(root_dir, ios_submodule_dir, with_test_lib)
elif platform == 'Android':
    set_log_tag('ANROID-SDK-BUILD')
    check_submodule_dir('Android', android_submodule_dir + '/sdk')
    # android.build(root_dir, android_submodule_dir, with_test_lib)
else:
    set_log_tag('WINDOWS-SDK-BUILD')
    check_submodule_dir('Windows', windows_submodule_dir + '/sdk')
    # windows.build(root_dir, windows_submodule_dir)

remove_files('*.pyc', script_dir, log=False)

# ------------------------------------------------------------------
# Script completed.
debug_green('Script completed!')
