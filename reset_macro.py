import keyboard
import mouse
import time
import pygetwindow as gw
import ctypes
import atexit
import win32con
import win32gui

WS_OVERLAPPED =       0x00000000
WS_POPUP            = 0x80000000
WS_CHILD            = 0x40000000
WS_MINIMIZE         = 0x20000000
WS_VISIBLE          = 0x10000000
WS_DISABLED         = 0x08000000
WS_CLIPSIBLINGS     = 0x04000000
WS_CLIPCHILDREN     = 0x02000000
WS_MAXIMIZE         = 0x01000000
WS_CAPTION          = 0x00C00000  
WS_BORDER           = 0x00800000
WS_DLGFRAME         = 0x00400000
WS_VSCROLL          = 0x00200000
WS_HSCROLL          = 0x00100000
WS_SYSMENU          = 0x00080000
WS_THICKFRAME       = 0x00040000
WS_GROUP            = 0x00020000
WS_TABSTOP          = 0x00010000
WS_EX_DLGMODALFRAME     = 0x00000001
WS_EX_NOPARENTNOTIFY    = 0x00000004
WS_EX_TOPMOST           = 0x00000008
WS_EX_ACCEPTFILES       = 0x00000010
WS_EX_TRANSPARENT       = 0x00000020
WS_EX_MDICHILD          = 0x00000040
WS_EX_TOOLWINDOW        = 0x00000080
WS_EX_WINDOWEDGE        = 0x00000100
WS_EX_CLIENTEDGE        = 0x00000200
WS_EX_CONTEXTHELP       = 0x00000400
WS_EX_STATICEDGE        = 0x00020000

WS_MINIMIZEBOX      = 0x00020000
WS_MAXIMIZEBOX      = 0x00010000


WS_OVERLAPPEDWINDOW =  (WS_OVERLAPPED     | 
                             WS_CAPTION        | 
                             WS_SYSMENU        | 
                             WS_THICKFRAME     | 
                             WS_MINIMIZEBOX    | 
                             WS_MAXIMIZEBOX)

SWP_NOSIZE         = 0x0001
SWP_NOMOVE          = 0x0002
SWP_NOREDRAW =         0x0008
SWP_NOZORDER =         0x0004
SWP_NOACTIVATE =       0x0010
SWP_FRAMECHANGED =     0x0020  
SWP_SHOWWINDOW =       0x0040
SWP_HIDEWINDOW =       0x0080
SWP_NOCOPYBITS =       0x0100
SWP_NOOWNERZORDER =    0x0200  
SWP_NOSENDCHANGING =   0x0400  

instanceWidth = 1920
instanceHeight = 540
instanceLock = [0,0,0]

cmd_window = gw.getWindowsWithTitle('cmd')[0]

windows = gw.getWindowsWithTitle('Minecraft')
if(windows.__len__() == 0):
    windows = gw.getWindowsWithTitle('instance')

if(windows.__len__() > 2):
    instanceHeight = 362

def setInstancesInPlace():
    windows[0].moveTo(0,0)
    win32gui.SetWindowText(windows[0]._hWnd, 'instance 1')
    windows[0].resizeTo(instanceWidth, instanceHeight)
    windows[1].moveTo(0,instanceHeight)
    win32gui.SetWindowText(windows[1]._hWnd, 'instance 2')
    windows[1].resizeTo(instanceWidth, instanceHeight)
    if(windows.__len__() > 2):
        windows[2].moveTo(0,instanceHeight*2)
        win32gui.SetWindowText(windows[2]._hWnd, 'instance 3')
        windows[2].resizeTo(instanceWidth, instanceHeight)


def resetUnfocusedWorld():
    keyboard.press_and_release('tab, tab, tab, tab, tab, tab, tab, tab, enter')

def resetWorld():
    keyboard.press_and_release('esc, tab, tab, tab, tab, tab, tab, tab, tab, tab, enter')
    time.sleep(1.2)
    setInstancesInPlace()
    keyboard.press_and_release('f3+esc')

def resetWorldPreview():
    keyboard.press_and_release('page down')
    time.sleep(0.8)
    keyboard.press_and_release('f3+esc')

def toggleF3Down():
    keyboard.press('f3')

def toggleF3Up():
    keyboard.release('f3')
def toggleF3Once():
    keyboard.press_and_release('f3', 1, 1)

keyboard.add_hotkey('decimal', resetWorld, args=())
keyboard.add_hotkey('page down', resetWorldPreview, args=())

lStyle = ctypes.windll.user32.GetWindowLongA(windows[0]._hWnd, -16)
lExStyle = ctypes.windll.user32.GetWindowLongA(windows[0]._hWnd, -20)

lStyle &= ~(WS_BORDER | WS_DLGFRAME | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU)
lExStyle &= ~(WS_EX_DLGMODALFRAME |
                  WS_EX_WINDOWEDGE | WS_EX_CLIENTEDGE | WS_EX_STATICEDGE)

ctypes.windll.user32.SetWindowLongA(windows[0]._hWnd, -16, lStyle | WS_OVERLAPPED | WS_VISIBLE | WS_SYSMENU)
ctypes.windll.user32.SetWindowLongA(windows[1]._hWnd, -16, lStyle | WS_OVERLAPPED | WS_VISIBLE | WS_SYSMENU)
if(windows.__len__() > 2):
    ctypes.windll.user32.SetWindowLongA(windows[2]._hWnd, -16, lStyle | WS_OVERLAPPED | WS_VISIBLE | WS_SYSMENU)


