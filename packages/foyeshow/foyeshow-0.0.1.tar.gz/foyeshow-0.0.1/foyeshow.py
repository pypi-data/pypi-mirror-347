import ctypes
import ctypes.wintypes
import threading

WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
WM_KEYFIRST = 0x0100
WM_KEYLAST = 0x010

CW_USEDEFAULT = 0x80000000
IDC_ARROW = 32512
IDC_CROSS = 32515
IDI_APPLICATION = 32512
WHITE_BRUSH = 0

class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.wintypes.HWND),
        ("message", ctypes.wintypes.UINT),
        ("wParam", ctypes.wintypes.WPARAM),
        ("lParam", ctypes.wintypes.LPARAM),
        ("time", ctypes.wintypes.DWORD),
        ("pt", ctypes.wintypes.POINT)
    ]

class WNDCLASSEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("style", ctypes.c_uint),
        ("lpfnWndProc", ctypes.c_void_p),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", ctypes.c_void_p),
        ("hIcon", ctypes.c_void_p),
        ("hCursor", ctypes.c_void_p),
        ("hbrBackground", ctypes.c_void_p),
        ("lpszMenuName", ctypes.c_char_p),
        ("lpszClassName", ctypes.c_char_p),
        ("hIconSm", ctypes.c_void_p),
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", ctypes.wintypes.DWORD),
        ("biWidth", ctypes.wintypes.LONG),
        ("biHeight", ctypes.wintypes.LONG),
        ("biPlanes", ctypes.wintypes.WORD),
        ("biBitCount", ctypes.wintypes.WORD),
        ("biCompression", ctypes.wintypes.DWORD),
        ("biSizeImage", ctypes.wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.wintypes.LONG),
        ("biYPelsPerMeter", ctypes.wintypes.LONG),
        ("biClrUsed", ctypes.wintypes.DWORD),
        ("biClrImportant", ctypes.wintypes.DWORD)
    ]

class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ("rgbBlue", ctypes.wintypes.BYTE),
        ("rgbGreen", ctypes.wintypes.BYTE),
        ("rgbRed", ctypes.wintypes.BYTE),
        ("rgbReserved", ctypes.wintypes.BYTE)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 3)
    ]

class __shared_HInstanceMeta(type):
    _hInstance = None

    def __call__(cls, *args, **kwargs):
        if cls._hInstance is None:
            cls._hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        instance = super().__call__(*args, **kwargs)
        instance.hInstance = cls._hInstance
        return instance

