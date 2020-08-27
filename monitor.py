
import win32gui
import win32con
import win32api
import cv2 
import server
import numpy as np

def windowEnumerationHandler(hwnd, top_windows):
	if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
		if(win32gui.GetWindowText(hwnd)!=''):
			top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
			ss = win32gui.GetWindowPlacement(hwnd)
			if(ss[4][0]<0):
				second_monitor.append((hwnd,ss[4]))
			else:
				main_monitor.append((hwnd,ss[4]))
top_windows = []
main_monitor=[]
second_monitor=[]
win32gui.EnumWindows(windowEnumerationHandler, top_windows)

cap = cv2.VideoCapture(0)
PINK_MIN = np.array([170, 120, 70], np.uint8)
PINK_MAX = np.array([180, 255, 255], np.uint8)
PINK_MIN1 = np.array([0, 120, 70], np.uint8)
PINK_MAX1 = np.array([10, 255, 255], np.uint8)
centroid_x = 0
centroid_y = 0
s = 'heavy right'
move = ''

while(cap.isOpened()):

    ret, img = cap.read()
    img = cv2.flip(img, 2)
    #thresh = cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
    orig = cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original',200,200)
    #img = cv2.GaussianBlur(img, (15, 15), 0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    """
    Use this for thresholding using Otsu's Binarization method
    """
    # grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, frame_threshed = cv2.threshold(grey, 127, 255,
    #                        cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    mask1 = cv2.inRange(hsv, PINK_MIN, PINK_MAX)
    mask2 = cv2.inRange(hsv, PINK_MIN1, PINK_MAX1)
    mask = mask1+mask2
    mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
    image,contours,hierarcy = cv2.findContours(mask, 1, 2)
    max_area = 0
    last_x = centroid_x
    last_y = centroid_y

    if contours:
        for i in contours:
            area = cv2.contourArea(i)
            if area > max_area:
                max_area = area
                cnt = i

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        centroid_x = (x + x+w)/2
        centroid_y = (y + y+h)/2

        cv2.circle(img, (int(centroid_x), int(centroid_y)), 2, (0,0,255), 2)
        # cv2.line(img,(400,0),(400,700),(255,0,0),5)
        # cv2.line(img,(900,0),(900,700),(255,0,0),5)
        # cv2.line(img,(400,350),(900, 350),(255,0,0),5)

        #cv2.imshow('Threshold', frame_threshed)
        cv2.imshow('Original', img)


        """
        This method uses self defined quadrants. It finds the location of
        the centroid of bounding rectangle among the quadrants and simulates
        appropriate move.
        """
        # up-down move
        # if centroid_x >= 400 and centroid_x <= 900:
        #     # up
        #     if centroid_y >= 0 and centroid_y <= 350:
        #         print ('up')
               
        #     # down
        #     if centroid_y >= 350 and centroid_y <=700:
        #         print ('down')
               

        # # left-right move
        # if centroid_y >= 0 and centroid_y <= 700:
        #     # left
        #     if centroid_x >= 0 and centroid_x <= 400:
        #         print ('left')
               
        #     # right
        #     if centroid_x >= 900:
        #         print ('right')
               


        """
        This method checks if there is a change in the coordinates of the
        centroid of bounding rectangle by some specific threshold in x or y
        axis and then simulates appropriate move.
        """

        ##right-left move
        window = win32gui.GetForegroundWindow()
        left,top,right,bottom = win32gui.GetWindowRect(window)
        # print(f'{left},{top},{right},{bottom}')
        width=1360
        height=760
   #      if(left<0 and left!=-8):
   #      	if(width>1366):
   #      			width=1366
			# if(height > 768):
			# 	height=766
			# win32gui.MoveWindow(window,0,0,width,height,True)
			# win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
		# else:
		# 	win32gui.MoveWindow(window,-1920,0,1920,1080,True)
		# 	win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
        diff_x = centroid_x - last_x
        
        if diff_x<=250 and diff_x>=150:
        	if(s!='heavy right'):
        		# server.start()
        		print('heavy right')
        	s='heavy right'
        elif diff_x >= 68 and diff_x<140:
           if(s!='right'):
         	  print ('right')
         	  # server.start()
         	  if(width>1366):
         	  	width=1366
         	  if(height > 768):
         	  	height=766
         	  win32gui.MoveWindow(window,0,0,width,height,True)
         	  win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
           # pyautogui.press('right')
           s = 'right'
        if diff_x <= -60:
           if(s!='left'):
           	print ('left')
           	win32gui.MoveWindow(window,-1920,0,1920,1080,True)
           	win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
           # pyautogui.press('left')
           s = 'left'


        #up-down move
        # diff_y = centroid_y - last_y
        # if diff_y >= 30:
        #    print ('down')
        #    # pyautogui.press('down')
        #    s = 'down'
        # elif diff_y <= -30:
        #    print ('up')
        #    # pyautogui.press('up')
        #    s = 'up'
        move = s

    k = cv2.waitKey(10)
    if k == 27:
        break


  
# define a video capture object 
# vid = cv2.VideoCapture(0) 
  
# while(True): 
      
#     # Capture the video frame 
#     # by frame 
#     ret, frame = vid.read() 
  
#     # Display the resulting frame 
#     cv2.imshow('frame', frame) 
      
#     # the 'q' button is set as the 
#     # quitting button you may use any 
#     # desired button of your choice 
#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         break
  
# # After the loop release the cap object 
# vid.release() 
# # Destroy all the windows 
# cv2.destroyAllWindows() 





# def windowEnumerationHandler(hwnd, top_windows):
# 	if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
# 		if(win32gui.GetWindowText(hwnd)!=''):
# 			top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
# 			ss = win32gui.GetWindowPlacement(hwnd)
# 			if(ss[4][0]<0):
# 				second_monitor.append((hwnd,ss[4]))
# 			else:
# 				main_monitor.append((hwnd,ss[4]))
# top_windows = []
# main_monitor=[]
# second_monitor=[]
# win32gui.EnumWindows(windowEnumerationHandler, top_windows)
# print(top_windows)
# print(f'first: {main_monitor}\nsecond: {second_monitor}')
# main_monitor.pop(0)
# print(f'after pop {main_monitor}')


# print (win32gui.GetWindowRect(top_windows[0][0]))
# print (win32gui.GetWindowRect(win32gui.GetForegroundWindow()))
# window = win32gui.FindWindowEx(None, None, None, 'How can I maximize a specific window with Python? - Stack Overflow - Google Chrome')
# window = win32gui.GetForegroundWindow()
# left,top,right,bottom = win32gui.GetWindowRect(window)
# print(f'{left},{top},{right},{bottom}')
# width=1360
# height=760
# if(left<0 and left!=-8):
# 	if(width>1366):
# 		width=1366
# 	if(height > 768):
# 		height=766	
# 	win32gui.MoveWindow(window,0,0,width,height,True)
# 	win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
# else:
# 	win32gui.MoveWindow(window,-1920,0,1920,1080,True)
# 	win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
# monitors = win32api.EnumDisplayMonitors()
# print(monitors)
# for i in range(len(monitors)):
# 	print(win32api.GetMonitorInfo(monitors[i][0]))