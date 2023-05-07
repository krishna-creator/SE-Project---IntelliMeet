# intializing and calling dependencies and libraries 
from __future__ import print_function
import os
import argparse
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from data import cfg_mnet, cfg_re50
from layers.functions.prior_box import PriorBox
from utils.nms.py_cpu_nms import py_cpu_nms
import cv2
from models.retinaface import RetinaFace
from utils.box_utils import decode, decode_landm
import time
import math

# initilizing arugment parsers for functions and classes
parser = argparse.ArgumentParser(description='Retinaface')

parser.add_argument('-m', '--trained_model', default='weights/Resnet50_Final.pth',
                    type=str, help='Trained state_dict file path to open')
parser.add_argument('--network', default='resnet50', help='Backbone network mobile0.25 or resnet50')
parser.add_argument('--cpu', action="store_true", default=False, help='Use cpu inference')
parser.add_argument('--confidence_threshold', default=0.02, type=float, help='confidence_threshold')
parser.add_argument('--top_k', default=5000, type=int, help='top_k')
parser.add_argument('--nms_threshold', default=0.4, type=float, help='nms_threshold')
parser.add_argument('--keep_top_k', default=750, type=int, help='keep_top_k')
parser.add_argument('-s', '--save_image', action="store_true", default=True, help='show detection results')
parser.add_argument('--vis_thres', default=0.6, type=float, help='visualization_threshold')
# creating object instance for the argparse class
args = parser.parse_args()


# check pre-trained graph model for inference
def check_keys(model, pretrained_state_dict):
    # set pre-defined training graph weights
    ckpt_keys = set(pretrained_state_dict.keys())
    model_keys = set(model.state_dict().keys())
    used_pretrained_keys = model_keys & ckpt_keys
    unused_pretrained_keys = ckpt_keys - model_keys
    missing_keys = model_keys - ckpt_keys
    #print('Missing keys:{}'.format(len(missing_keys)))
    #print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
    #print('Used keys:{}'.format(len(used_pretrained_keys)))
    assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
    return True


def remove_prefix(state_dict, prefix):
    ''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
    #print('remove prefix \'{}\''.format(prefix))
    f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
    return {f(key): value for key, value in state_dict.items()}


def load_model(model, pretrained_path, load_to_cpu):
    # loading the face dection trained model from the path mentioned. Model defined the type of model which has to be loaded
    #print('Loading pretrained model from {}'.format(pretrained_path))
    # based ont the flag passed, load the model either to CPU or GPU
    if load_to_cpu:
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
    else:
        device = torch.cuda.current_device()
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
    if "state_dict" in pretrained_dict.keys():
        pretrained_dict = remove_prefix(pretrained_dict['state_dict'], 'module.')
    else:
        pretrained_dict = remove_prefix(pretrained_dict, 'module.')
    check_keys(model, pretrained_dict)
    model.load_state_dict(pretrained_dict, strict=False)
    # retunr the loaded model
    return model

########################################################################

# set torcch gradiient
torch.set_grad_enabled(False)
cfg = None
# either load moblnet odel or resnet model
if args.network == "mobile0.25":
    cfg = cfg_mnet
elif args.network == "resnet50":
    cfg = cfg_re50
# net and model
net = RetinaFace(cfg=cfg, phase = 'test')
net = load_model(net, args.trained_model, args.cpu)
net.eval()
print('Finished loading model!')
#print(net)
# set CUDA usage to true
cudnn.benchmark = True
device = torch.device("cpu" if args.cpu else "cuda")
net = net.to(device)

resize = 1
##########################################################################

def attentiveness_calculation(eyes, nose, mouth):
    # Function to claculate the pose of input face
    pose_sensitivity = 0.05
    # calculate the slope inbetween the eyes
    temp_slope = ((eyes[1][1]-eyes[0][1])/(eyes[1][0]-eyes[0][0]))
    # find the median between the eyes
    mid_eyes = int((eyes[0][0] + eyes[1][0])/2)
    # calculate pose angle
    face_angle = math.degrees(math.atan(temp_slope))
    # check if the face is attentive or not
    if (int(face_angle) >40) or (int(face_angle) < -40) or (nose[0] < min(eyes[0][0], eyes[1][0])) or (nose[0] > max(eyes[0][0], eyes[1][0])):
        #print("NOT Attentive !!!")
        return 1
    else:
        #print(eyes[1][0] - eyes[0][0])
        # calculate the distance between eyes
        if ((eyes[1][0] - eyes[0][0]))<63 and ((eyes[1][0] - eyes[0][0]))>40:
            pose_sensitivity = 0.022
        if (eyes[1][0] - eyes[0][0]) > 93:
            pose_sensitivity = 0.054
        if ((eyes[1][0] - eyes[0][0]))<=95 and ((eyes[1][0] - eyes[0][0]))>=56:
            pose_sensitivity = 0.05
        #print(int(nose[0]), mid_eyes, int((1 + pose_sensitivity) * mid_eyes), int((1 - pose_sensitivity) * mid_eyes))
        # calculaet the loaction of nose in the input face
        if (int(nose[0]) > int((1 + pose_sensitivity) * mid_eyes)) or (int(nose[0]) < int((1 - pose_sensitivity) * mid_eyes)):
            #print("CHECK for ATTENTION !!!!")
            return 1
        else:
            return 0
    

