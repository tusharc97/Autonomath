from PIL import Image
import json, sys
from fixEq import createAlliances

class Digit(object):
    def __init__(self):
        self.value = None
        self.top = None
        self.left = None
        self.right = None
        self.bottom = None
        self.position = 0 # 0 is inline, 1 is super, 2 is sub


last_label = None

def segmentation(image_link):
    im = Image.open(image_link)
    im = im.convert('1')
    width, height = im.size
    output = dict()
    eq_table = dict()

    im_data = list(im.getdata())
    im_data = [im_data[i * width:(i + 1) * width] for i in range(height)]
    pixels = []
    for row in range(height):
        curr_row = []
        for col in range(width):
            val = im_data[row][col]
            if(val < 10):
                val = 0
                label = None
            else:
                val = 255
                label = -1
            curr_row += [[val,label]] # pixel value, digit_class
        pixels += [curr_row]

    for row in range(height):
        for col in range(width):
            pixel = pixels[row][col]
            val = pixel[0]
            label = pixel[1]
            if(val == 0):
                new_label, labels = checkNeighbors(pixels, row, col)
                pixels[row][col] = [val, new_label]
                eq_table[new_label] = addList2Set(labels, eq_table.get(new_label, set()))
                if(new_label in eq_table[new_label]):
                    # print(eq_table)
                    eq_table[new_label].remove(new_label)

    for row in range(height):
        for col in range(width):
            pixel = pixels[row][col]
            val = pixel[0]
            label = pixel[1]
            if(val == 0):
                new_label, labels = checkNeighbors(pixels, row, col)
                pixels[row][col] = [val, new_label]
            label = pixel[1]
            if(output.get(label, None) == None):
                output[label] = [row, col, row, col]
            else:
                sr, sc, er, ec = output[label]
                if(col < sc):
                    output[label] = [sr, col, er, ec]
                if(col > ec):
                    output[label] = [sr, sc, er, col]
                if(row > er):
                    output[label] = [sr, sc, row, ec]

    return output, eq_table

def createOutput(bboxes):
    temp = dict()
    output = []
    for bbox in bboxes:
        temp = dict()
        temp['startRow'] = bbox[0]
        temp['startCol'] = bbox[1]
        temp['endRow'] = bbox[2]
        temp['endCol'] = bbox[3]
        output += [temp]

    json.dump(output, sys.stdout)


def checkNeighbors(pixels, row, col):
    global last_label
    tl = pixels[row-1][col-1]
    t  = pixels[row-1][col]
    tr = pixels[row-1][col+1]
    l  = pixels[row][col-1]
    r  = pixels[row][col+1]
    bl = pixels[row+1][col-1]
    b  = pixels[row+1][col]
    br = pixels[row+1][col+1]
    neighbors = [tl,t,tr,l,r,bl,b,br]
    labels = []
    for pix in neighbors:
        val = pix[0]
        label = pix[1]
        if(val == 0 and label != None):
            labels += [label]
    # print(labels)
    labels = list(set(labels))
    if(labels != []):
        return min(labels), labels
    else:
        if(last_label == None):
            last_label = 0
        else:
            last_label += 1
        return last_label, labels

def addList2Set(l, s):
    a = s
    for i in l:
        a.add(i)
    return a


def main():
    all_bboxes, eq_table = segmentation("Testing Images/test.JPG")
    # Call Jessie's code
    eq_clean = createAlliances(eq_table)
    final_labels = []
    for key in eq_clean:
        label = min(list(eq_clean[key]))
        final_labels += [label]

    # Use that to fix bboxes
    bboxes = []
    # print(all_bboxes, final_labels)
    for key in final_labels:
        bboxes += [all_bboxes[key]]
    createOutput(bboxes)

main()