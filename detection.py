from imageai.Detection import ObjectDetection
import os

def get_detection_captcha(word):
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
    detector.loadModel()

    arr = os.listdir('images')
    arr1 = []
    for i in arr:
        arr1.append(int(i.split('.png')[0]))

    dict_image_captcha = {}

    for i in sorted(arr1):
        detections = detector.detectObjectsFromImage(input_image=os.path.join('{}/images'.format(execution_path) , "{}.png".format(i)), output_image_path=os.path.join('{}/imagesnew'.format(execution_path) , "{}.png".format(i)))
        print('IMAGE {}.png'.format(i))
        aux = []
        for eachObject in detections:
            # print(eachObject["name"])
            aux.append(eachObject["name"].strip())
        
        res = []
        [res.append(x) for x in aux if x not in res]

        if word in res:
            a = {i: True}
            dict_image_captcha.update(a)
        else:
            a = {i: False}
            dict_image_captcha.update(a)

    return dict_image_captcha