class basic_window(metaclass=__shared_HInstanceMeta):
    WNDPROC = ctypes.WINFUNCTYPE(
        ctypes.c_long, 
        ctypes.c_void_p, 
        ctypes.c_uint, 
        ctypes.c_void_p, 
        ctypes.c_void_p
    )
    
    @staticmethod
    def WindowProc(hwnd, msg, wParam, lParam):
        hwnd = ctypes.c_void_p(hwnd)
        wParam = ctypes.c_void_p(wParam)
        lParam = ctypes.c_void_p(lParam)
        
        if msg == WM_CLOSE:
            return 0
        elif msg == WM_DESTROY:
            ctypes.windll.user32.PostQuitMessage(0)
            return 0
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
    
    hwnd : ctypes.wintypes.HWND = None

    def __init__(self, title_name: str, width: int, height: int) -> None:
        self._original_title = title_name
        self._class_name = (title_name + "::laofoye").encode('utf-16le')
        self._wndproc = basic_window.WNDPROC(basic_window.WindowProc)
        
        wc = WNDCLASSEX()
        wc.cbSize = ctypes.sizeof(WNDCLASSEX)
        wc.style = 0
        wc.lpfnWndProc = ctypes.cast(self._wndproc, ctypes.c_void_p)
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = self._hInstance
        wc.hIcon = ctypes.windll.user32.LoadIconW(None, IDI_APPLICATION)
        wc.hCursor = ctypes.windll.user32.LoadCursorW(None, IDC_CROSS)
        wc.hbrBackground = ctypes.windll.gdi32.GetStockObject(WHITE_BRUSH)
        wc.lpszMenuName = None
        wc.lpszClassName = self._class_name
        wc.hIconSm = ctypes.windll.user32.LoadIconW(None, IDI_APPLICATION)

        if not ctypes.windll.user32.RegisterClassExW(ctypes.byref(wc)):
            raise RuntimeError("Failed to register window class")
        
        self.hwnd = ctypes.windll.user32.CreateWindowExW(
            0,
            self._class_name,
            title_name.encode('utf-16le'),
            (0x00000000 | 0x00C00000 | 0x00080000 | 0x00040000 | 0x00020000 | 0x00010000),
            CW_USEDEFAULT, CW_USEDEFAULT,
            width, height,
            None,
            None,
            self._hInstance,
            None
        )

        if not self.hwnd:
            raise RuntimeError("Failed to create window")
        
        ctypes.windll.user32.ShowWindow(self.hwnd, 1)
        ctypes.windll.user32.UpdateWindow(self.hwnd)
    
    def __del__(self):
        self.close()
        
    def resize(self, width: int, height: int) -> None:
        if not self.is_open():
            raise RuntimeError("Window handle not available")
        
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
        
        new_width = width
        new_height = height
        
        flags = 0x0004 | 0x0010
        
        ctypes.windll.user32.SetWindowPos(
            self.hwnd,
            None,
            rect.left,
            rect.top,
            new_width,
            new_height,
            flags
        )
                
    def set_topmost(self, topmost: bool = True) -> None:
        if not self.is_open():
            raise RuntimeError("Window handle not available")

        HWND_NOTOPMOST = ctypes.wintypes.HWND(-2)
        HWND_TOPMOST = ctypes.wintypes.HWND(-1)
        
        flags = 0x0001 | 0x0002 | 0x0040
        
        ctypes.windll.user32.SetWindowPos(
            self.hwnd,
            HWND_TOPMOST if topmost else HWND_NOTOPMOST,
            0, 0, 0, 0,
            flags
        )
            
    def close(self):
        if hasattr(self, 'hwnd') and self.hwnd:
            ctypes.windll.user32.DestroyWindow(self.hwnd)
            self.hwnd = None
        
        if hasattr(self, '_class_name') and self._class_name:
            ctypes.windll.user32.UnregisterClassW(self._class_name, self._hInstance)
            self._class_name = None

    def set_title(self, new_title: str):
        if hasattr(self, 'hwnd') and self.hwnd:
            buffer = ctypes.create_unicode_buffer(new_title)
            ctypes.windll.user32.SetWindowTextW(self.hwnd, buffer)
            self._original_title = new_title
        else:
            raise RuntimeError("Window handle not available")
    
    def is_open(self) -> bool:
        return hasattr(self, 'hwnd') and bool(self.hwnd)
        
class gdi32:
    SRCCOPY = 0x00CC0020
    DIB_RGB_COLORS = 0
    GDI_ERROR = 0xFFFFFFFF

    @staticmethod
    def CreateCompatibleDC(hdc):
        result = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
        if not result:
            raise RuntimeError("Failed to create compatible DC")
        return result

    @staticmethod
    def CreateDIBSection(hdc, pbmi, usage, ppvBits, hSection, offset):
        result = ctypes.windll.gdi32.CreateDIBSection(hdc, pbmi, usage, ppvBits, hSection, offset)
        if not result:
            raise RuntimeError("Failed to create DIB section")
        return result

    @staticmethod
    def SelectObject(hdc, hgdiobj):
        result = ctypes.windll.gdi32.SelectObject(hdc, hgdiobj)
        if result == gdi32.GDI_ERROR:
            raise RuntimeError("Failed to select GDI object")
        return result

    @staticmethod
    def DeleteObject(hgdiobj):
        if not ctypes.windll.gdi32.DeleteObject(hgdiobj):
            raise RuntimeError("Failed to delete GDI object")

    @staticmethod
    def DeleteDC(hdc):
        if not ctypes.windll.gdi32.DeleteDC(hdc):
            raise RuntimeError("Failed to delete DC")

    @staticmethod
    def BitBlt(hdcDest, xDest, yDest, width, height, hdcSrc, xSrc, ySrc, rop):
        if not ctypes.windll.gdi32.BitBlt(hdcDest, xDest, yDest, width, height, hdcSrc, xSrc, ySrc, rop):
            raise RuntimeError("BitBlt operation failed")
        

