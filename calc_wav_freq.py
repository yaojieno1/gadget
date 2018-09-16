# -*- coding: utf-8 -*-

import struct

filedir="D:/Music/"
filename="0913-harry-1.wav"

t = 0 # state
bbi = 0 # flag for enter into signal
c = 0   # cross ge shu
val = []

#  12242 -  28228
#  44269 -  60228
#  76279 -  92253
# 108342 - 124263
# 140261 - 156253
# 172329 - 188301
# 204342 - 220296
# 236356 - 

def init():
    global t, bbi, c
    
    t = 0
    bbi = 0
    c = 0

def clear():
    init()

def get_state(b):
    if b > 128:
        return 1
    elif b < 128:
        return -1
    else: # if b == 128:
        return 0

def hit_limit(b):
    if b >= 131:
        return 1
    if b <= 124:
        return -1
    return 0

def move_into_signal(bi):
    global t, bbi, c
    
    c = c + 7
    if t == 1:
        return
    t = 1
    bbi = bi


def calc_freq(i):
    global c, bbi

    freq = 8000.0 * c / (i - bbi)
    print "[calc_freq] begin(%d), end(%d), c(%d), freq(%f)" % (bbi, i, c, freq)
    return freq

def show_val():
    global val

    print "val: %d %d %d %d   %d %d %d %d" \
        % (val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7])
 
def send2record(f):
    global val

    bit = 0
    #if (f < 900):
    if (f < 790):
        bit = 0
    else:
        bit = 1
        
    val.append(bit)

    if len(val) == 8:
        show_val()

        x = 0
        for i in range(8):
            x = (x << 1)+ val[i]
        print hex(x) + " : " + chr(x)
        val = []

def move_into_no_signal(i):
    global bbi, t, c
    
    if t == 0:
        return

    if (bbi + 1900) > i and (bbi + 300) < i:
        return

    t = 0
    if c < 50:
        # print "[abort()] i(%d) bbi(%d) c(%d) too small, abort!" % (i, bbi, c)
        clear()
        return

    freq = calc_freq(i)

    send2record(freq)
    
    clear()
    


def proc(f):
    global bbi
    
    print "[proc()] input file: " + f.name
    header = f.read(42)
    l = f.read(4) # chunk count
    s = ord(l[3])*pow(2, 24) + ord(l[2])*pow(2, 16) + ord(l[1])*pow(2,8)+ord(l[0])
    print "[proc()] chunk size: 0x" + l.encode("hex") + " = " + str(s)

    init()

    b = ord(f.read(1)) # read each byte
    last_r = '1'
    r = '0'
    i = 0  # visit each chunk
    current_state = 0
    last_state = 0
    cross = 0
    hit_high = 0
    hit_low = 0
    bi = 0
    
    while i < s:
        current_state = get_state(b)
        if current_state == 0:
            i=i+1
            r = f.read(1)
            if len(r) == 0:
                break
            b = ord(r)                
            continue

        if last_state == 0:
            last_state = current_state

        if current_state != last_state:
            cross = cross + 1
            last_state = current_state

        hit = hit_limit(b)
        if hit == 1:
            hit_high = hit_high + 1
        elif hit == -1:
            hit_low = hit_low + 1

        for x in range(1):
            if cross >= 14: # 7 ge zhou qi
                if hit_high >= 2 or hit_low >= 2 or hit_high + hit_low >= 2: # liang ci chu ji shang xia xian
                    move_into_signal(bi) # you xin hao le
                    #if (bi>=10023 and bi<= 10717):
                    #    print "[in_signal][%d]hit_high=%d hit_low=%d i=%d bbi=%d" % (bi, hit_high, hit_low, i, bbi)
                else:
                    if (bi>=10023 and bi<= 10717):
                        print "[no_signal][%d]hit_high=%d hit_low=%d i=%d bbi=%d" % (bi, hit_high, hit_low, i, bbi)

                    if False == move_into_no_signal(bi): # mei xin hao le
                        break
            
                hit_high = 0
                hit_low = 0
                bi = i
                cross = 0

        i=i+1
        last_r = r 
        r = f.read(1)
        while i < s and len(r) != 0 and ord(last_r) == ord(r):
            #print '[i %d] last_r %d == r %d' % (i, ord(last_r), ord(r))
            i = i + 1
            last_r = r
            r = f.read(1)

        if len(r) == 0:
            break

        b = ord(r)

    clear()
    print("[finish()]")


def main():
    f=open(filedir+filename, "rb")
    try:
        proc(f)
    finally:
        f.close()


#val.append(1)
main()
