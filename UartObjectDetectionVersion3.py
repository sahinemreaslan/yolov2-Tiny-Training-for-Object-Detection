import sensor, image, lcd, time
import KPU as kpu
from fpioa_manager import fm
from machine import UART
#<--------------- Mapping FPİO - Start ---------------->
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(11, fm.fpioa.UART1_RX, force=True)
#<--------------- Mapping FPİO - End ---------------->

#<--------------- UART İnit - Start ---------------->
uart_A = UART(UART.UART1, 115200, 8, None, 0, timeout=1000, read_buf_len=4096)
#<--------------- UART İnit - End ---------------->



'''
default freq = "24000000" ----> 10fps to
freq = "6000000"  ----> 3 fps
'''

#sensor.skip_frames(10)
'''
sensor.skip_frames(n, [, time])

Kamera ayarlarını değiştirdikten sonra kamera görüntüsünün sabit kalması için
belirtilen kare sayısını atlayın veya belirtilen süre içinde görüntüyü atlayın
'''
sensor.reset(freq=6000000, set_regs=True, dual_buff=True)

sensor.set_vflip(1)


sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.skip_frames(3)
#sensor.set_hmirror(1)
sensor.run(1)
#sensor.set_brightness(2)

'''

clock.tick()
img = sensor.snapshot()
fps =clock.fps()
img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
lcd.display(img)

'''



my_class = ["hedef"]
task = kpu.load(0x300000)
anchors = [3.8125, 3.8125, 5.375, 5.375, 7.1875, 7.1875, 11.25, 11.3125, 9.125, 9.125]
#my model weights
#a = kpu.init_yolo2(task, 0.2, 0.3, 5, anchors)
#(task,thresh,box_iou threshold,weights/2,anchors)
a = kpu.init_yolo2(task, 0.5, 0.5, 5, anchors)

sayac1 = 0
sayac2 = 0
sayac3 = 0


def GarbageCollector():
    a = kpu.deinit(task)
    uart_A.deinit()
    del uart_A

def PositionTransmitBuffer(sayac1,sayac2,sayac):
    #Send Recivier Buffer (to Arduino)
    if sayac1 > sayac2 and sayac1 > sayac3:
        uart_A.write("l")
    elif sayac2 > sayac3 and sayac2 > sayac1:
        uart_A.write("r")
    elif sayac3 > sayac1 and sayac3 > sayac2:
        uart_A.write("s")


while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task,img)
    #<-------------------------İmg Center Cross - Start --------------------------->#
    img_merge = img.draw_cross(112,112,color = (255,0,0))
    #<-------------------------İmg Center Cross - End --------------------------->#

    if code:
        for i in code:
            #<-------------------------Bounding Box Draw - Start --------------------------->#
            a = img.draw_rectangle(i.rect(),color = (0,255,0))
            a = img.draw_string( i.x(),i.y(),my_class[i.classid()],color = (255,0,0),scale = 3)
            #<-------------------------Bounding Box Draw - Start --------------------------->#
            x = int (i.x()+(i.w()/2))
            y = int (i.y()+(i.h()/2))
            img.draw_cross(x,y,color = (255,0,0))
            #<-------------------------Object Position - Start --------------------------->#
            '''
            if sayac1 == 4 or sayac2 == 4 or sayac3 == 4:
                PositionBuffer(sayac1,sayac2,sayac3)
            '''
            if(x>=125):
                img.draw_string(112,112,"nesne sagda",color = (255,0,0),scale = 1)
                sayac1+= 1
            elif(99>=x):
                img.draw_string(112,112,"nesne solda",color = (255,0,0),scale = 1)
                sayac2+= 1
            else:
                img.draw_string(112,112,"nesne ortada",color = (255,0,0),scale = 1)
                sayac3+= 1
            #the recieved data is print lcd a screen
            #<-------------------------Object Position - End --------------------------->#
        a = lcd.display(img)
    else:
        a = lcd.display(img)


GarbageCollector()
