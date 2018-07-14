#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import urllib
from PIL import Image

picPath = './pics/'
fontPath = './fonts/'
modPath = './mods/'

'''
发现有一种很简单的验证码，不需要什么难度就能100%识别...写了个批量识别的脚本...
'''

def getPics(num):
    for i in range(num):
        print 'downloading ', i
        file('./pics/%04d.gif' % i, 'wb').write(urllib.urlopen('url-for-captcha').read())

def binary(threshold):
    for f in os.listdir(picPath):
        if f.endswith('.gif'):
            img = Image.open(picPath + f)
            pixdata = img.load()
            for y in xrange(img.size[1]):
                for x in xrange(img.size[0]):
                    if pixdata[x, y][0] < threshold[0] or pixdata[x, y][1] < threshold[1]:
                        pixdata[x, y] = (0, 0, 0, 255)
                    else:
                        pixdata[x, y] = (255, 255, 255, 255)
            img.save(picPath + f)

def division():
    counter = 1
    nums = []
    for f in os.listdir(picPath):
        if f.endswith('.gif'):
            img = Image.open(picPath + f)
            for i in range(4):
                num = img.crop((13 * i + 5, 3, 13 * i + 18, 17))
                num.save(fontPath + 'font%d.gif' % counter)
                counter += 1
                nums.append(num)

    return nums

def recognize(nums):
    result = ''
    results = []
    mods = []
    for i in range(10):
        mods.append((str(i), Image.open(modPath + '%d.gif' % i)))

    nums = division()
    for num in nums:
        points = []
        for mod in mods:
            diffs = 0
            for y in range(14):
                for x in range(13):
                    if mod[1].getpixel((x, y)) != num.getpixel((x, y)):
                        diffs += 1
            points.append((diffs, mod[0]))
        points.sort()
        result += points[0][1]
        if len(result) % 4 == 0:
            results.append(result)
            result = ''

    return results

if __name__ == '__main__':
    getPics(10)
    binary([90, 136])
    nums = division()
    results = recognize(nums)
    print results
