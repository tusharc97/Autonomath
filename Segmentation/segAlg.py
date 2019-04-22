from PIL import Image
import json, sys
from fixEq import createAlliances

# Struct for bounding box for each digit and value
class Digit(object):
    def __init__(self):
        self.value = None
        self.top = None
        self.left = None
        self.right = None
        self.bottom = None
        self.position = 0 # 0 is inline, 1 is super, 2 is sub


last_label = None # Last label assigned to a potential bounding box

def segmentation(image_link):

    # Image Loading
    im = Image.open(image_link)
    im = im.convert('1')

    output = dict()
    eq_table = dict()


    # Getting pixel data 
    width, height = im.size
    im_data = list(im.getdata())
    im_data = [im_data[i * width:(i + 1) * width] for i in range(height)]
    pixels = []

    # Converting pixel data to binary values
    for row in range(height):
        curr_row = []
        for col in range(width):
            val = im_data[row][col]
            if(val < 10):
                val = 0
                label = None # Unlabelled pixel
            else:
                val = 255
                label = -1 # Background pixel
            curr_row += [[val,label]] # pixel value, digit_class
        pixels += [curr_row]

    # First rounding of labeling pixels
    for row in range(height):
        for col in range(width):
            pixel = pixels[row][col]
            val = pixel[0]
            label = pixel[1]
            if(val == 0):
                # Foreground pixel

                # Checks all the neighbors and gives the lowest label
                # and all neighboring labels (which are all equivalent)
                new_label, labels = checkNeighbors(pixels, row, col)
                pixels[row][col] = [val, new_label] # Assigning new label

                #Update equivalence table with new equivalences
                eq_table[new_label] = addList2Set(labels, eq_table.get(new_label, set()))
                if(new_label in eq_table[new_label]):
                    # print(eq_table)
                    eq_table[new_label].remove(new_label)

    # Second pass of labelling
    for row in range(height):
        for col in range(width):
            pixel = pixels[row][col]
            val = pixel[0]
            label = pixel[1]
            if(val == 0):
                # Background pixel
                new_label, labels = checkNeighbors(pixels, row, col)
                pixels[row][col] = [val, new_label]
            label = pixel[1]
            if(output.get(label, None) == None):
                # First time assigning that label
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
    for key in bboxes:
        temp = dict()
        bbox = bboxes[key]
        # print(key, bbox)
        temp['startRow'] = bbox[0]
        temp['startCol'] = bbox[1]
        temp['endRow'] = bbox[2]
        temp['endCol'] = bbox[3]
        output += [temp]

    json.dump(output, sys.stdout)


def checkNeighbors(pixels, row, col):
    global last_label
    # Checks all neighbors of the pixels
    if(row == 0):
        print("oops")
    if(col == 0):
        print("oops!!")
    tl = pixels[row-1][col-1]
    t  = pixels[row-1][col]
    tr = pixels[row-1][col+1]
    l  = pixels[row][col-1]
    r  = pixels[row][col+1]
    bl = pixels[row+1][col-1]
    b  = pixels[row+1][col]
    br = pixels[row+1][col+1]
    neighbors = [tl,t,tr,l,r,bl,b,br]

    labels = [] # list of labels of neighbors
    for pix in neighbors:
        val = pix[0]
        label = pix[1]
        if(val == 0 and label != None):
            # Foreground, labelled pixel
            labels += [label]
    # print(labels)

    labels = list(set(labels)) # Get a list of unique labels
    if(labels != []):
        # If at least one of the pixels is labelled
        return min(labels), labels
    else:
        # No labelled neighbors
        if(last_label == None):
            # First pixel to get labelled in image
            last_label = 0
        else:
            # New digit and new bounding box
            last_label += 1
        return last_label, labels

def addList2Set(l, s):
    a = s
    for i in l:
        a.add(i)
    return a


def main():
    if(len(sys.argv) != 2):
        print("Too few or too many arguments!")

    file_name = sys.argv[1]
    all_bboxes, eq_table = segmentation(file_name)
    # Call Jessie's code
    eq_clean = createAlliances(eq_table)
    final_labels = []
    output = dict()
    for key in eq_clean:
        # Coalesce key-value pairs
        eq_keys = eq_clean[key]
        bsr, bsc, ber, bec = all_bboxes[key]
        for eq_key in eq_keys:
            sr, sc, er, ec = all_bboxes[eq_key]
            if(sr < bsr):
                bsr = sr
            if(sc < bsc):
                bsc = sc
            if(er > ber):
                ber = er
            if(ec > bec):
                bec = ec
        output[key] = [bsr, bsc, ber, bec]
    
    
    # print(eq_clean)
    # print()
    # print("-------")
    # print(all_bboxes, final_labels)
    
    # print(all_bboxes)
    # print()
    # print("-------")
    # print(output)
    createOutput(output)

main()