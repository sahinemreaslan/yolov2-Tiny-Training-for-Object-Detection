'''

'''
import sensor, image, lcd, time
import KPU as kpu
from fpioa_manager import fm
from machine import UART

fm.register(10, fm.fpioa.UART1_TX, force=True)
#arduino mavi kablo rx
fm.register(11, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, None, 0, timeout=1000, read_buf_len=4096)




'''
default freq = "24000000" ----> 10fps to
freq = "6000000"  ----> 3 fps
'''
#sensor.skip_frames(n, [, time])
#Kamera ayarlarını değiştirdikten sonra kamera görüntüsünün sabit kalması için belirtilen kare sayısını atlayın veya belirtilen süre içinde görüntüyü atlayın
sensor.reset(freq=15000000, set_regs=True, dual_buff=True)

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_vflip(0)
#sensor.set_hmirror(1)
sensor.run(1)
#sensor.skip_frames(10)
#sensor.set_brightness(2)


my_class = ["hedef"]
task = kpu.load(0x300000)
anchors = [3.8125, 3.8125, 5.375, 5.375, 7.1875, 7.1875, 11.25, 11.3125, 9.125, 9.125]
#my model weights
#a = kpu.init_yolo2(task, 0.2, 0.3, 5, anchors)
#(task,thresh,box_iou threshold,weights/2,anchors)
a = kpu.init_yolo2(task, 0.5, 0.5, 5, anchors)





while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task,img)
    img_merge = img.draw_cross(112,112,color = (255,0,0))
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect(),color = (0,255,0))
            a = img.draw_string( i.x(),i.y(),my_class[i.classid()],color = (255,0,0),scale = 3)
            #print(i.rect.rect())
            x = int (i.x()+(i.w()/2))
            y = int (i.y()+(i.h()/2))
            img.draw_cross(x,y,color = (255,0,0))


            if(x>=122):
                img.draw_string(112,112,"nesne sagda",color = (255,0,0),scale = 1)
                time.sleep_ms(100)# wait uart ready
                uart_A.write("l")
                time.sleep_ms(100)
            elif(102>=x):
                img.draw_string(112,112,"nesne solda",color = (255,0,0),scale = 1)
                time.sleep_ms(100)
                uart_A.write("r")
            else:
                img.draw_string(112,112,"nesne ortada",color = (255,0,0),scale = 1)
                time.sleep_ms(100)
                uart_A.write("s")
            #the recieved data is print lcd a screen
            if uart_A.any():
                    while uart_A.any():
                      read_data = uart_A.read()
                      print(read_data)
                      img.draw_string(200,3,read_data,color = (255,0,0),scale = 1)
            '''
            img.draw_string(200,3,uart_A.read(),color = (255,0,0),scale = 1)
            '''
        a = lcd.display(img)
    else:
        a = lcd.display(img)


a = kpu.deinit(task)
uart_A.deinit()
del uart_A

