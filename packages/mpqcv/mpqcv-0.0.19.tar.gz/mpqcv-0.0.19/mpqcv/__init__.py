import sys
import cv2
import os
lib_path = (os.path.split(os.path.realpath(__file__))[0])
sys.path.append(lib_path)
from My_CV import *
# -*- coding utf-8 -*-
"""
Created on May 18th 09:41 2023

@auther: Peiqi Miao

"""
# 椒盐噪声
def Salt_AndPepper(src, percetage=0.3):
    SP_NoiseImg = SaltAndPepper(src, percetage)
    return SP_NoiseImg

# 高斯噪声
def add_GaussianNoise(image, percetage=0.3):
    G_Noiseimg = addGaussianNoise(image, percetage)
    return G_Noiseimg

# 昏暗
def dar_ker(image, percetage=0.9):
    image_copy = darker(image, percetage)
    return image_copy

# 亮度
def brigh_ter(image, percetage=1.5):
    image_copy = brighter(image, percetage)
    return image_copy

# 旋转
def ro_tate(image, angle, center=None, scale=1.0):
    rotated = rotate(image, angle, center, scale)
    return rotated

# 翻转
def fl_ip(image):
    flipped_image = flip(image)
    return flipped_image

################################
def get_Frame(video_path='',save_path=''):
    ####从视频获取图片
    #e.g: get_frame(video_path='1.avi',save_path='')
    get_frame(video_path=video_path, save_path=save_path)

def get_Frame(video_path='', save_path='', frame_interval=1):
    ####从视频获取图片
    #e.g: get_frame(video_path='1.avi',save_path='')
    get_frame(video_path=video_path, save_path=save_path, frame_interval = frame_interval)

def bright_Pic(img, alpha=1.5, beta=0):
    ###增加亮度
    img_bright = bright_pic(img, alpha=alpha, beta=beta)
    return img_bright

def normal_Pic(img,dst=None,alpha=350,beta=10,norm_type=cv2.NORM_MINMAX):
    img_norm=normal_pic(img,dst=dst,alpha=alpha,beta=beta,norm_type=norm_type)
    return img_norm

def gama_Pic(img,x = 0.4):
    img_gamma = gama_pic(img,x = x)
    return img_gamma

def contr_Pic(img,contrast = 1.5):
    # 对比度增强
    img_contrasted = contr_pic(img,contrast = 1.5)
    return img_contrasted

def enhance_Contrast(image,clipLimit=7.0, tileGridSize=(50, 50)):
    #自适应对比度增强
    result = enhance_contrast(image,clipLimit=clipLimit, tileGridSize=tileGridSize)
    return result
######################################################

def find_C_only(cnts,level):
    c = find_c_only(cnts,level)
    return c

def find_Mask_points(img, c):
    mask_pic, pts = find_mask_points(img, c)
    return mask_pic,pts

##########基于灰度图像的梯度共生矩阵###################
'''根据灰度梯度共生矩阵计算纹理特征量，包括小梯度优势，大梯度优势，灰度分布不均匀性，梯度分布不均匀性，能量，灰度平均，梯度平均，
    灰度方差，梯度方差，相关，灰度熵，梯度熵，混合熵，惯性，逆差矩'''
def get_Glgcm(img_gray, ngrad=16, ngray=16):
    glgcm_features = glgcm(img_gray, ngrad, ngray)
    return glgcm_features
#########color moments(CMs)###################
def get_Color_moments_array(array):
    color_feature = get_color_moments_array(array)
    return color_feature
# Compute low order moments(1,2,3)
def get_Color_moments(img):
    ####img为BGR格式,用opencv打开即可，或readPic（）方法
    color_feature = color_moments(img)
    return color_feature
#########color moments(CMs)###################

def cutPic(pic,gre_thre=127,kernel=10,iter1=0,iter2=0):
    #gre_thre[0,255],kernel卷积核大小，thre1缩小程度，扩大程度
    new_pic = cut_pic(pic,gre_thre,kernel,iter1,iter2)
    return new_pic

def readPic(name):
    img = read_pic(name)
    return img

def readGraypic(name):
    img = readPic(name)
    gray_pic = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray_pic

def save_pic(savename,img):
    cv2.imwrite(savename,img)

def show_img(img,dely):
    cv2.namedWindow('show',0)
    cv2.imshow('show', img)
    cv2.waitKey(dely)

def show_img(img,dely):
    cv2.namedWindow('show',0)
    cv2.imshow('show', img)
    cv2.waitKey(dely)


def mkDir(path):
    mkdir(path)

def rot90(img):
    img90 = rot_90(img)
    return img90

