## 필요한 모듈 import

import csv
import os

import pandas as pd
from tqdm import tqdm

from app.ai.foot_ap_angle import *
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

from app.config.config import base_dir

## inference
cfg = get_cfg()
cfg.MODEL.DEVICE = 'cpu'
cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.DATALOADER.NUM_WORKERS = 0  # On Windows environment, this value must be 0.
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.RETINANET.NUM_CLASSES = 1
cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 8
cfg.TEST.KEYPOINT_OKS_SIGMAS = np.ones((8, 1), dtype=float).tolist()
cfg.OUTPUT_DIR = os.path.join(f"{base_dir}static", "foot_ap")  # 결과물 저장된 폴더

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

cfg.MODEL.WEIGHTS = os.path.join(base_dir, "app/ai/ap_model_final.pth")  # 학습된 모델 들어가 있는 곳
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # custom testing threshold
predictor = DefaultPredictor(cfg)

keypoint_names = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'
}
edges = []


## 함수 정의
def draw_keypoints(
        image,
        keypoints,
        edges: List[Tuple[int, int]] = None,
        keypoint_names: Dict[int, str] = None,
        boxes: bool = True
) -> None:
    """
    Args:
        image (ndarray): [H, W, C]
        keypoints (ndarray): [N, 3]
        edges (List(Tuple(int, int))):
    """
    keypoints = keypoints.astype(np.int64)
    keypoints_ = keypoints.copy()
    np.random.seed(42)
    colors = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(8)}
    if len(keypoints_) == 16:
        keypoints_ = [[keypoints_[i], keypoints_[i + 1]] for i in range(0, len(keypoints_), 2)]

    assert isinstance(image, np.ndarray), "image argument does not numpy array."
    image_ = np.copy(image)
    for i, keypoint in enumerate(keypoints_):
        cv2.circle(
            image_,
            tuple(keypoint),
            3, colors.get(i), thickness=3, lineType=cv2.FILLED)

        if keypoint_names is not None:
            cv2.putText(
                image_,
                f'{i}: {keypoint_names[i]}',
                tuple(keypoint),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    if edges is not None:
        for i, edge in enumerate(edges):
            cv2.line(
                image_,
                tuple(keypoints_[edge[0]]),
                tuple(keypoints_[edge[1]]),
                colors.get(edge[0]), 3, lineType=cv2.LINE_AA)
    if boxes:
        x1, y1 = min(np.array(keypoints_)[:, 0]), min(np.array(keypoints_)[:, 1])
        x2, y2 = max(np.array(keypoints_)[:, 0]), max(np.array(keypoints_)[:, 1])
        cv2.rectangle(image_, (x1, y1), (x2, y2), (255, 100, 91), thickness=3)

    # 각도 구하기
    global hallux_valgus_angle, intermetatarsal_angle

    if keypoints_[4][0] > keypoints_[6][0]:                   # e keypoint x좌표 > g keypoint x좌표 left로 인식
        hallux_valgus_angle = calculate_angle(keypoints_[2], keypoints_[3], keypoints_[4], keypoints_[5])
        intermetatarsal_angle = calculate_angle(keypoints_[6], keypoints_[7], keypoints_[4], keypoints_[5])


    if keypoints_[4][0] < keypoints_[6][0]:                   # e keypoint x좌표 < g keypoint x좌표 right로 인식
        hallux_valgus_angle = calculate_angle(keypoints_[4], keypoints_[5], keypoints_[2], keypoints_[3])
        intermetatarsal_angle = calculate_angle(keypoints_[4], keypoints_[5], keypoints_[6], keypoints_[7])

    hallux_valgus_angle = format(hallux_valgus_angle, ".3f")
    intermetatarsal_angle = format(intermetatarsal_angle, ".3f")


    return image_


def save_samples():
    pred()

    dst_path = os.path.join(f"{base_dir}static/foot_ap", "out")
    image_path = os.path.join(f"{base_dir}static/foot_ap", "test_imgs")
    csv_path = os.path.join(f"{base_dir}static/foot_ap", "ap_prediction.csv")

    mode = "choice"
    size = 5
    index = range(len(get_files()))

    df = pd.read_csv(csv_path)

    # csv 파일로 angle 결과값 저장
    output_file = open(dst_path + '/footap_result.csv', 'w', newline='')
    f = csv.writer(output_file)
    # csv 파일에 header 추가
    f.writerow(["image", "Hallux Valgus angle", "I-II intermetatarsal angle"])

    if mode == "random":
        assert size is not None, "mode argument is random, but size argument is not given."
        choice_idx = np.random.choice(len(df), size=size, replace=False)
    if mode == "choice":
        assert index is not None, "mode argument is choice, but index argument is not given."
        choice_idx = index

    for idx in choice_idx:
        image_name = df.iloc[idx, 0]
        keypoints = df.iloc[idx, 1:]
        image = cv2.imread(os.path.join(image_path, image_name), cv2.IMREAD_COLOR)

        combined = draw_keypoints(image, keypoints, edges, keypoint_names, boxes=False)
        hallux_valgus = draw_HVA(image, keypoints, keypoint_names)
        intermetatarsal = draw_IMA(image, keypoints, keypoint_names)

        cv2.imwrite(os.path.join(dst_path, "result_" + image_name), combined)
        cv2.imwrite(os.path.join(dst_path, "hv_" + image_name), hallux_valgus)
        cv2.imwrite(os.path.join(dst_path, "im_" + image_name), intermetatarsal)

        f.writerow([image_name, hallux_valgus_angle, intermetatarsal_angle])


def get_files():
    test_dir = os.path.join(f"{base_dir}static/foot_ap", "test_imgs")  # prediction 할 test image 들어가 있는 폴더
    test_list = os.listdir(test_dir)
    test_list.sort()

    files = []

    for file in tqdm(test_list):
        files.append(file)

    return files


def pred():
    preds = []
    except_list = []

    test_dir = os.path.join(f"{base_dir}static/foot_ap", "test_imgs")  # prediction 할 test image 들어가 있는 폴더
    test_list = os.listdir(test_dir)
    test_list.sort()

    for file in tqdm(test_list):
        filepath = os.path.join(test_dir, file)
        im = cv2.imread(filepath)
        outputs = predictor(im)
        outputs = outputs["instances"].to("cpu").get("pred_keypoints").numpy()
        pred = []
        try:
            for out in outputs[0]:
                pred.extend([float(e) for e in out[:2]])
        except IndexError:
            pred.extend([0] * 24)
            except_list.append(filepath)
        preds.append(pred)

    # prediction 좌표 csv로 저장
    df_sub = pd.read_csv(f"{base_dir}static/foot_ap/footap_column.csv")  # csv columns 형식 불러오기
    df = pd.DataFrame(columns=df_sub.columns)
    df["image"] = get_files()  # image 열에 파일명 list
    df.iloc[:, 1:] = preds  # 각 행에 prediction 좌표 입력

    df.to_csv(os.path.join(cfg.OUTPUT_DIR, "ap_prediction.csv"), index=False)  # predict 좌표 csv로 저장
    if except_list:
        print(
            "The following images are not detected keypoints. The row corresponding that images names would be filled with 0 value."
        )
        print(*except_list)

