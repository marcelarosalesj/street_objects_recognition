"""
Object detection program that detect from the webcam

Resources: https://heartbeat.fritz.ai/real-time-object-detection-on-raspberry-pi-using-opencv-dnn-98827255fa60
"""
import cv2

print("Hello World!")

# Pretrained classes in the model
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def id_class_name(class_id, classes):
    for key,value in classes.items():
        if class_id == key:
            return value

# The model
model = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
print("Model created")

cap = cv2.VideoCapture(0)
image = None
print("Press -q- to select the frame")
while(True):
    # Capture frame-by-frame
    ret, image = cap.read()
    cv2.imshow('Frame for recognition',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Image captured")

image_height, image_width, _ = image.shape

"""
To feed image into a network we need to convert image into a blob
- Convert RGB to BGR because OpenCV reads in BGR
- Resize to 300x300
"""
model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))

output = model.forward()
for detection in output[0, 0, :, :]:
    confidence = detection[2]
    if confidence > 0.5:
        class_id = detection[1] # class id
        class_name=id_class_name(class_id,classNames)
        print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))
        print(">"+str(detection[0]))
        print(">"+str(detection[1]))
        print(">"+str(detection[2]))
        print(">"+str(detection[3]))
        box_x = detection[3] * image_width
        box_y = detection[4] * image_height
        box_width = detection[5] * image_width
        box_height = detection[6] * image_height
        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
        cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
