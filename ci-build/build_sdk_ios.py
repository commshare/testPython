from scripting_utils import *

def egcCall(command, shell=False):
    print 'calling:', str(command)
    res = subprocess.call(command, shell=shell)
    if res != 0:
        sys.exit(-1)
def build(project_dir, source_code_folder, ios_out_dir,with_test_lib):
    # ------------------------------------------------------------------
    # Paths.
    root_dir             = '{0}'.format(project_dir)
    ios_script_dir       = '{0}\\build\\ios'.format(project_dir)
    src_dir               = '{0}'.format(source_code_folder)
    lib_out_dir           = '{0}/libs'.format(ios_out_dir)
    include_out_dir      = '{0}/include'.format(ios_out_dir)
    sdk_static_framework  = '{0}/Frameworks/Static/AdjustSdk.framework'.format(src_dir)


    debug_green('Script start. project_dir=[{0}]. src_dir=[{1}]. lib_out_dir=[{2}]'.format(root_dir, src_dir,
                                                                                                 lib_out_dir))

    # ------------------------------------------------------------------
    # Build EduGrpcBase framework target.
    debug_green('Building EduGrpcBase ios ....ios_script_dir[{0}]'.format(ios_script_dir))
    change_dir(ios_script_dir)
    arch = 'arm64'
    egcCall(['python', 'build_egc_ios.py', arch,ios_out_dir])
    #xcode_build_release('AdjustStatic')
    #copy_file(sdk_static_framework + '/Versions/A/AdjustSdk', lib_out_dir + '/AdjustSdk.a')
    #copy_files('*', sdk_static_framework + '/Versions/A/Headers/', lib_out_dir)

    if with_test_lib:
        # ------------------------------------------------------------------
        # Paths.
        test_static_framework = '{0}/Frameworks/Static/AdjustTestLibrary.framework'.format(src_dir)

        # ------------------------------------------------------------------
        # Build AdjustTestLibraryStatic framework target.
        set_log_tag('IOS-TEST-LIB-BUILD')
        debug_green('Building Test Library started ...')
        change_dir('{0}/AdjustTests/AdjustTestLibrary'.format(src_dir))
        xcode_build_debug('AdjustTestLibraryStatic')
        #copy_file(test_static_framework + '/Versions/A/AdjustTestLibrary', lib_out_dir_test + '/AdjustTestLibrary.a')
        #copy_files('*', test_static_framework + '/Versions/A/Headers/', lib_out_dir_test)