ctypes.windll.user32.SetWindowLongA(windows[0]._hWnd, -20, WS_EX_TOPMOST)
ctypes.windll.user32.SetWindowLongA(windows[1]._hWnd, -20, WS_EX_TOPMOST)
if(windows.__len__() > 2):
    ctypes.windll.user32.SetWindowLongA(windows[2]._hWnd, -20, lExStyle | WS_EX_TOPMOST)


ctypes.windll.user32.SetWindowPos(windows[1]._hWnd, -1, 0, 0, 0, 0,  SWP_NOOWNERZORDER|SWP_NOZORDER|SWP_NOSIZE|SWP_NOMOVE|SWP_FRAMECHANGED)
setInstancesInPlace()

def doWindowFocus(index):
    #windows[index].activate()
    if windows[index].isActive == False:
        windows[index].activate()


def goInstance1():
    doWindowFocus(0)
    instanceLock[0] = 0
    #windows[0].maximize()
    windows[0].moveTo(0,0)
    windows[0].resizeTo(1920, 1080)
    win32gui.SetWindowText(windows[0]._hWnd, 'instance 1')

def goInstance2():
    doWindowFocus(1)
    instanceLock[1] = 0
    #windows[1].maximize()
    windows[1].moveTo(0,0)
    windows[1].resizeTo(1920, 1080)
    win32gui.SetWindowText(windows[1]._hWnd, 'instance 2')

def goInstance3():
    doWindowFocus(2)
    #windows[1].maximize()
    windows[2].moveTo(0,0)
    windows[2].resizeTo(1920, 1080)
    win32gui.SetWindowText(windows[2]._hWnd, 'instance 3')

    
def resetInstance1():
    if(instanceLock[0]):
        return
    windows[1].restore()
    windows[1].moveTo(0,instanceHeight)
    windows[1].resizeTo(instanceWidth, instanceHeight)
    doWindowFocus(0)
    windows[0].restore()
    windows[0].moveTo(0,0)
    windows[0].resizeTo(instanceWidth, instanceHeight)
    resetUnfocusedWorld()
    win32gui.SetWindowText(windows[0]._hWnd, 'instance 1')
    cmd_window.activate()
def resetInstance2():
    if(instanceLock[1]):
        return
    windows[0].restore()
    windows[0].moveTo(0,0)
    windows[0].resizeTo(instanceWidth, instanceHeight)
    doWindowFocus(1)
    windows[1].restore()
    windows[1].moveTo(0,instanceHeight)
    windows[1].resizeTo(instanceWidth, instanceHeight)
    resetUnfocusedWorld()
    win32gui.SetWindowText(windows[1]._hWnd, 'instance 2')
    cmd_window.activate()
def resetInstance3():
    doWindowFocus(2)
    windows[2].restore()
    windows[2].moveTo(0,instanceHeight*2)
    windows[2].resizeTo(instanceWidth, instanceHeight)
    resetUnfocusedWorld()
    win32gui.SetWindowText(windows[2]._hWnd, 'instance 3')
    cmd_window.activate()


#save system cursor, before changing it
cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 
                            0, 0, win32con.LR_SHARED)
save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR, 
                            0, 0, win32con.LR_COPYFROMRESOURCE)

def restore_cursor():
    ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(save_system_cursor)

#Make sure cursor is restored at the end
atexit.register(restore_cursor)

#change system cursor
cursor = win32gui.LoadImage(0, 32515, win32con.IMAGE_CURSOR, 
                            0, 0, win32con.LR_SHARED)
ctypes.windll.user32.SetSystemCursor(cursor, 32512)
ctypes.windll.user32.DestroyCursor(cursor)

def keyhook(event):
    if(event.name == 'home' and event.event_type == 'up'):
        instanceLock[0] = 1
    if(event.name == 'up' and event.event_type == 'up'):
        instanceLock[1] = 1
    if(event.name == 'down' and event.event_type == 'up'):
        resetInstance2()
    if(event.name == 'end' and event.event_type == 'up'):
        resetInstance1()
    if(event.name == 'page down' and event.event_type == 'up'):
        resetInstance3()
    if(event.name == 'left' and event.event_type == 'up'):
        goInstance1()
    if(event.name == 'clear' and event.event_type == 'up'):
        goInstance2()
    if(event.name == 'right' and event.event_type == 'up'):
        goInstance3()

keyboard.hook(keyhook)


def mousehook(event):
    if(type(event) == mouse.ButtonEvent):
        if(event.button == 'x' and event.event_type == 'down'):
            toggleF3Down()
        elif(event.button == 'x' and event.event_type == 'up'):
            toggleF3Once()


#mouse.hook(mousehook)

while True:
    time.sleep(5)
    if(windows[0].title != 'instance 1'):
        win32gui.SetWindowText(windows[0]._hWnd, 'instance 1')
    if(windows[1].title != 'instance 2'):
        win32gui.SetWindowText(windows[1]._hWnd, 'instance 2')
    if(windows.__len__() > 2 and windows[2].title != 'instance 3'):
        win32gui.SetWindowText(windows[2]._hWnd, 'instance 3')
