import ctypes

def isDarkModeEnabled():
    try:
        # Constants and shit
        HKEY_CURRENT_USER = 0x80000001
        KEY_QUERY_VALUE = 0x0001

        # Open the registry key containing the preferred app mode
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = ctypes.c_void_p()
        reg_result = ctypes.windll.advapi32.RegOpenKeyExW(HKEY_CURRENT_USER, key_path, 0, KEY_QUERY_VALUE, ctypes.byref(key))

        if reg_result == 0:
            # Read AppsUseLightTheme registry key
            value_type = ctypes.c_ulong()
            value = ctypes.c_ulong()
            buffer_size = ctypes.c_ulong(ctypes.sizeof(value))
            reg_result = ctypes.windll.advapi32.RegQueryValueExW(key, "AppsUseLightTheme", None, ctypes.byref(value_type),
                                                                 ctypes.cast(ctypes.byref(value), ctypes.POINTER(ctypes.c_ubyte)),
                                                                 ctypes.byref(buffer_size))

            if reg_result == 0 and value_type.value == 4:  # Check that the value type is DWORD
                return value.value == 0  # 0 = dark mode is enabled

        return None

    except Exception as e:
        return None
