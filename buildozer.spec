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

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,requests

# (str) Icon of the application
icon = icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, VIBRATE

# (int) Target Android API
android.api = 30

# (int) Minimum API your APK / AAB will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
# ИСПРАВЛЕНО: Kivy требует NDK 28c
android.ndk = 28c

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1