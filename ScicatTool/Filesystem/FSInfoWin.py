import win32api
import win32con
import win32security


def get_ownername(filename):
    sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
    name, _, _ = win32security.LookupAccountSid(None, sd.GetSecurityDescriptorOwner())
    return name
