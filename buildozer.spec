[app]
title = KarCul
package.name = karcul
package.domain = org.karcul
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 1
icon = icon.png
android.permissions = INTERNET, VIBRATE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 28c
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1