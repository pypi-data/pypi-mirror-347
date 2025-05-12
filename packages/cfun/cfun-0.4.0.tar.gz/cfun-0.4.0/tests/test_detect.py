from pathlib import Path

from cfundata import cdata

from cfun.yolo.classify import YOLOClassifier
from cfun.yolo.detect import YOLODetector


def test_detect():
    onnx_path = Path(cdata.DX_DET_ONNX)

    img_path = Path(__file__).parent / Path("images") / "image_detect_01.png"
    print(f"img_path: {img_path}")
    print(type(img_path))
    assert img_path.exists(), f"img_path: {img_path} 不存在"
    assert onnx_path.exists(), f"onnx_path: {onnx_path} 不存在"
    detector = YOLODetector(onnx_path)

    detections, original_img = detector.detect(img_path)
    for det in detections:
        print(det)
    detector.draw_results(original_img, detections, save_path="result1.png")


def test_classify():
    onnx_file = cdata.DX_CLS_ONNX
    print(f"onnx_file: {onnx_file}")
    print(type(onnx_file))
    img_path = Path(__file__).parent / "images" / "image_cls_01.png"
    print(f"img_path: {img_path}")
    print(type(img_path))
    assert img_path.exists(), f"img_path: {img_path} 不存在"
    assert onnx_file.exists(), f"onnx_file: {onnx_file} 不存在"

    # from all_name import all_names
    all_names = {
        0: "cat",
        1: "dog",
        1307: "阿",
    }  # 示例字典

    classifier = YOLOClassifier(model_path=onnx_file, all_names=all_names)

    class_id, class_name, confidence = classifier.classify(img_path)

    print(f"预测类别: {class_name} (ID: {class_id}), 置信度: {confidence:.4f}")
    assert class_id == 1307, "分类结果不正确"


if __name__ == "__main__":
    test_detect()
    test_classify()
