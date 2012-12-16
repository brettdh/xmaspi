#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# TODO: implement with pyqt.
class EmulatedBulb(QWidget):
    def __init__(self):
        super(EmulatedBulb, self).__init__()
        self.__color = (0.,0.,0.,0.) # RGBA

        self.__geometry = (0, 0, 10, 10)
        #self.setGeometry(*self.__geometry)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        
        qp.setPen(Qt.black)
        
        qcolor = QColor(*self.__color)
        qp.setBrush(qcolor)
        qp.drawEllipse(*self.__geometry)
        
        qp.end()

    def setColor(self, brightness, red, green, blue):
        # brightness: 0-255
        # red, green, blue: 0-15
        self.__color = (self.__getColor(red),
                        self.__getColor(green),
                        self.__getColor(blue),
                        brightness)
        self.update()
        
    def __getColor(self, color_value):
        return (color_value / 15.0) * 255.0

class EmulatorGui(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.__bulbs = []

        self.setGeometry(0, 0, 1100, 110)
        
        self.__layout = QHBoxLayout(self)
        self.__layout.setSpacing(0)

    def addBulb(self, bulb):
        self.__bulbs.append(bulb)
        self.__layout.addWidget(bulb)

STRAND_LEN = 50

# Keeps a mapping between LED Ids (0-N*50) to (strand, addr) pairs
class Emulator(object):
    # Strand orientations are arrays of either 1 or -1,
    # for each strand.
    # A strand with a -1 orientation will address 
    def __init__(self, strand_orientations=[-1, 1], \
                 strand_order=[0, 1], do_init=False):

        self.__bulbs = [None] * (len(strand_orientations) * STRAND_LEN)
        self.num_strands = 1
        if strand_orientations != None:
            self.num_strands = len(strand_orientations)
        self.initialize(strand_orientations, strand_order, do_init)
    
    # Initialize physical address on the strand
    # and the mapping from led_id to physical addr (strand, addr)
    # strand order is either [0, 1] or [1, 0]
    def initialize(self, strand_orientations=None, strand_order=None, do_init=False):
        
        # Default strand orientation ascending
        if strand_orientations == None:
            strand_orientations = [1]*strand_orientations

        if strand_order == None:
            strand_order = [0, 1]

        self.__gui = EmulatorGui()

        #self.phys_addr = {} 
        led_id = 0
        for index in range(len(strand_orientations)):
            orientation = strand_orientations[index]
            if orientation == 1:
                addr = 0
            else:
                addr = STRAND_LEN - 1

            for i in range(STRAND_LEN):
                # don't care about phys_addr; just position on screen
                #self.phys_addr[led_id] = (strand_order[index], addr)
                
                self.__bulbs[led_id] = EmulatedBulb()
                self.__gui.addBulb(self.__bulbs[led_id])
                
                if do_init == True:
                    self.set_led_color(led_id, 0, 0, 0, 0)
                addr += orientation
                led_id += 1
                
        self.__gui.show()

    def set_led_color(self, led_id, brightness, red, green, blue):
        self.__bulbs[led_id].setColor(brightness, red, green, blue)

    def write_led(self, led_id, brightness, blue, green, red):
        if led_id == -1:
            # Broadcast
            #for s in range(self.num_strands):
            #    self.buffer_pkt((s, 63), brightness, 0, 0, 0)

            # XXX: I'm guessing that this should set all LEDs,
            # XXX: but I'm not sure, so I'll just leave it unimplemented.
            # XXX: (I don't see any code using it anyway.)
            raise Exception("Broadcast not supported with emulator")
        elif led_id == 100:
            # nop
            return
        else:
            # Unicast
            self.set_led_color(led_id, brightness, red, green, blue)
