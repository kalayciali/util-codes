from PIL import Image
import pytesseract
from pytesseract import Output

def cleanFile(filePath, threshold):
    img = Image.open(filePath)

    # set treshold value for the img
    # 255 is meant to black
    img = img.point(lambda x: 0 if x < threshold else 255)
    return img

def getConfidence(img):
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    text = data['text']
    confidences = []
    numChars = []

    for i in range(len(text)):
        if int(data['conf'][i]) > -1:
            confidences.append(data['conf'][i])
            numChars.append(len(text[i]))

    tot = 0
    for i in range(len(confidences)):
        tot += confidences[i] * numChars[i]
    avg = tot /  sum(numChars)

    return avg, sum(numChars)

FILEPATH = './text_test.jpg'

start = 80
step = 5
end = 200

for threshold in range(start, end, step):
    img = cleanFile(FILEPATH, threshold)
    scores = getConfidence(img)
    print('threshold: ' + str(threshold) + ", confidence: " +
          str(scores[0]) + ", numChars: " + str(scores[1]))
img = cleanFile('./text_test.jpg', './cleaned.jpg')
print(pytesseract.image_to_string(img))
