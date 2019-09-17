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
import os, shutil, glob, time, sys, platform, subprocess
import argparse
import zipfile

def set_log_tag(t):
    global TAG
    TAG = t
def logmsg(msg):
    if not is_windows():
        print(('{0}[{1}').format( TAG, msg))
    else:
        print(('[{0}][INFO]: {1}').format(TAG, msg))
def is_windows():
    return platform.system().lower() == 'windows';
set_log_tag('IOS_COPY')
execfile('../build_common.py')
init_common(os.path.abspath('..'))


parser = argparse.ArgumentParser(description='builder for iOS')
##the zip out dir of ci system
parser.add_argument('outdir',     help='outdir for zip')
parser.add_argument('release_ios_out_dir',     help='ios_all_a_out_dir')
parser.add_argument('ioszipname',     help='ioszipname')

args = parser.parse_args()
OUTDIR = args.outdir
OUTNAME = args.ioszipname

release_ios_out_dir = args.release_ios_out_dir

# TODO
BUILD_MODE = 'Release'

arch_list = ['arm64',
            'armv7',
            'armv7s',
            'x86_64'   # Simulator
            ]

release_libs_dir = os.path.abspath(release_ios_out_dir)
#create folder
makedirs(release_libs_dir)
#show msg
logmsg('Script start. OUTDIR=[{0}]. release_libs_dir=[{1}]'.format(OUTDIR, release_libs_dir))

def create_universal_lib(libs):
    if len(libs) == 0:
        return
    #file name
    name = os.path.basename(libs[0])
    print 'creating universal library', name + ' ...'
    lipo_commands = ['lipo', '-create']
    for lib in libs:
        lipo_commands.append(lib)
    lipo_commands.append('-output')
    lipo_commands.append(release_libs_dir + '/' + name)
    call(lipo_commands)

build_dir = os.path.abspath('build/' + BUILD_MODE) + '/'

# static libs
#nakama_cpp_libs = []
#grpc_libs = []
#grpcpp_libs = []
#gpr_libs = []
libgflags_nothreads_libs = []
address_sorting_libs = []
cares_libs = []
crypto_libs = []
ssl_libs = []
protobuf_libs = []
z_libs = []
#cpprest_libs = []


def zip_ios_libs(folder, zipfilepath):
    logmsg('zip_ios_libs start. from folder =[{0}] to  [{1}]'.format(folder, zipfilepath))
#    zf = zipfile.ZipFile('./bundle_egc_ios.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
#thePath = 'G:\LEAEN_PY\ci-build\out_third_sdk\libs\ios'
    list = os.listdir(folder)
    zf = zipfile.ZipFile(zipfilepath, mode='w', compression=zipfile.ZIP_STORED)
    try:
        for f in list:
            filename = os.path.basename(f)
            print("has file : " + folder + os.sep + f)
            absfile = folder + os.sep + f
            #print("has file : " + filename)
            print("add file : " + filename)
            zf.write(absfile, filename)
    finally:
        print('closing')
        zf.close()

for arch in arch_list:
    
    print '===build for arch ', arch + ' ...====='
   # ONLY COPY NOT BUILD 
   # call(['python', 'build_ios.py', arch])
    
    build_arch_dir = build_dir + arch
    
    # nakama_cpp_libs     .append(build_arch_dir + '/src/libnakama-cpp.a')
    # grpc_libs           .append(build_arch_dir + '/third_party/grpc/libgrpc.a')
    # grpcpp_libs         .append(build_arch_dir + '/third_party/grpc/libgrpc++.a')
    # gpr_libs            .append(build_arch_dir + '/third_party/grpc/libgpr.a')
    address_sorting_libs.append(build_arch_dir + '/grpc/libaddress_sorting.a')
    libgflags_nothreads_libs    .append(build_arch_dir + '/grpc/third_party/gflags/libgflags_nothreads.a')

    cares_libs          .append(build_arch_dir + '/grpc/third_party/cares/cares/lib/libcares.a')
    crypto_libs         .append(build_arch_dir + '/grpc/third_party/boringssl/crypto/libcrypto.a')
    ssl_libs            .append(build_arch_dir + '/grpc/third_party/boringssl/ssl/libssl.a')
    protobuf_libs       .append(build_arch_dir + '/grpc/third_party/protobuf/libprotobuf.a')
    z_libs              .append(build_arch_dir + '/grpc/third_party/zlib/libz.a')
    # cpprest_libs        .append(build_arch_dir + '/third_party/cpprestsdk/' + BUILD_MODE + '/Binaries/libcpprest.a')

make_universal_list = []

# def copy_nakama_lib():
#     make_universal_list.append(nakama_cpp_libs)

def copy_protobuf_lib():
    make_universal_list.append(protobuf_libs)

def copy_ssl_lib():
    make_universal_list.append(ssl_libs)
    make_universal_list.append(crypto_libs)

def copy_grpc_lib():
    make_universal_list.append(address_sorting_libs)
    # make_universal_list.append(gpr_libs)
    # make_universal_list.append(grpcpp_libs)
    # make_universal_list.append(grpc_libs)
    ###add this 
    make_universal_list.append(libgflags_nothreads_libs)
    make_universal_list.append(cares_libs)
    make_universal_list.append(z_libs)

# def copy_rest_lib():
#     make_universal_list.append(cpprest_libs)

    print '====copy libs ======='

####COPY LIBS TO DEST FOLDER
#copy_libs()

logmsg('=====zip_ios_libs')
zip_ios_libs(release_libs_dir,OUTDIR+os.sep+OUTNAME)

for libs_list in make_universal_list:
    create_universal_lib(libs_list)

####copy BOOST 
# copy boost libs (they are already universal libs)
# boost_libs_path = os.path.abspath('../../third_party/cpprestsdk/Build_iOS/boost/lib')
# copy_file(os.path.join(boost_libs_path, 'libboost_chrono.a'), release_libs_dir)
# copy_file(os.path.join(boost_libs_path, 'libboost_thread.a'), release_libs_dir)

#######DYLIB NOT NEED
# dynamic libs
#release_libs_dir = os.path.abspath(OUTDIR)

# for arch in arch_list:
#     call(['python', 'build_ios.py', '--dylib', arch])
    
#     build_arch_dir = build_dir + arch
#     dest_dir = release_libs_dir + '/' + arch

#     dylib_in_build = build_arch_dir + '/src/libnakama-cpp.dylib'
#     call(['install_name_tool', '-id', '@executable_path/libnakama-cpp.dylib', dylib_in_build])
    
#     makedirs(dest_dir)
#     copy_file(dylib_in_build, dest_dir)



#https://github.com/jeromevonk/candidates-api/blob/b3e97550a52912d0381ccb968ee7c97fc801358c/scripts/aws_bundle.py
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

#https://github.com/TrafficSenseMSD/SumoTools/blob/8607b4f885f1d1798e43240be643efe6dccccdaa/build_module.py
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

#zip file in folder to zipfilepath (full path with name)




print 'done.'