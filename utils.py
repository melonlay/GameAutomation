from PIL import Image
WIN_HANDLES = None
import numpy as np
import cv2
WNAME=None

def capture_win_alt(window_name,change=True):
    # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui
    global WIN_HANDLES,WNAME
    if change:
        WIN_HANDLES=None
    from ctypes import windll

    import win32gui
    import win32ui

    if WIN_HANDLES is None:
        assert window_name is not None
        WNAME=window_name
        #print("Acquiring window handle")
        windll.user32.SetProcessDPIAware()
        hwnd = win32gui.FindWindow(None, window_name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top
        #print(f"Client rect: {left}, {top}, {right}, {bottom}")

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)

        WIN_HANDLES = (hwnd, hwnd_dc, mfc_dc, save_dc, bitmap)

    (hwnd, hwnd_dc, mfc_dc, save_dc, bitmap) = WIN_HANDLES
    save_dc.SelectObject(bitmap)

    # If Special K is running, this number is 3. If not, 1
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)

    im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

    if result != 1:
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        WIN_HANDLES = None
        raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

    open_cv_image = np.array(im,dtype=np.float32)/255.
    return open_cv_image