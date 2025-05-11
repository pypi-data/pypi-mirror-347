from pathlib import Path
from typing import Optional

import numpy as np
import onnxruntime as ort
from PIL import Image


class YOLOClassifier:
    """yolo 分类器(采用 PIL 库处理图像)

    Attributes:
        session (onnxruntime.InferenceSession): ONNX 推理会话
        input_name (str): 模型输入名称

    """

    def __init__(
        self,
        model_path: str | Path,
        all_names: dict[int, str],
        input_size: tuple[int, int] = (64, 64),
        providers: Optional[list] = None,
    ):
        """初始化分类器

        Args:
            model_path (str | Path): 模型路径
            all_names (dict[int, str]): 类别字典，如 {0: "cat", 1: "dog", ...}
            input_size (tuple[int, int], optional): 模型输入图像尺寸 (W, H). Defaults to (64, 64).
            providers (Optional[list], optional): ONNX 推理后端. Defaults to None.
        """
        self.model_path = Path(model_path)
        if providers is None:
            providers = ["CPUExecutionProvider"]
        self.all_names = all_names
        self.input_size = input_size

        self.session = ort.InferenceSession(self.model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name

    def _preprocess(self, img_path: str | Path) -> np.ndarray:
        """预处理图像
        Args:
            img_path (str | Path): 图像路径

        Returns:
            np.ndarray: 预处理后的图像（NCHW 格式）

        """
        img = Image.open(img_path).convert("RGB")  # 打开图像并确保为 RGB
        img = img.resize(
            self.input_size, Image.BILINEAR
        )  # 调整大小,后面的是一种插值算法
        img = np.array(img).astype(np.float32) / 255.0  # 转为 float32 并归一化
        img = np.transpose(img, (2, 0, 1))  # HWC → CHW
        img = np.expand_dims(img, axis=0)  # 添加 batch 维度 → NCHW
        # ascontiguousarray函数将一个内存不连续存储的数组转换为内存连续存储的数组，使得运行速度更快。
        img = np.ascontiguousarray(img)
        return img

    def _infer(self, img):
        """推理"""
        return self.session.run(None, {self.input_name: img})[0]

    def classify(self, img_path: str | Path) -> tuple[int, str, float]:
        """根据输入的图像进行分类

        Args:
            img_path (str | Path): 图像路径

        Returns:
            tuple: (class_id, class_name, confidence)
                - class_id (int): 预测的类别 ID
                - class_name (str):  预测的类别名称
                - confidence (float): 预测的置信度

        Example:
            ````python
            from cfun.yolo.classify import YOLOClassifier
            # 假设你有一个名为 "model.onnx" 的 ONNX 模型文件
            # 并且你有一个类别字典 all_names, 例如 {0: "cat", 1: "dog"}
            classifier = YOLOClassifier(model_path="model.onnx", all_names={0: "cat", 1: "dog"})
            class_id, class_name, confidence = classifier.classify("path/to/image.jpg")
            print(f"预测类别: {class_name} (ID: {class_id}), 置信度: {confidence:.4f}")
            ````

        """
        img = self._preprocess(img_path)
        outputs = self._infer(img)
        probs = outputs[0]
        if probs.ndim == 2:
            probs = probs[0]
        class_id = int(np.argmax(probs))
        confidence = float(probs[class_id])
        class_name = self.all_names.get(class_id, f"class_{class_id}")
        return class_id, class_name, confidence


if __name__ == "__main__":
    # from all_name import all_names
    all_names = {0: "cat", 1: "dog"}  # 示例字典
    from cfundata import cdata

    # 加载自己的模型文件
    classifier = YOLOClassifier(model_path=cdata.DX_CLS_ONNX, all_names=all_names)

    img_path = "assets/image_cls_01.png"
    class_id, class_name, confidence = classifier.classify(img_path)

    print(f"预测类别: {class_name} (ID: {class_id}), 置信度: {confidence:.4f}")