def call_face_detection(input_raw_image):
    # core function for face detection
    img_raw = input_raw_image
    #image_path = "test.jpg"
    #img_raw = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # type case the image to FP32
    img = np.float32(img_raw)
    # set the height and width of the image
    im_height, im_width, _ = img.shape
    # scale the image tensor
    scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
    img -= (104, 117, 123)
    img = img.transpose(2, 0, 1)
    img = torch.from_numpy(img).unsqueeze(0)
    # pass the image to CPU or GPU device
    img = img.to(device)
    scale = scale.to(device)
    # tic the timer for inference time calculation
    #tic = time.time()
    loc, conf, landms = net(img)  # forward pass
    #print('net forward time: {:.4f}'.format(time.time() - tic))
    # crate an object of the priorbox class for bounding box detection and refinement
    priorbox = PriorBox(cfg, image_size=(im_height, im_width))
    priors = priorbox.forward()
    priors = priors.to(device)
    prior_data = priors.data
    # getting bounding box data
    boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
    # scaling and resizing the bounding boxes
    boxes = boxes * scale / resize
    boxes = boxes.cpu().numpy()
    # calculating the scores fo the bounding box classes
    scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
    landms = decode_landm(landms.data.squeeze(0), prior_data, cfg['variance'])
    # calculate the labels and scales for each bounding box for face detection
    scale1 = torch.Tensor([img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                           img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                           img.shape[3], img.shape[2]])
    scale1 = scale1.to(device)
    # generating landmarks of faces
    landms = landms * scale1 / resize
    landms = landms.cpu().numpy()
   
    # ignore low scores
    inds = np.where(scores > args.confidence_threshold)[0]
    boxes = boxes[inds]
    landms = landms[inds]
    scores = scores[inds]

    # keep top-K before NMS
    order = scores.argsort()[::-1][:args.top_k]
    boxes = boxes[order]
    landms = landms[order]
    scores = scores[order]

    # do NMS
    dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    keep = py_cpu_nms(dets, args.nms_threshold)
    # keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
    dets = dets[keep, :]
    landms = landms[keep]

    # keep top-K faster NMS
    dets = dets[:args.keep_top_k, :]
    landms = landms[:args.keep_top_k, :]

    dets = np.concatenate((dets, landms), axis=1)

    # show image
    #if args.save_image:
    if len(dets)<1:
        print("No FACE !!!!")
        return img_raw, -1
    else:
        tmp_face_count = 0
        # localize faces in the image
        for b in dets:
            if b[4] < args.vis_thres:
                if tmp_face_count >= len(dets):
                    print("No FACE !!!")
                    continue
                else:
                    tmp_face_count = tmp_face_count +1
                    continue
            #text = "{:.4f}".format(b[4])
            b = list(map(int, b))
            #cv2.rectangle(img_raw, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
            cx = b[0]
            cy = b[1] + 12
            #cv2.putText(img_raw, text, (cx, cy),
            #            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

            # landms
            #cv2.circle(img_raw, (b[5], b[6]), 1, (0, 0, 255), 4)
            #cv2.circle(img_raw, (b[7], b[8]), 1, (0, 255, 255), 4)
            #cv2.circle(img_raw, (b[9], b[10]), 1, (255, 0, 255), 4)
            #cv2.circle(img_raw, (b[11], b[12]), 1, (0, 255, 0), 4)
            #cv2.circle(img_raw, (b[13], b[14]), 1, (255, 0, 0), 4)
            
            # calculate the attentiveness of the input face and add label to the face.
            if (attentiveness_calculation([[b[5], b[6]],[b[7], b[8]]], [b[9], b[10]], [[b[11], b[12]],[b[13], b[14]]])):
                img_raw = cv2.putText(img_raw, "NOT ATTENTIVE !!!", (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
                return img_raw, 1
            else:
                return img_raw, 0

        # save image
    
        #name = "test.jpg"