def warpMinirect(rect,img):
    warped = warp_minirect(rect,img)
    return warped

def xintaiArg(c):
    a1_w, a1_h, area, baohedu1, match_k = xintai_arg(c)
    return a1_w, a1_h, area, baohedu1, match_k

def give_day_name():
    name = datetime.datetime.now().strftime('%Y%m%d')
    print(name)
    return name

def give_name():
    name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return name

def preProcessing(frame,gray_thre = 100,kernel = 10,iter1=1,iter2 = 1,type = 0):
    dst = pre_processing(frame,gray_thre,kernel,iter1,iter2,type)
    return dst

def find_cMax(cnts):
    c = find_c_max(cnts)
    return c

def findCnts(bin_img):
    cnts = find_cnts(bin_img)
    return cnts

def drawCnts(src,cnts):
    src = draw_cnts(src,cnts)
    return src

def Rect(c):
    bounding_boxes = rect(c)
    return bounding_boxes

def draw_Rect(frame,rect):
    frame = draw_rect(frame,rect)
    return frame

def minRect(c):
    rect = min_rect(c)
    return rect

def draw_Min_rect(frame,rect):
    draw_min_rect(frame, rect)
    return frame

def drawCircle(img,center,r,color,thickness,txt_key=1,index=1):
    img = draw_circle(img,center,r,color,thickness,txt_key,index)
    return  img
def matchC(c1,c2):
    retval = match_c(c1,c2)
    return retval
def concatPic1(img):
    img_01 = concat_pic1(img)
    return img_01

def concatPic2(img, axis):
    img_02 = concat_pic2(img, axis)
    return img_02

def concatPic3(img):
    img_03 = concat_pic3(img)
    return img_03

def tiaoZheng(img_list):
    out = tiaozheng(img_list)
    return out

def tiaoZheng234(img_list):
    out = tiaozheng234(img_list)
    return out
def centerX_down(img,h,thre,dk):
    #饭回图片最下边目标的中心X左边，如无轮廓，返回-100
    center_x = c_x_down(img, h, thre, dk)
    return center_x
def cat_Pic(gray,resize_k=1,h0=2000,w0=4080,thre = 200,type=0,min_area=500,min_pic_num=8):
    flag,discribe,concat_pic = cat_pic(gray, resize_k, h0, w0, thre, type, min_area, min_pic_num)
    return flag,discribe,concat_pic
def getGray(img1,channal):
    get_Gray(img1, channal)

if __name__ == '__main__':
    # show_name('./test2.jpg',0)
    # img = readGraypic('./test2.jpg')
    # img = drawCircle(img,(100,100),30,255,-1,txt_key=0)
    # show_img(img,0)
    # # CMs = get_Color_oments(img)
    # # print(CMs)
    # # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # # new_pic = cut_pic(img,100,10,1,1)
    # # show_img(new_pic,0)
    # # glgcm = get_Glgcm(img)
    # # print(glgcm)
    # path = './dt2/'
    #
    # namelist=os.listdir(path)
    # print(namelist)
    # new_list = []
    # for file in namelist:
    #     filenum = file[0:-4]
    #     new_list.append(int(filenum))
    # new_list.sort()
    # print(new_list)
    # for i,file in enumerate(new_list):
    #     gray = cv2.imread(path+str(file)+'.tif',0)
    #     gray = gray[:,:800]
    #     flag,discribe,img=cat_Pic(gray,h0=512,w0=800)
    #     print(i,file,flag,discribe)
    #     if flag == 1:
    #         name = give_name()
    #         cv2.imwrite(name+'.png',img)

    img = cv2.imread('aaa.png')
    cv2.imshow("1", img)
    cv2.waitKey(5000)
    # 旋转
    rotated_90 = ro_tate(img, 90)
    show_img(rotated_90, 0)
    rotated_180 = ro_tate(img, 180)
    show_img(rotated_180, 0)

    # 镜像
    flipped_img = fl_ip(img)
    show_img(flipped_img, 0)
    # 增加噪声
    img_salt = Salt_AndPepper(img, 0.3)
    show_img(img_salt, 0)
    # cv2.imwrite(file_dir + img_name[0:7] + '_salt.jpg', img_salt)
    img_gauss = add_GaussianNoise(img, 0.3)
    show_img(img_gauss, 0)
    # 变暗/变亮
    img_darker = dar_ker(img)
    show_img(img_darker, 0)
    img_brighter = brigh_ter(img)
    show_img(img_brighter, 0)

    blur = cv2.GaussianBlur(img, (7, 7), 1.5)
    #      cv2.GaussianBlur(图像，卷积核，标准差）
    show_img(blur, 0)