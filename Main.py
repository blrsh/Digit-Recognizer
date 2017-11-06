import csv
import SimpleNet as net
from PIL import Image

test_data = None
test_answer = None

num = []
 
def putWeight(x, y, shade):
    im = Image.open("weights.png")
    pix = im.load()

    if im.mode == '1':
        value = int(shade >= 127) # Black-and-white (1-bit)
    elif im.mode == 'L':
        value = shade # Grayscale (Luminosity)
    elif im.mode == 'RGB':
        value = (shade, shade, shade)
    elif im.mode == 'RGBA':
        value = (shade, shade, shade, 255)
    elif im.mode == 'P':
        raise NotImplementedError("TODO: Look up nearest color in palette")
    else:
        raise ValueError("Unexpected mode for PNG image: %s" % im.mode)

    pix[x, y] = value 

    im.save("weights.png")
    
def saveWeights():
    for y in range(28):
        for x in range(28):
            if (28 * y + x) < 783:
                putWeight(x, y, int((1 + net.w[28 * y + x]) * 127))

def getIndex(x):
    global num
    if x == num[0]:
        return 0
    elif x == num[1]:
        return 1
    else:
        print("GET INDEX ERROR")
        return -1

def loadAnswers():
    global num
    
    answers = []
    train_file = "mnist_train.csv"
    with open(train_file) as f:
        reader = csv.reader(f, delimiter=",")
        for i in reader:
            if int(i[0]) is num[1] or int(i[0]) is num[0]:
                answers.append(getIndex(int(i[0])))
    return answers

def loadData():
    global num
    
    data = []
    image = []
    train_file = "mnist_train.csv"
    with open(train_file) as f:
        reader = csv.reader(f, delimiter=",")
        for i in reader:
            image = []
            if int(i[0]) is num[1] or int(i[0]) is num[0]:
                for j in range(1, 784):
                    image.append(int(i[j]) / 255)
                data.append(image)
    return data

def loadTestData():
    global num
    
    data = []
    image = []
    train_file = "mnist_test.csv"
    with open(train_file) as f:
        reader = csv.reader(f, delimiter=",")
        for i in reader:
            image = []
            if int(i[0]) is num[1] or int(i[0]) is num[0]:
                for j in range(1, 784):
                    image.append(int(i[j]) / 255)
                data.append(image)
    return data

def loadTestAnswers():
    global num
    
    answers = []
    train_file = "mnist_test.csv"
    with open(train_file) as f:
        reader = csv.reader(f, delimiter=",")
        for i in reader:
            if int(i[0]) is num[1] or int(i[0]) is num[0]:
                answers.append(getIndex(int(i[0])))
    return answers

def test(x):
    global num
    
    global test_data
    global test_answer
    
    net.test(test_data[x])
    print("Actual Value:", num[test_answer[x]])

def superTest():
    global test_data
    global test_answer
    global num
    
    right = 0
    for i in range(len(test_answer)):
        guess = num[net.test(test_data[i])]
        ans = num[test_answer[i]]
        if i % 2 == 0:
            print("Index:", i, "Guess:", guess, "Acual Answer:", ans)
        if guess == ans:
            right += 1
    print("Restults:", right, "/", len(test_answer), "correct.")
    print("Accuracy:", int(100 * (right / len(test_answer))), "%")
    print()
    
def t():
    global num
    pic = []
    im = Image.open("test_image.png") 
    pix = im.load()
    for y in range(28):
        for x in range(28):
            pic.append(pix[x, y][0] / 255)
    print("AI Guesses:", num[net.test(pic)])
    print()

def testMenu():
    global test_data
    global test_answer
    
    inp = input("Would you like to test the AI with the test dataset?[Y/N] ").lower()
    if inp == 'y':
        print("Loading test data...")
        test_data = loadTestData()
        print("Loading test labels...")
        test_answer = loadTestAnswers()
        superTest()
    while input("Test the AI with test_image.png?[Y/N]").lower()[0] == 'y':
        t()
        
def start():
    global num
    
    print("Pick two digits for the AI to classify (Ex. 1 vs 4)")
    num.append(int(input("Didget 1: ")))
    num.append(int(input("Didget 2: ")))
    print("Loading training data...")
    net.data = loadData()
    print("Loading labels...")
    net.answer = loadAnswers()
    net.train(2000, 1)
    saveWeights()
    testMenu()
    inp = input("[R]estart Training Process\n[T]est Menu\n[E]xit Program\n").lower()[0]
    if inp == 'r':
        start()
    elif inp == 't':
        testMenu()
    else:
        print("Finished.")
    
start()


