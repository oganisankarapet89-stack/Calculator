[app]

# (str) Title of your application
title = KarCul

# (str) Package name
package.name = karcul

# (str) Package domain (needed for android/ios packaging)
package.domain = org.karcul

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (leave empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (leave empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# ИСПРАВЛЕНО: добавлен requests
requirements = python3,kivy,requests

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# ИСПРАВЛЕНО: раскомментировано и добавлен icon.png
icon = icon.png

# (list) Supported orientations
orientation = portrait

# (list) List of services to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

# author = © Copyright Info

# Kivy version to use
osx.kivy_version = 2.2.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application
#icon = icon.png

# (list) Permissions
# ИСПРАВЛЕНО: добавлены разрешения для интернета и вибрации
android.permissions = INTERNET, VIBRATE

# (list) features
#android.features = android.hardware.usb.host

# (int) Target Android API
# ИСПРАВЛЕНО: раскомментировано
android.api = 30

# (int) Minimum API your APK / AAB will support
# ИСПРАВЛЕНО: раскомментировано
android.minapi = 21

# (int) Android SDK version to use
# ИСПРАВЛЕНО: раскомментировано
android.sdk = 30

# (str) Android NDK version to use
# ИСПРАВЛЕНО: раскомментировано
android.ndk = 23b

# (int) Android NDK API to use
android.ndk_api = 21

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android SDK
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
# ИСПРАВЛЕНО: добавлено для автоматической сборки
android.accept_sdk_license = True

# (str) Android entry point
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> tag
#android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml

# (str) Full name including package path of the Java class that implements Python Service
#android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (bool) If True, your application will be listed as a home app
# android.home_app = False

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory
#android.add_assets =

# (list) Put these files or directories in the apk res directory
#android.add_resources =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support
# android.enable_androidx = True

# (list) add java compile options
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add
#android.add_gradle_repositories =

# (list) packaging options to add
#android.add_packaging_options =

# (list) Java classes to add as activities to the manifest
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (list) Copy these files to src/main/res/xml/
#android.res_xml = PATH_TO_FILE,

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (str) screenOrientation to set for the main activity
#android.manifest.orientation = fullSensor

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
#android.logcat_pid_only = False

# (str) Android additional adb arguments
#android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation
# android.numeric_version = 1

# (bool) enables Android auto backup feature
android.allow_backup = True

# (str) XML file for custom backup rules
# android.backup_rules =

# (str) manifestPlaceholders property
# android.manifest_placeholders = [:]

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) The format used to package the app for release mode
# android.release_artifact = aab

# (str) The format used to package the app for debug mode
# android.debug_artifact = apk

# (str) A display cutout
#android.display_cutout = never

#
# Python for android (p4a) specific
#

#p4a.url =
#p4a.fork = kivy
#p4a.branch = master
#p4a.commit = HEAD
#p4a.source_dir =
#p4a.local_recipes =
#p4a.hook =
# p4a.bootstrap = sdl2
#p4a.port =
#p4a.setup_py = false
#p4a.extra_args =

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
#ios.codesign.development_team.release = <hexstring>

# (str) Justification text for media
#ios.media_usage_description = "<APP> needs to access your media in order to <Do X and Y and Z> "

# (str) Justification text for local network
#ios.local_network_usage_description = "<App> needs permissions to <Do X and Y and Z> in your Local Area Network"

# (str) Camera Usage justification string
#ios.camera_usage_description = "<App> uses Camera to do <X and Y and Z>"

# (bool) Allow StatusBar to be controlled by API
# ios.viewcontroller_based_statusbar_appearance = False

# (str) A Xml String specifying a extension type
#ios.app_extensions = [["7zip", "zip"],  ["public.zip-archive"], "org.kivy.myappextensionfile", "<MyCustom> Extension File", "${MACOSX_BUNDLE_ICON_FILE}", "http://mysite.com/myapp/extensions.html"],

# (str) URL pointing to .ipa file to be installed
#ios.manifest.app_url =

# (str) URL pointing to an icon (57x57px) to be displayed during download
#ios.manifest.display_image_url =

# (str) URL pointing to a large icon (512x512px) to be used by iTunes
#ios.manifest.full_size_image_url =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
