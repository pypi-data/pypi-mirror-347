from pathlib import Path

from cfun.sfz.idcardocr import IDCardOCR


# 示例用法
def test_sfz():
    model_path = Path("model/sfz_det.onnx")
    idcard = IDCardOCR(model_path)  # 创建sfz处理器实例

    images = [f for f in Path("idcard").rglob("*.jpg") if f.is_file()]

    images = sorted(images)
    df = []
    for img_path in images:
        try:
            info = idcard.process_image(img_path)
            df.append(info)
            print(f"Processed {img_path}:\n{info}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            break


if __name__ == "__main__":
    test_sfz()
