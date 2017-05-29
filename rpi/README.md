The newest (and best) one is panorama11.py

Needs both opencv and opencv_contrib to run. 
Reference: http://www.pyimagesearch.com/2015/07/16/where-did-sift-and-surf-go-in-opencv-3/
            https://stackoverflow.com/questions/37517983/opencv-install-opencv-contrib-on-windows
            
1. Download opencv and extra to c:\opencv
2. Copy C:\opencv\build\python\2.7\x64\cv2.pyd to C:\Anaconda2\Lib
3. Setup system path for opencv
4. Download opencv_contrib from https://github.com/opencv/opencv_contrib and unzip in c:\opencv
5. Install cmake from https://cmake.org/download/
6. C:\opencv>cmake -DOPENCV_EXTRA_MODULES_PATH=C:\opencv\opencv_contrib-master\modules C:\opencv\sources


