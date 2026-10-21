# hook.py
# Add gradle options for notify



from pathlib import Path
from os.path import dirname, join, exists
from pythonforandroid.recipe import  info
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    manifest_file = Path(toolchain._dist.dist_dir) / "src" / "main" / "AndroidManifest.xml"
    old_manifest = manifest_file.read_text(encoding="utf-8")
    unprocessed_args = toolchain.args.unknown_args

    # Your custom receiver XML
    package = "com.snehasys.notify"
    receiver_name = "ResetReceiver"
    receiver_xml = f'''
    <receiver android:name="{package}.{receiver_name}"
              android:enabled="true"
              android:exported="false">
        <intent-filter>
            <action android:name="{package}.ACTION_RESET" />
        </intent-filter>
    </receiver>
    '''

    # Insert before the closing </application>
    new_manifest = old_manifest.replace('</application>', f'{receiver_xml}\n</application>')

    manifest_file.write_text(new_manifest, encoding="utf-8")

    if old_manifest != new_manifest:
        print("Receiver added successfully")
    else:
        print("Failed to add receiver")

def before_apk_build(toolchain):
    unprocessed_args = toolchain.args.unknown_args

    if '--enable-androidx' not in unprocessed_args:
        unprocessed_args.append('--enable-androidx')
        info('Notify Provider: Add android.enable_androidx = True')

    if 'POST_NOTIFICATIONS' not in unprocessed_args:
        unprocessed_args.append('--permission')
        unprocessed_args.append('POST_NOTIFICATIONS')
        info('Notify Provider: Add android.permissions = POST_NOTIFICATIONS')

    if 'INTERNET' not in unprocessed_args:
        unprocessed_args.append('--permission')
        unprocessed_args.append('INTERNET')
        info('Notify Provider: Add android.permissions = INTERNET')
        
    # Check the current versions of these camera Gradle dependencies here:
    #https://developer.android.com/jetpack/androidx/releases/camera#dependencies
    # and the other packages at https://mvnrepository.com/
    required_depends = ['androidx.core:core:1.10.1',
                        'androidx.work:work-runtime:2.7.1'
                        ]    
    existing_depends = []
    read_next = False
    for ua in unprocessed_args:
        if read_next:
            existing_depends.append(ua)
            read_next = False
        if ua == '--depend':
            read_next = True
            
    message = False
    for rd in required_depends:
        name, version = rd.rsplit(':',1)
        found = False
        for ed in existing_depends:
            if name in ed:
                found = True
                break
        if not found:
            unprocessed_args.append('--depend')
            unprocessed_args.append('{}:{}'.format(name,version))
            message = True
    if message:
        info('Camerax Provider: Add android.gradle_dependencies reqired ' +\
             'for CameraX')
        
    # Add the Java source
    java = join(dirname(__file__), 'src')
    if exists(java):
        unprocessed_args.append('--add-source')
        unprocessed_args.append(java)
        info('Add android.add_src = ' +\
             './src')

    # if p4a version supports it 
    # Add android resource
    # res = join(dirname(__file__) , 'src/res')
    # if exists(res):
    #     unprocessed_args.append('--add-resource')
    #     unprocessed_args.append(res)
    #     info("Add android res ... ")
