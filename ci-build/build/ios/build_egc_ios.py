#!/usr/bin/env python
#
# Copyright 2019 The Nakama Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import os
import argparse


execfile('../build_common.py')
init_common(os.path.abspath('..'))

parser = argparse.ArgumentParser(description='builder for iOS')
parser.add_argument('arch',     help='architecture e.g. arm64 armv7 armv7s x86_64')
parser.add_argument('outdir',     help='outdir for zip')
parser.add_argument('--dylib',  help='build DynamicLib', action='store_true')

args = parser.parse_args()

ARCH = args.arch
SHARED_LIB = args.dylib
###TODO
BUILD_MODE = 'Release'
OUTDIR = args.outdir

print
print 'Building for', ARCH + 'outdir ' , OUTDIR ,  str(SHARED_LIB)
print

build_dir = './build/' + BUILD_MODE + '/' + ARCH

if ARCH == 'x86_64':
    is_simulator = True
else:
    is_simulator = False

cwd = os.getcwd()

makedirs(build_dir)

def build(target):
    print 'building ' + target + '...'
    call(['cmake',
          '--build',
          build_dir,
          '--target',
          target
          ])

deployment_target = '10.9'

if USE_CPPREST:
    # build boost
    boost_version = '1.69.0'

    CPPREST_IOS_PATH = os.path.abspath('../../third_party/cpprestsdk/Build_iOS')

    Apple_Boost_BuildScript_Path = os.path.join(CPPREST_IOS_PATH, 'Apple-Boost-BuildScript')

    if not os.path.exists(Apple_Boost_BuildScript_Path):
        # clone Apple-Boost-BuildScript
        call([
            'git', 'clone', 'https://github.com/faithfracture/Apple-Boost-BuildScript',
            Apple_Boost_BuildScript_Path
        ])
        os.chdir(Apple_Boost_BuildScript_Path)
        call(['git', 'checkout', '1b94ec2e2b5af1ee036d9559b96e70c113846392'])

    target_boost_path = os.path.join(CPPREST_IOS_PATH, 'boost')
    target_boost_lib_path = os.path.join(target_boost_path, 'lib')
    target_boost_inc_path = os.path.join(target_boost_path, 'include')

    # check is boost built
    if not os.path.exists(target_boost_lib_path) or not os.path.exists(target_boost_inc_path):
        os.chdir(Apple_Boost_BuildScript_Path)
        # boost.sh --min-ios-version 8.0 -ios --no-framework --universal --boost-libs "chrono system thread" --ios-archs "arm64 armv7 armv7s" --boost-version 1.69.0
        call(['./boost.sh',
            '--min-ios-version', deployment_target,
            '-ios',
            '--no-framework',
            '--universal',
            '--boost-libs', 'chrono system thread',
            '--ios-archs', 'arm64 armv7 armv7s',
            '--boost-version', boost_version
            ])
        os.chdir(cwd)

        boost_universal_libs_path = os.path.join(Apple_Boost_BuildScript_Path, 'build/boost/' + boost_version + '/ios/build/universal')
        makedirs(target_boost_path)
        mklink(link=target_boost_lib_path, target=boost_universal_libs_path)
        mklink(link=target_boost_inc_path, target=os.path.join(Apple_Boost_BuildScript_Path, 'build/boost/' + boost_version + '/ios/prefix/include'))

if is_simulator:
    cmake_toolchain_path = os.path.abspath('../../cmake/ios.simulator.toolchain.cmake')
else:
    cmake_toolchain_path = os.path.abspath('../../cmake/ios.toolchain.cmake')

#generator = 'Xcode'
generator = 'Unix Makefiles'

##-B to set binary folder 
# generate projects
# call(['cmake',
#       '-B',
#       build_dir,
#       '-DCMAKE_OSX_DEPLOYMENT_TARGET=' + deployment_target,
#       '-DCMAKE_OSX_ARCHITECTURES=' + ARCH,
#       '-Dprotobuf_BUILD_PROTOC_BINARIES=OFF',
#       '-DgRPC_BUILD_CODEGEN=OFF',
#       '-DCMAKE_TOOLCHAIN_FILE=' + cmake_toolchain_path,
#       '-DCMAKE_BUILD_TYPE=' + BUILD_MODE,
#       '-DENABLE_BITCODE=FALSE',
#       '-DENABLE_ARC=TRUE',
#       '-DNAKAMA_SHARED_LIBRARY=' + bool2cmake(SHARED_LIB),
#       '-DBUILD_REST_CLIENT=' + bool2cmake(BUILD_REST_CLIENT),
#       '-DBUILD_GRPC_CLIENT=' + bool2cmake(BUILD_GRPC_CLIENT),
#       '-DBUILD_HTTP_CPPREST=' + bool2cmake(BUILD_HTTP_CPPREST),
#       '-DBUILD_WEBSOCKET_CPPREST=' + bool2cmake(BUILD_WEBSOCKET_CPPREST),
#       '-G' + generator,
#       '../..'
#       ])
#
# call(['cmake',
#       '--build',
#       '/Users/zhangbin/myProjects/ggrpc/grpcv1.22.0/build/ios/build/Release/'+ARCH,
#       '--config',
#       'Release'
#       ])

##copy files to dest folder
call(['python', 'build_ios_all_copy_third.py',OUTDIR,".."+os.sep+".."+os.sep+"out_grpc_third"+os.sep+"libs"+os.sep+"ios",'egc_ios_out.zip'])
### copy file ???

