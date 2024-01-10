import numpy as np
from typing import Tuple, List, Sequence, Callable, Dict
import cv2


# Calcaneal pitch 각도 구하는 함수
def calculate_calcaneal(b, c, d):
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)

    radians = np.arctan2(b[1] - c[1], b[0] - c[0]) - np.arctan2(b[1] - d[1], b[0] - d[0])
    angle = radians * 180.0 / np.pi

    if abs(angle) > 180.0:
        angle = 360 - abs(angle)

    return angle


# Boehler angle 구하는 함수
def calculate_boehler(j, k, l):
    j = np.array(j)
    k = np.array(k)
    l = np.array(l)

    radians = np.arctan2(j[1] - k[1], j[0] - k[0]) - np.arctan2(k[1] - l[1], k[0] - l[0])
    angle = radians * 180.0 / np.pi

    if abs(angle) > 180.0:
        angle = 360 - abs(angle)

    return angle


# Meary's angle, Talar declination angle 구하는 함수
def calculate_4point_angle(f, g, h, i):
    f = np.array(f)
    g = np.array(g)
    h = np.array(h)
    i = np.array(i)

    radians = np.arctan2(h[1] - i[1], h[0] - i[0]) - np.arctan2(f[1] - g[1], f[0] - g[0])
    angle = radians * 180.0 / np.pi

    if abs(angle) > 180.0:
        angle = 360 - abs(angle)

    return angle


