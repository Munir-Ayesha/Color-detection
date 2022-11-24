#importing libraries
import argparse
import cv2
import pandas as pd

#instantiate the ArgumentParser object as ap
ap = argparse.ArgumentParser()

#we add our only argument. This is a required argument as is noted by required=True.
ap.add_argument('-i', '--image', required=True, help="Image Path")

#instructs Python and the argparse library to parse the command line arguments.
args = vars(ap.parse_args())

#saving image in variable
img_path = args['image']

#Reading image with opencv
img = cv2.imread(img_path)

#saving dataset in variable
csv_path = 'colors.csv'

#making list for column name of dataset
index = ['color','color_name','hex','R','G','B']

#Reading dataset with pandas
df = pd.read_csv(csv_path, names=index, header=None)

#adjusting image size
img = cv2.resize(img, (800,600))
clicked = False
r = g = b = xpos = ypos = 0

#creating function to get color name
def get_color_name(R,G,B):
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

#calculate the rgb values of the pixel which we double click.
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Setting mouse callback event on a window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

#creating func to update the color name and RGB values on the window whenever a double click event occurs.
while True:
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)
        text = get_color_name(r,g,b) + 'R = ' + str(r) + 'G = ' + str(g) + 'B = ' + str(b)
        cv2.putText(img, text, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        
        if r+g+b >= 600:
            cv2.putText(img, text, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()