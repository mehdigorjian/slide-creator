import glob
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

# before running the code make sure to create "four_output" and "slide_output" directories
# also add a "background_images" directory and include the background and the fourView ".jpg"
# the slide size is (800, 600) and the fourView size is (200, 200)
# coef enlarges the slide size with respect to the 4:3 ratito
coef = 3
rootdir = "input_data"
fourView = "background_images/fourView.jpg"
slide = "background_images/slide600_new.jpg"
fourViewRootDir = "four_output"
slide_output = "slide_output"


inputdata = int(input("Choose an option [1] Head [2] Shoe: "))
if inputdata == 1:
    model = "Head "
if inputdata == 2:
    model = "Shoe "

coords = [(0*coef, 0*coef), (0*coef, 105*coef),
          (105*coef, 0*coef), (105*coef, 105*coef)]
slideCoords = [(50*coef, 200*coef), (300*coef, 200*coef), (550*coef, 200*coef)]
bottomTextCoords = [(120*coef, 450*coef), (370*coef,
                                           450*coef), (620*coef, 450*coef)]
permute = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]


with Image.open(fourView) as bkg4:
    bkg4.load()
bkg4.convert("RGBA")
bkg4W, bkg4H = bkg4.size
bkg4 = bkg4.resize((bkg4W*coef, bkg4H*coef))


with Image.open(slide) as slideBkg:
    slideBkg.load()
slideBkg.convert("RGBA")
slideBkgW, slideBkgH = slideBkg.size
slideBkg = slideBkg.resize((slideBkgW*coef, slideBkgH*coef))


def subFolderPathAndNumList(rootdir):
    # getting folder path and folder number in the form of a tuple (dirName, folderNum)
    # insert the root path
    subFolders = []
    for subDir in os.listdir(rootdir):
        d = os.path.join(rootdir, subDir)
        if os.path.isdir(d):
            dirName = d + "/"
            headTail = os.path.split(dirName)
            folderPathSplit = headTail[0].split('/')
            folderName = folderPathSplit[-1]
            folderNum = folderName[4:]
            subFolders.append((dirName, folderNum))
    return subFolders


def getListOfFilesForEachImageCluster(folderPath, userNum, imgNum):
    # outputs a list of 4 views of an image
    # folder path with "/" in the end
    filesRelatedToSpecificImage = glob.glob(
        folderPath + 'u_' + str(userNum) + '_i_' + str(imgNum) + '_*')

    filesRelatedToSpecificImage.sort(
        key=lambda x: x.split('_')[-1].split('.')[0])
    return filesRelatedToSpecificImage


def listOfFourViewImages(folderPath, imgNum):
    # outputs a list of 4 views of an image
    # folder path with "/" in the end
    ff = glob.glob(folderPath + "[1-3].jpg")
    ff.sort()
    return ff


def noSortListOfFourViewImages(folderPath):
    # outputs a list of 4 views of an image
    # folder path with "/" in the end
    ff = glob.glob(folderPath + "[1-3].jpg")
    return ff


def addToSlide(rootDestinationFolderPath, slideBkgImage, fourView, x, y, userIDNum):
    # headImage.convert("RGBA")
    # headResized = headImage.resize((95, 95))
    slideBkgImage.paste(fourView, (x, y))
    # fourViewBkgImage.show()
    d = rootDestinationFolderPath
    if not os.path.exists(d):
        os.mkdir(d)
    file = str(userIDNum) + ".jpg"
    slideBkgImage.save(d + "/" + file)


def imShowResized(imPath):
    with Image.open(imPath) as img:
        img.load()
    imgResized = img.resize((95*coef, 95*coef))
    imgResized.show()


def createFourView(rootDestinationFolderPath, fourViewBkgImage, headImage, x, y, headID, userIDNum):
    headImage.convert("RGBA")
    headResized = headImage.resize((95*coef, 95*coef))
    fourViewBkgImage.paste(headResized, (x, y), headResized)
    # fourViewBkgImage.show()
    d = rootDestinationFolderPath + "/" + "User" + str(userIDNum)
    if not os.path.exists(d):
        os.mkdir(d)
    file = str(headID) + ".jpg"
    fourViewBkgImage.save(d + "/" + file)


def generateFourViewImages(rootdir):
    subDirectory = subFolderPathAndNumList(rootdir)
    # for item in subDirectory:
    #     print(item)
    for imFile in subDirectory:
        # print(imFile[0]) ###################### console
        print("User" + imFile[1] + ": \n")  # console
        bkg4copy = bkg4.copy()
        # imgNum = imFile[1].split('_')[-2].split('.')[0]
        for headCounter in range(1, 4):
            # print("imFile[0]: "+imFile[0])
            imgPathNameAndImgNum = getListOfFilesForEachImageCluster(
                imFile[0], imFile[1], headCounter)
            counter = 0
            # headID = (rootF.split('_')[-2].split('.')[0])[-1]
            for imgPath in imgPathNameAndImgNum:  # this loop executes 4 times to create the fourView image
                with Image.open(imgPath) as headItem:
                    headItem.load()
                # print("*******")
                print(imgPath)  # console
                # imShowResized(imgPathName)
                headID = (imgPath.split('_')[-2].split('.')[0])[-1]
                # print("headID: " + str(headID))
                # print("userIDNum: " + imFile[1])
                createFourView(fourViewRootDir, bkg4copy,
                               headItem, coords[counter][0], coords[counter][1], headID, imFile[1])
                counter += 1
                # print(headID)
            # bkg4copy.show()
            print('--------------')  # console
        print('------------------------------------------')  # console