# Calcaneal pitch
def draw_calcaneal_sesa(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints1 = keypoints.astype(np.int64)
    keypoints1_ = keypoints1.copy()
    np.random.seed(42)
    colors1 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    if len(keypoints1_) == 24:
        keypoints1_ = [[keypoints1_[i], keypoints1_[i + 1]] for i in range(0, len(keypoints1_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image1_ = np.copy(image)
    cv2.circle(image1_, tuple(keypoints1_[1]), 3, colors1.get(1), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{1}: {keypoint_names[1]}', tuple(keypoints1_[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image1_, tuple(keypoints1_[2]), 3, colors1.get(2), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{2}: {keypoint_names[2]}', tuple(keypoints1_[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image1_, tuple(keypoints1_[4]), 3, colors1.get(4), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image1_, f'{4}: {keypoint_names[4]}', tuple(keypoints1_[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.line(image1_, tuple(keypoints1_[1]), tuple(keypoints1_[2]), colors1.get(2), 3, lineType=cv2.LINE_AA)
    cv2.line(image1_, tuple(keypoints1_[1]), tuple(keypoints1_[4]), colors1.get(4), 3, lineType=cv2.LINE_AA)

    return image1_


def draw_calcaneal_5th(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints0 = keypoints.astype(np.int64)
    keypoints0_ = keypoints0.copy()
    np.random.seed(42)
    colors0 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    if len(keypoints0_) == 24:
        keypoints0_ = [[keypoints0_[i], keypoints0_[i + 1]] for i in range(0, len(keypoints0_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image0_ = np.copy(image)

    cv2.circle(image0_, tuple(keypoints0_[1]), 3, colors0.get(1), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image0_, f'{1}: {keypoint_names[1]}', tuple(keypoints0_[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image0_, tuple(keypoints0_[2]), 3, colors0.get(2), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image0_, f'{2}: {keypoint_names[2]}', tuple(keypoints0_[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image0_, tuple(keypoints0_[3]), 3, colors0.get(3), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image0_, f'{3}: {keypoint_names[3]}', tuple(keypoints0_[3]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.line(image0_, tuple(keypoints0_[1]), tuple(keypoints0_[2]), colors0.get(2), 3, lineType=cv2.LINE_AA)
    cv2.line(image0_, tuple(keypoints0_[1]), tuple(keypoints0_[3]), colors0.get(3), 3, lineType=cv2.LINE_AA)

    return image0_


# Boehler angle
def draw_boehler(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints2 = keypoints.astype(np.int64)
    keypoints2_ = keypoints2.copy()
    np.random.seed(42)
    colors2 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    if len(keypoints2_) == 24:
        keypoints2_ = [[keypoints2_[i], keypoints2_[i + 1]] for i in range(0, len(keypoints2_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image2_ = np.copy(image)

    cv2.circle(image2_, tuple(keypoints2_[9]), 3, colors2.get(9), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{9}: {keypoint_names[9]}', tuple(keypoints2_[9]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image2_, tuple(keypoints2_[10]), 3, colors2.get(10), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{10}: {keypoint_names[10]}', tuple(keypoints2_[10]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0),
                1)
    cv2.circle(image2_, tuple(keypoints2_[11]), 3, colors2.get(11), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image2_, f'{11}: {keypoint_names[11]}', tuple(keypoints2_[11]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0),
                1)
    cv2.line(image2_, tuple(keypoints2_[9]), tuple(keypoints2_[10]), colors2.get(9), 3, lineType=cv2.LINE_AA)
    cv2.line(image2_, tuple(keypoints2_[10]), tuple(keypoints2_[11]), colors2.get(10), 3, lineType=cv2.LINE_AA)

    return image2_


# Meary's angle
def draw_meary(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints3 = keypoints.astype(np.int64)
    keypoints3_ = keypoints3.copy()
    np.random.seed(42)
    colors3 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    if len(keypoints3_) == 24:
        keypoints3_ = [[keypoints3_[i], keypoints3_[i + 1]] for i in range(0, len(keypoints3_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image3_ = np.copy(image)
    cv2.circle(image3_, tuple(keypoints3_[5]), 3, colors3.get(5), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image3_, f'{5}: {keypoint_names[5]}', tuple(keypoints3_[5]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image3_, tuple(keypoints3_[6]), 3, colors3.get(6), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image3_, f'{6}: {keypoint_names[6]}', tuple(keypoints3_[6]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image3_, tuple(keypoints3_[7]), 3, colors3.get(7), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image3_, f'{7}: {keypoint_names[7]}', tuple(keypoints3_[7]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image3_, tuple(keypoints3_[8]), 3, colors3.get(3), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image3_, f'{8}: {keypoint_names[8]}', tuple(keypoints3_[8]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)

    cv2.line(image3_, tuple(keypoints3_[5]), tuple(keypoints3_[6]), colors3.get(5), 3, lineType=cv2.LINE_AA)
    cv2.line(image3_, tuple(keypoints3_[7]), tuple(keypoints3_[8]), colors3.get(7), 3, lineType=cv2.LINE_AA)

    return image3_


# Talar declination angle
def draw_talar(image, keypoints, keypoint_names: Dict[int, str] = None):
    keypoints4 = keypoints.astype(np.int64)
    keypoints4_ = keypoints4.copy()
    np.random.seed(42)
    colors4 = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    if len(keypoints4_) == 24:
        keypoints4_ = [[keypoints4_[i], keypoints4_[i + 1]] for i in range(0, len(keypoints4_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image4_ = np.copy(image)
    cv2.circle(image4_, tuple(keypoints4_[1]), 3, colors4.get(1), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image4_, f'{1}: {keypoint_names[1]}', tuple(keypoints4_[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image4_, tuple(keypoints4_[4]), 3, colors4.get(4), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image4_, f'{4}: {keypoint_names[4]}', tuple(keypoints4_[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image4_, tuple(keypoints4_[7]), 3, colors4.get(7), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image4_, f'{7}: {keypoint_names[7]}', tuple(keypoints4_[7]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)
    cv2.circle(image4_, tuple(keypoints4_[8]), 3, colors4.get(8), thickness=3, lineType=cv2.FILLED)
    cv2.putText(image4_, f'{8}: {keypoint_names[8]}', tuple(keypoints4_[8]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                1)

    cv2.line(image4_, tuple(keypoints4_[1]), tuple(keypoints4_[4]), colors4.get(4), 3, lineType=cv2.LINE_AA)
    cv2.line(image4_, tuple(keypoints4_[7]), tuple(keypoints4_[8]), colors4.get(7), 3, lineType=cv2.LINE_AA)

    return image4_