class basic_render:
    def __init__(self, window):
        self.window = window
        self.current_width = 0
        self.current_height = 0
        self.current_channels = 0
        self.memdc = None
        self.hbitmap = None
        self.old_bitmap = None
        self.ppv_bits = None
        
        self.bmi = BITMAPINFO()
        self.bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        self.bmi.bmiHeader.biPlanes = 1
        self.bmi.bmiHeader.biBitCount = 24
        self.bmi.bmiHeader.biCompression = 0
        self.bmi.bmiHeader.biSizeImage = 0
        
        hdc = ctypes.windll.user32.GetDC(self.window.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        try:
            self.memdc = gdi32.CreateCompatibleDC(hdc)
        finally:
            ctypes.windll.user32.ReleaseDC(self.window.hwnd, hdc)

    def __del__(self):
        try:
            if self.memdc:
                if self.hbitmap:
                    gdi32.SelectObject(self.memdc, self.old_bitmap)
                    gdi32.DeleteObject(self.hbitmap)
                gdi32.DeleteDC(self.memdc)
        except Exception as e:
            print(f"Resource cleanup error: {str(e)}")

    def __call__(self, image):
        if not self.window.is_open():
            raise RuntimeError("Window is not open")
        
        if len(image.shape) not in (2, 3):
            raise ValueError("Image must be 1, 3, or 4 channel")
        
        height, width = image.shape[:2]
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        
        if channels == 1:
            self.bmi.bmiHeader.biBitCount = 8
        elif channels == 3:
            self.bmi.bmiHeader.biBitCount = 24
        elif channels == 4:
            self.bmi.bmiHeader.biBitCount = 32
        else:
            raise ValueError("Unsupported number of channels (must be 1, 3, or 4)")
        
        self.bmi.bmiHeader.biWidth = width
        self.bmi.bmiHeader.biHeight = -height
        
        if (width != self.current_width or 
            height != self.current_height or 
            channels != self.current_channels):
            
            if self.hbitmap:
                gdi32.SelectObject(self.memdc, self.old_bitmap)
                gdi32.DeleteObject(self.hbitmap)
            
            hdc_window = ctypes.windll.user32.GetDC(self.window.hwnd)
            ppv_bits = ctypes.c_void_p()
            self.hbitmap = gdi32.CreateDIBSection(
                hdc_window,
                ctypes.byref(self.bmi),
                gdi32.DIB_RGB_COLORS,
                ctypes.byref(ppv_bits),
                None, 0
            )
            ctypes.windll.user32.ReleaseDC(self.window.hwnd, hdc_window)
            
            self.old_bitmap = gdi32.SelectObject(self.memdc, self.hbitmap)
            self.ppv_bits = ppv_bits
            self.current_width = width
            self.current_height = height
            self.current_channels = channels
        
        if channels == 1:
            ctypes.memmove(self.ppv_bits, image.ctypes.data, image.nbytes)
        elif channels == 3:
            ctypes.memmove(self.ppv_bits, image.ctypes.data, image.nbytes)
        elif channels == 4:
            ctypes.memmove(self.ppv_bits, image.ctypes.data, image.nbytes)
        
        hdc = ctypes.windll.user32.GetDC(self.window.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        
        try:
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetClientRect(self.window.hwnd, ctypes.byref(rect))
            client_width = rect.right - rect.left
            client_height = rect.bottom - rect.top
            x = (client_width - width) // 2
            y = (client_height - height) // 2
            
            gdi32.BitBlt(hdc, x, y, width, height, self.memdc, 0, 0, gdi32.SRCCOPY)
        finally:
            ctypes.windll.user32.ReleaseDC(self.window.hwnd, hdc)

class basic_painter:
    def __init__(self, hwnd) -> None:
        self.hwnd = hwnd
        self._font_cache = {}
        self._default_font = None
        
    def __del__(self):
        for hfont in self._font_cache.values():
            gdi32.DeleteObject(hfont)
        self._font_cache.clear()

    def puttext(self, text: str, x: int, y: int, color: tuple = (0, 0, 0), 
                font_size: int = 12, font_name: str = "微软雅黑", font_weight: int = 400) -> None:
        hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        
        try:
            font_key = (font_name.lower(), font_size, font_weight)
            
            if font_key not in self._font_cache:
                hfont = ctypes.windll.gdi32.CreateFontW(
                    font_size, 0, 0, 0, font_weight, 0, 0, 0,
                    ctypes.windll.kernel32.GetACP(),
                    0, 0, 0, 0, font_name)
                
                if not hfont:
                    raise RuntimeError("创建字体失败")
                self._font_cache[font_key] = hfont
            
            hfont = self._font_cache[font_key]
                
            old_font = ctypes.windll.gdi32.SelectObject(hdc, hfont)
            if old_font == gdi32.GDI_ERROR:
                raise RuntimeError("无法选中字体到设备上下文")
            
            if not self._default_font:
                self._default_font = old_font
                
            bgr_color = (color[2] << 16) | (color[1] << 8) | color[0]
            ctypes.windll.gdi32.SetTextColor(hdc, bgr_color)
            ctypes.windll.gdi32.SetBkMode(hdc, 1)
            
            text_wide = ctypes.create_unicode_buffer(text)
            if not ctypes.windll.gdi32.TextOutW(hdc, x, y, text_wide, len(text)):
                raise RuntimeError("文本输出失败")
                
        finally:
            if 'old_font' in locals() and old_font != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, self._default_font)
            ctypes.windll.user32.ReleaseDC(self.hwnd, hdc)

    def putrect(self, left: int, top: int, right: int, bottom: int, 
                color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        
        try:
            if len(color) != 3:
                raise ValueError("Color must be a tuple of 3 integers (R, G, B)")
            bgr_color = (color[2] << 16) | (color[1] << 8) | color[0]
            
            hpen = ctypes.windll.gdi32.CreatePen(0, thickness, bgr_color)
            if not hpen:
                raise RuntimeError("Failed to create pen")
            
            old_pen = ctypes.windll.gdi32.SelectObject(hdc, hpen)
            if old_pen == gdi32.GDI_ERROR:
                raise RuntimeError("Failed to select pen into DC")
            
            hbrush = ctypes.windll.gdi32.GetStockObject(5)
            old_brush = ctypes.windll.gdi32.SelectObject(hdc, hbrush)
            if old_brush == gdi32.GDI_ERROR:
                raise RuntimeError("Failed to select brush into DC")
            
            if not ctypes.windll.gdi32.Rectangle(hdc, left, top, right, bottom):
                raise RuntimeError("Failed to draw rectangle")
        
        finally:
            if 'old_brush' in locals() and old_brush != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, old_brush)
            if 'old_pen' in locals() and old_pen != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, old_pen)
            
            if 'hpen' in locals():
                ctypes.windll.gdi32.DeleteObject(hpen)
            
            ctypes.windll.user32.ReleaseDC(self.hwnd, hdc)

    def put_line(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                 color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        
        try:
            if len(color) != 3:
                raise ValueError("Color must be a tuple of 3 integers (R, G, B)")
            bgr_color = (color[2] << 16) | (color[1] << 8) | color[0]
            
            hpen = ctypes.windll.gdi32.CreatePen(0, thickness, bgr_color)
            if not hpen:
                raise RuntimeError("Failed to create pen")
            
            old_pen = ctypes.windll.gdi32.SelectObject(hdc, hpen)
            if old_pen == gdi32.GDI_ERROR:
                raise RuntimeError("Failed to select pen into DC")
            
            prev_point = ctypes.wintypes.POINT()
            if not ctypes.windll.gdi32.MoveToEx(hdc, start_x, start_y, ctypes.byref(prev_point)):
                raise RuntimeError("MoveToEx failed")
            if not ctypes.windll.gdi32.LineTo(hdc, end_x, end_y):
                raise RuntimeError("LineTo failed")
        
        finally:
            if 'old_pen' in locals() and old_pen != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, old_pen)
            if 'hpen' in locals():
                ctypes.windll.gdi32.DeleteObject(hpen)
            ctypes.windll.user32.ReleaseDC(self.hwnd, hdc)

    def put_ring(self, left: int, top: int, right: int, bottom: int, 
                 color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not hdc:
            raise RuntimeError("Failed to get device context")
        
        try:
            if len(color) != 3:
                raise ValueError("Color must be a tuple of 3 integers (R, G, B)")
            bgr_color = (color[2] << 16) | (color[1] << 8) | color[0]
            
            hpen = ctypes.windll.gdi32.CreatePen(0, thickness, bgr_color)
            if not hpen:
                raise RuntimeError("Failed to create pen")
            
            old_pen = ctypes.windll.gdi32.SelectObject(hdc, hpen)
            if old_pen == gdi32.GDI_ERROR:
                raise RuntimeError("Failed to select pen into DC")
            
            hbrush = ctypes.windll.gdi32.GetStockObject(5)
            old_brush = ctypes.windll.gdi32.SelectObject(hdc, hbrush)
            if old_brush == gdi32.GDI_ERROR:
                raise RuntimeError("Failed to select brush into DC")
            
            if not ctypes.windll.gdi32.Ellipse(hdc, left, top, right, bottom):
                raise RuntimeError("Ellipse failed")
        
        finally:
            if 'old_brush' in locals() and old_brush != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, old_brush)
            if 'old_pen' in locals() and old_pen != gdi32.GDI_ERROR:
                ctypes.windll.gdi32.SelectObject(hdc, old_pen)
            if 'hpen' in locals():
                ctypes.windll.gdi32.DeleteObject(hpen)
            ctypes.windll.user32.ReleaseDC(self.hwnd, hdc)

