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
        if ele==255:
            count+=1

    percentage=(count/totalLeafPix)*100

    return (count,percentage)


#thresholding
def applyThresholding(h_channel,threshold,typeC):
    rows,cols=h_channel.shape
    h_channel=h_channel.reshape(rows*cols)

    for index,pixel in enumerate(h_channel):
        if pixel<threshold:
            h_channel[index]=0
        else:
            h_channel[index]=255
    h_channel=h_channel.reshape(rows,cols)
    h_channel=cv2.bitwise_not(h_channel)
    #performing morphological erosion on the image
    kernel=np.ones((2,2),np.uint8)
    if typeC=='hsv':
        eroded_img=cv2.erode(h_channel,kernel,iterations=1)
    elif typeC=='lab':
        h_channel=np.array(h_channel,dtype=np.uint8)
        eroded_img=cv2.erode(h_channel,kernel,iterations=3)


    return np.copy(eroded_img)
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
def calcLeafArea(imagePath):
    totalLeafPix=0
    #calculating total leaf area
    image=cv2.cvtColor(cv2.imread(imagePath),cv2.COLOR_BGR2GRAY)
    _,thresh=cv2.threshold(image,0,255,cv2.THRESH_BINARY)
    #calculating total leaf area
    kernel=np.ones((2,2),np.uint8)
    thresh=cv2.erode(thresh,kernel,iterations=3)
    totalLeafPix=cv2.countNonZero(thresh)
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

#extract the l_channel
def extractA(imgPath):
    eb2=cv2.imread(imgPath)
    eb2=cv2.cvtColor(eb2,cv2.COLOR_BGR2LAB)
    achannel=eb2[:,:,1]
    rows,cols=achannel.shape
    achannel=achannel.reshape(rows*cols)
    achannelDup=[]
    for _,pixel in enumerate(achannel.flatten()):
        if pixel==128:
            achannelDup.append(255)
            continue
        achannelDup.append(255-pixel)
    achannelDup=np.array(achannelDup).reshape(rows,cols)
    achannel=np.copy(achannelDup)

    return np.copy(achannel)



colorSPace=input('Enter the channel you want to extract : ')
diseaseType=input('Enter the disease type code : ')
if diseaseType.lower()=='eb':
    pathToPics='../Tomato Early Blight/EB'
    headName='Early Blight'
    if colorSPace.lower()=='lab':
        file='earlyL.xlsx'
    elif colorSPace.lower()=='hsv':
        file='early.xlsx'
elif diseaseType.lower()=='lb':
    pathToPics='../Tomato Late Blight/LB'
    headName='Late Blight'
    if colorSPace.lower()=='lab':
        file='lateL.xlsx'
    elif colorSPace.lower()=='hsv':
        file='late.xlsx'
#runner programme
row=0
workbook=xlsxwriter.Workbook(file)
worksheet=workbook.add_worksheet()
worksheet.set_column(0,10,30)
worksheet.set_default_row(58)
#read early blight images
for ele in range(0,51):
    if row==0:
        worksheet.write(row,0,'Sample')
        worksheet.write(row,1,'Image')
        worksheet.write(row,2,'Disease Type')
        worksheet.write(row,3,'Diseased Pixels')
        worksheet.write(row,4,'Total Pixels')
        worksheet.write(row,5,'Percentage Infc.')
    else:
        if colorSPace.lower()=='hsv':
            channel=improveContrast(extractH('{}{}.jpg'.format(pathToPics,row)))

        elif colorSPace.lower()=='lab':
            channel=improveContrast(extractA('{}{}.jpg'.format(pathToPics,row)))
        else:
            print('Invalid details or some error happened')
            exit()
        print('{}{}.jpg'.format(pathToPics,row))
        totalArea=calcLeafArea('{}{}.jpg'.format(pathToPics,row))
        thresh=generateHisto(channel)
        channel=applyThresholding(channel,thresh,colorSPace.lower())
        bad,percentage=quantify(channel,totalArea)
        worksheet.write(row,0,'EB{}'.format(row))
        worksheet.insert_image(row,1,'{}{}.jpg'.format(pathToPics,row),{'x_scale': 0.3, 'y_scale': 0.3})
        worksheet.write(row,2,headName)
        worksheet.write(row,3,bad)
        worksheet.write(row,4,totalArea)
        worksheet.write(row,5,percentage)

    row+=1
workbook.close()