def slideFourViewPlace(fourViewrootdir):
    subDirectory = subFolderPathAndNumList(fourViewrootdir)
    for imFile in subDirectory:
        # print(imFile[0])
        # print("User" + imFile[1] + " slide created!") ###################### console
        slideBkgcopy = slideBkg.copy()
        headerTextTitle = "User " + imFile[1]
        headerText = ImageDraw.Draw(slideBkgcopy)
        myFont = ImageFont.truetype('Arial.ttf', coef*30)
        headerText.text((coef*340, coef*100), headerTextTitle,
                        font=myFont, fill=(80, 80, 80))
        for fourViewCount in range(1, 4):
            # print("imFile[0]: "+imFile[0])
            imgPathNameAndImgNum = listOfFourViewImages(
                imFile[0], fourViewCount)
            counter = 0
            # print(imgPathNameAndImgNum)
            for imgPath in imgPathNameAndImgNum:  # this loop executes 3 times to create the slide
                with Image.open(imgPath) as fourViewItem:
                    fourViewItem.load()
                # print("imgPath: "+imgPath)
                # imShowResized(imgPathName)
                # headID = (imgPath.split('/')[-1]).split('.')[0]
                # print("headID: " + str(headID))
                # print("userIDNum: " + imFile[1])
                addToSlide(slide_output, slideBkgcopy,
                           fourViewItem, slideCoords[counter][0], slideCoords[counter][1], imFile[1])

                TextTitle = model + str(counter+1)
                myFont1 = ImageFont.truetype('Arial.ttf', coef*18)
                headerText.text((bottomTextCoords[counter][0], bottomTextCoords[counter][1]), TextTitle,
                                font=myFont1, fill=(80, 80, 80))
                counter += 1
            # bkg4copy.show()
            # print('--------------')
        # print('------------------------------------------')


def permuteSlideFourViewPlace(fourViewrootdir):
    subDirectory = subFolderPathAndNumList(fourViewrootdir)
    # for item in subDirectory:
    # print(item)
    for imFile in subDirectory:
        # print(imFile[0])
        print("User" + imFile[1] + " slide created!")  # console
        slideBkgcopy = slideBkg.copy()
        headerTextTitle = "User " + imFile[1]
        headerText = ImageDraw.Draw(slideBkgcopy)
        myFont = ImageFont.truetype('Arial.ttf', coef*30)
        headerText.text((coef*340, coef*100), headerTextTitle,
                        font=myFont, fill=(80, 80, 80))

        p = permute[int(imFile[1]) % 6]
        # print(p)
        for _ in range(1, 4):
            # print("imFile[0]: "+imFile[0])
            imgPathNameAndImgNum = noSortListOfFourViewImages(imFile[0])
            imZip = zip(p, imgPathNameAndImgNum)
            counter = 0
            # print(imgPathNameAndImgNum)
            for cnt, imgPath in imZip:
                # for imgPath in imgPathNameAndImgNum:  # this loop executes 3 times to create the slide
                with Image.open(imgPath) as fourViewItem:
                    fourViewItem.load()
                # print("imgPath: "+imgPath)
                # imShowResized(imgPathName)
                # headID = (imgPath.split('/')[-1]).split('.')[0]
                # print("headID: " + str(headID))
                # print("userIDNum: " + imFile[1])
                addToSlide(slide_output, slideBkgcopy,
                           fourViewItem, slideCoords[cnt-1][0], slideCoords[cnt-1][1], imFile[1])

                TextTitle = model + str(counter+1)
                myFont1 = ImageFont.truetype('Arial.ttf', coef*18)
                headerText.text((bottomTextCoords[counter][0], bottomTextCoords[counter][1]), TextTitle,
                                font=myFont1, fill=(80, 80, 80))
                counter += 1
                # print(headID)
            # bkg4copy.show()
            # print('--------------')
        # print('------------------------------------------')

        logString = ""
        for s in p:
            logString += str(s)
        fileLogName = slide_output + "/" + \
            "logFile_user" + str(imFile[1]) + ".txt"
        # print(fileLogName)
        logFile = open(fileLogName, "w")
        logFile.write(logString)
        logFile.close()


generateFourViewImages(rootdir)  # creating four views
# slideFourViewPlace(fourViewRootDir) # slide creating without permutation
permuteSlideFourViewPlace(fourViewRootDir)  # slide creating with permutation