class window(basic_window, basic_render, basic_painter):
    _instance_count = 0
    _instance_lock = threading.Lock()

    def __init__(self, title_name: str = "老佛爷", width: int = 640, height: int = 480) -> None:
        basic_window.__init__(self, title_name, width, height)
        basic_render.__init__(self, self)
        basic_painter.__init__(self, self.hwnd)

        with window._instance_lock:
            window._instance_count += 1

    @classmethod
    def instance_count(cls):
        with cls._instance_lock:
            return cls._instance_count
        
    def __del__(self):
        basic_painter.__del__(self)
        basic_render.__del__(self)
        basic_window.__del__(self)

        with window._instance_lock:
            window._instance_count -= 1
                
    def __bool__(self):
        return basic_window.is_open(self)
    
    def set_title(self, name : str) -> None:
        basic_window.set_title(self, name)

    def set_resize(self, width : int, height : int) -> None:
        basic_window.resize(self, width, height)

    def set_topmost(self, boolalpha : bool) -> None:
        basic_window.set_topmost(self, boolalpha)

    def put_image(self, data):
        basic_render.__call__(self, data)

    def put_text(self, text: str, x: int, y: int, color: tuple = (0, 0, 0), 
                 font_size: int = 12, font_name: str = "微软雅黑", font_weight: int = 400) -> None:
        basic_painter.puttext(self, text, x, y, color, font_size, font_name, font_weight)

    def put_rect(self, left: int, top: int, right: int, bottom: int, color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        basic_painter.putrect(self, left, top, right, bottom, color, thickness)
            
    def put_line(self, start_x: int, start_y: int, end_x: int, end_y : int, color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        basic_painter.put_line(self, start_x, start_y, end_x, end_y, color, thickness)

    def put_ring(self, left: int, top: int, right: int, bottom: int, color: tuple = (0, 0, 0), thickness: int = 1) -> None:
        basic_painter.put_ring(self, left, top, right, bottom, color, thickness)

    @staticmethod
    def refresh(delay_ms : int = 0):
        start_time = ctypes.windll.kernel32.GetTickCount()
        end_time = start_time + delay_ms

        msg = MSG()
        while True:
            if ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                if msg.message == WM_KEYDOWN or msg.message == WM_SYSKEYDOWN:
                    return msg.wParam

                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
            else:
                if delay_ms < 0:
                    return -1
                elif delay_ms == 0:
                    if not ctypes.windll.user32.PeekMessageW(
                        ctypes.byref(msg), None, WM_KEYFIRST, WM_KEYLAST, 0):
                        continue
                else:
                    current_time = ctypes.windll.kernel32.GetTickCount()
                    if current_time >= end_time:
                        return -1
                    continue

__all__ = ['window']

if __name__ == "__main__":
    import numpy as np
    from time import perf_counter as time
    from mss import mss
    import cv2

    win : window = window("老佛爷")
    win2 : window = window("老佛爷")

    im = cv2.imread("1.jpg")
    win2.put_image(im)


    sct = mss()
    count = 0
    while win:
        img = np.array(sct.grab({"top": 0, "left": 0, "width": 800, "height": 600}))

        t1 = time()

        win.put_image(img)
        FPS = f"FPS: {1000 // round((time() - t1) * 1_000, 6)}"

        count += 1
        win2.set_title(f"老佛爷 {count}")
        win2.set_topmost(True)


        win.set_topmost(True)
        win.set_resize(img.shape[1], img.shape[0])
        win.set_title("老佛爷: " + FPS)
        win.put_text(FPS, 10, 10, color=(255, 0, 0), font_size=40)
        win.put_rect(50, 50, 200, 150, color=(0, 255, 0), thickness=2)
        win.put_line(0, 0, 200, 200, color=(0, 0, 255), thickness=3)
        win.put_ring(100, 100, 200, 200, color=(255, 0, 0), thickness=2)

        window.refresh(-1) # 这个是静态方法  必须要周期性调用一次以维持所有窗口的活跃状态

        print(win.instance_count())