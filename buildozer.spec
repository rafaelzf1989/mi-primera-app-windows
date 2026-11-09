[app]
title = PTT Client
package.name = pttclient
package.domain = org.ptt
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.permissions = INTERNET
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
