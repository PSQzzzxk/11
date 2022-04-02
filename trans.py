import os
import cv2
import sys
import csv
import configparser

def preprocessVideo(test_video_path, train_video_path):
    
    ## test img1
    vidcap = cv2.VideoCapture(test_video_path)
    (cap, frame) = vidcap.read()

    height = frame.shape[0]
    width = frame.shape[1]
    framerate = vidcap.get(5)
    cnt_frame = 0

    while (cap):
        cv2.imwrite(
            os.path.join(test_frame_save_path, "frame_%d.jpg" % (cnt_frame)),
            frame)
        cnt_frame += 1
        print(cnt_frame, end="\r")
        sys.stdout.flush()
        (cap, frame) = vidcap.read()
    vidcap.release()
    print("test frame finish!")

    ## test ini
    os.system('touch {}'.format(test_ini_path))
    conf = configparser.ConfigParser()
    conf.read(test_ini_path, encoding='utf-8')
    section = "Sequence"
    conf.add_section(section)
    conf.set(section,"name","seq1")
    conf.set(section,"imDir","img1")
    conf.set(section,"frameRate",str(framerate))
    conf.set(section,"seqLength","600")
    conf.set(section,"imWidth",str(width))
    conf.set(section,"imHeight",str(height))
    conf.set(section,"imExt",".jpg")
    with open(test_ini_path, 'w') as f:
        conf.write(f)
    print("test ini finish!")

    ## train img1
    vidcap = cv2.VideoCapture(train_video_path)
    (cap, frame) = vidcap.read()

    height = frame.shape[0]
    width = frame.shape[1]
    framerate = vidcap.get(5)
    cnt_frame = 0

    while (cap):
        cv2.imwrite(
            os.path.join(train_frame_save_path, "frame_%d.jpg" % (cnt_frame)),
            frame)
        cnt_frame += 1
        print(cnt_frame, end="\r")
        sys.stdout.flush()
        (cap, frame) = vidcap.read()
    vidcap.release()
    print("train frame finish!")

    ## train ini
    os.system('touch {}'.format(train_ini_path))
    conf = configparser.ConfigParser()
    conf.read(train_ini_path, encoding='utf-8')
    section = "Sequence"
    conf.add_section(section)
    conf.set(section,"name","seq2")
    conf.set(section,"imDir","img1")
    conf.set(section,"frameRate",str(framerate))
    conf.set(section,"seqLength","600")
    conf.set(section,"imWidth",str(width))
    conf.set(section,"imHeight",str(height))
    conf.set(section,"imExt",".jpg")
    with open(train_ini_path, 'w') as f:
        conf.write(f)
    print("train ini finish!")

    
def preprocessTxt(test_txt_path, train_txt_path, csv_path):
    
    ## test det
    test_source = open(test_txt_path)
    test_data = test_source.read()
    test_target = open(test_det_save_path + "det.txt", 'w')
    test_target.write(test_data)
    test_source.close()
    test_target.close()
    print("test det finish!")

    ## train det
    train_source = open(train_txt_path)
    train_data = train_source.read()
    train_target = open(train_det_save_path + "det.txt", 'w')
    train_target.write(train_data)
    train_source.close()
    train_target.close()
    print("train det finish!")

    ## train gt
    csv_out_target = open(train_gt_save_path + "gt.txt",'w')
    
    for id in range(0,20):                                    ## max nuber of target in a frame
        print('start')
        file = open(csv_path)
        reader = csv.reader(file)
        for row in reader:
            if(row[1] == str(id)):
                write_data = row[0]+','+str((id+1))+','+row[2]+','+ \
                             row[3]+','+row[4]+','+row[5]+','+ \
                             '1,'+'1,'+'1'
                print(write_data)
                csv_out_target.write(write_data)
                csv_out_target.write('\r\n')
                print("================")
        file.close()  
        print('finished id %d' % id)
        id+=1             
    csv_out_target.close()
    print("train gt finish")


if __name__ == "__main__":
    
    DataSet_path = input('input path of dataset\n') + '/'	 
    ## DataSet_path = "/home/vfido"     
    
    test_video_path = "/home/vfido/Downloads/testvideo.mp4"    ## The following five paths need to be modified
    train_video_path = "/home/vfido/Downloads/trainvideo.mp4"  ## 
    test_txt_path = "/home/vfido/Downloads/testvideo.txt"	 ##
    train_txt_path = "/home/vfido/Downloads/trainvideo.txt"	 ##
    csv_path = "/home/vfido/Downloads/tsvideo.csv"		 ##
    
    ## make dir
    os.makedirs(DataSet_path + "MOT16/images/test/seq1/det")
    os.makedirs(DataSet_path + "MOT16/images/test/seq1/img1")

    os.makedirs(DataSet_path + "MOT16/images/train/seq2/det")
    os.makedirs(DataSet_path + "MOT16/images/train/seq2/gt")
    os.makedirs(DataSet_path + "MOT16/images/train/seq2/img1")

    ## set path
    test_frame_save_path = DataSet_path + "MOT16/images/test/seq1/img1/"
    test_det_save_path = DataSet_path + "MOT16/images/test/seq1/det/"
    
    train_frame_save_path = DataSet_path + "MOT16/images/train/seq2/img1/"
    train_det_save_path = DataSet_path + "MOT16/images/train/seq2/det/"
    train_gt_save_path = DataSet_path + "MOT16/images/train/seq2/gt/"

    test_ini_path = DataSet_path + "MOT16/images/test/seq1/seqinfo.ini"
    train_ini_path = DataSet_path + "MOT16/images/train/seq2/seqinfo.ini"

    preprocessVideo(test_video_path, train_video_path)
    preprocessTxt(test_txt_path, train_txt_path,csv_path)
    
    print("finish dataset!")
