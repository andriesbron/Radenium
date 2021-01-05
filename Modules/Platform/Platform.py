try:
    import pycom
    _PLATFORM_ = "PYCOM"
    _PLATFORM_VER_ = "3.0"
    _PLATFORM_REL_ = "1.2"

except:
    import platform
    _PLATFORM_ = platform.system()
    _PLATFORM_VER_ = ""
    _PLATFORM_REL_ = platform.release()

class Platform:
    def automator(self):
        return []

    def system(self):
        return {"platform":_PLATFORM_, "version":_PLATFORM_VER_, "release":_PLATFORM_REL_}


