import numpy as np
from typing import Tuple, List, Sequence, Callable, Dict
import cv2


# angle 구하는 함수
def calculate_angle(c, d, e, f):
    c = np.array(c)
    d = np.array(d)
    e = np.array(e)
    f = np.array(f)

    radians = np.arctan2(f[1] - e[1], f[0] - e[0]) - np.arctan2(d[1] - c[1], d[0] - c[0])
    angle = radians * 180.0 / np.pi

    if angle > 180.0:
        angle = 360 - angle

    return angle


# hallux valgus line 그리기
def draw_HVA(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints1 = keypoints.astype(np.int64)
    keypoints1_ = keypoints1.copy()
    np.random.seed(42)
    colors1 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(16)}
    if len(keypoints1_) == 16:
        keypoints1_ = [[keypoints1_[i], keypoints1_[i + 1]] for i in range(0, len(keypoints1_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image1_ = np.copy(image)
    cv2.circle(image1_, tuple(keypoints1_[2]), 3, colors1.get(2), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{2}: {keypoint_names[2]}', tuple(keypoints1_[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image1_, tuple(keypoints1_[3]), 3, colors1.get(3), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{3}: {keypoint_names[3]}', tuple(keypoints1_[3]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image1_, tuple(keypoints1_[4]), 3, colors1.get(4), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{4}: {keypoint_names[4]}', tuple(keypoints1_[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image1_, tuple(keypoints1_[5]), 3, colors1.get(5), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{5}: {keypoint_names[5]}', tuple(keypoints1_[5]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)

    # e-f 연장선 그리기
    if keypoints1_[4][0] != keypoints1_[5][0]:
        m = (keypoints1_[4][1] - keypoints1_[5][1]) / (keypoints1_[4][0] - keypoints1_[5][0])
        a = keypoints1_[4][1] - (m * keypoints1_[4][0])
        x3 = (keypoints1_[2][1] - a) / m

    if keypoints1_[4][0] == keypoints1_[5][0]:
        x3 = keypoints1_[4][0]

    # c-d 연장선 그리기
    if keypoints1_[2][0] != keypoints1_[3][0]:
        n = (keypoints1_[2][1] - keypoints1_[3][1]) / (keypoints1_[2][0] - keypoints1_[3][0])
        b = keypoints1_[2][1] - (n * keypoints1_[2][0])
        x4 = (keypoints1_[5][1] - b) / n
    if keypoints1_[2][0] == keypoints1_[3][0]:
        x4 = keypoints1_[2][0]

    cv2.line(image1_, tuple(keypoints1_[2]), (int(x4), keypoints1_[5][1]), colors1.get(3), 3, lineType=cv2.LINE_AA)
    cv2.line(image1_, (int(x3), keypoints1_[2][1]), tuple(keypoints1_[5]), colors1.get(4), 3, lineType=cv2.LINE_AA)

    return image1_


# I-II intermetatarsal line 그리기
def draw_IMA(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints2 = keypoints.astype(np.int64)
    keypoints2_ = keypoints2.copy()
    np.random.seed(42)
    colors1 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(16)}
    if len(keypoints2_) == 16:
        keypoints2_ = [[keypoints2_[i], keypoints2_[i + 1]] for i in range(0, len(keypoints2_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image2_ = np.copy(image)
    cv2.circle(image2_, tuple(keypoints2_[4]), 3, colors1.get(4), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{4}: {keypoint_names[4]}', tuple(keypoints2_[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image2_, tuple(keypoints2_[5]), 3, colors1.get(5), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{5}: {keypoint_names[5]}', tuple(keypoints2_[5]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image2_, tuple(keypoints2_[6]), 3, colors1.get(6), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{6}: {keypoint_names[6]}', tuple(keypoints2_[6]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image2_, tuple(keypoints2_[7]), 3, colors1.get(7), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{7}: {keypoint_names[7]}', tuple(keypoints2_[7]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)

    # e-f 연장선 그리기
    if keypoints2_[4][0] != keypoints2_[5][0]:
        j = (keypoints2_[4][1] - keypoints2_[5][1]) / (keypoints2_[4][0] - keypoints2_[5][0])
        c = keypoints2_[4][1] - (j * keypoints2_[4][0])
        x5 = (image2_.shape[1] - c) / j

    if keypoints2_[4][0] == keypoints2_[5][0]:
        x5 = keypoints2_[4][0]

    # c-d 연장선 그리기
    if keypoints2_[6][0] != keypoints2_[7][0]:
        k = (keypoints2_[6][1] - keypoints2_[7][1]) / (keypoints2_[6][0] - keypoints2_[7][0])
        d = keypoints2_[6][1] - (k * keypoints2_[6][0])
        x6 = (image2_.shape[1] - d) / k
    if keypoints2_[6][0] == keypoints2_[7][0]:
        x6 = keypoints2_[6][0]

    cv2.line(image2_, tuple(keypoints2_[4]), (int(x5), image2_.shape[1]), colors1.get(4), 3, lineType=cv2.LINE_AA)
    cv2.line(image2_, tuple(keypoints2_[6]), (int(x6), image2_.shape[1]), colors1.get(6), 3, lineType=cv2.LINE_AA)

    return image2_
