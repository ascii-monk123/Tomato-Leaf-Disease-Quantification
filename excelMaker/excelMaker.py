import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import xlsxwriter

#quantification
def quantify(h_channel,totalLeafPix):
    count=0
    for index,ele in enumerate(h_channel.flatten()):
        if ele==0:
            count+=1

    percentage=(count/totalLeafPix)*100

    return (count,percentage)


#thresholding
def applyThresholding(h_channel,threshold):
    rows,cols=h_channel.shape
    h_channel=h_channel.reshape(rows*cols)

    for index,pixel in enumerate(h_channel):
        if pixel<threshold:
            h_channel[index]=0
        else:
            h_channel[index]=255
    h_channel=h_channel.reshape(rows,cols)
    return np.copy(h_channel)
    # plt.close()
    # plt.imshow(h_channel,cmap='gray')
    # plt.show()

#generate the histogram
def generateHisto(h_channel):
    histo,bins,_=plt.hist(h_channel.flat,bins=100,range=(0,100),ec='black')

    #histogram peak
    maxHisto=np.amax(histo)
    #starting index of the bin
    maxBin=bins[np.where(histo==maxHisto)][0]
    if maxBin<=40:
        maxVal=0.2*maxHisto
    else:
        maxVal=0.5*maxHisto

    #calculating R
    import math
    maxi=-math.inf
    maxV=-math.inf
    for index,ele in enumerate(histo):
        if ele >maxVal and ele !=maxHisto and ele>maxV:
            maxi=bins[index]
            maxV=ele
        
    r=maxi
    if r==(-math.inf):
        r=maxBin
    #calculating s
    s=2*r/3
    threshold=s
    return threshold

#calculate total leafArea
def calcLeafArea(h_channel):
    totalLeafPix=0
    #calculating total leaf area
    for inde,pixel in enumerate(h_channel.flatten()):
        if pixel==255:
            continue
        totalLeafPix+=1
    return totalLeafPix

def improveContrast(h_channel):
    #improving the contrast of the image
    rows,cols=h_channel.shape
    h_channel=h_channel.reshape(rows*cols)
    minP,maxP=np.amin(h_channel),np.amax(h_channel)

    #min-max contrast enhancement
    for index,pixel in enumerate(h_channel):
        h_channel[index]=(((pixel-minP)/(maxP-minP)))*255
        if pixel==0:
            h_channel[index]=255
    h_channel=h_channel.reshape(rows,cols)
    return h_channel
    

#extract the h_channel
def extractH(imgPath):
    #reading the image
    eb2=cv2.imread(imgPath)
    eb2=cv2.cvtColor(cv2.cvtColor(eb2,cv2.COLOR_BGR2RGB),cv2.COLOR_RGB2HSV)
    h_channel=eb2[:,:,0]
    #displaying the h_channel
    # plt.imshow(h_channel,cmap='gray')
    # plt.show()
    return np.copy(h_channel)




#runner programme
row=0
workbook=xlsxwriter.Workbook('results.xlsx')
worksheet=workbook.add_worksheet()
worksheet.set_column(0,10,30)
worksheet.set_default_row(58)
#read early blight images
for ele in range(0,10):
    if row==0:
        worksheet.write(row,0,'Sample')
        worksheet.write(row,1,'Image')
        worksheet.write(row,2,'Disease Type')
        worksheet.write(row,3,'Diseased Pixels')
        worksheet.write(row,4,'Total Pixels')
        worksheet.write(row,5,'Percentage Infc.')
    else:
        h_channel=improveContrast(extractH('../Tomato Early Blight/EB{}.jpg'.format(row)))
        totalArea=calcLeafArea(h_channel)
        thresh=generateHisto(h_channel)
        h_channel=applyThresholding(h_channel,thresh)
        bad,percentage=quantify(h_channel,totalArea)
        worksheet.write(row,0,'EB{}'.format(row))
        worksheet.insert_image(row,1,'../Tomato Early Blight/EB{}.jpg'.format(row),{'x_scale': 0.3, 'y_scale': 0.3})
        worksheet.write(row,2,'Early Blight')
        worksheet.write(row,3,bad)
        worksheet.write(row,4,totalArea)
        worksheet.write(row,5,percentage)

    row+=1
workbook.close()







