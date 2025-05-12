from pathlib import Path
from typing import Optional, Union

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw


class YOLODetector:
    """yolo检测器

    Attributes:
        session: ONNX Runtime inference session.
        input_name: Name of the input tensor.
        input_size: Size of the input image.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        input_size: tuple[int, int] = (640, 640),
        providers: Optional[list] = None,
    ):
        """初始化

        Args:
            model_path (str or Path): Path to the ONNX model file.
            input_size (tuple): Size of the input image (width, height).
            providers (list): List of execution providers for ONNX Runtime.

        """
        if providers is None:
            providers = ["CPUExecutionProvider"]
        self.session = ort.InferenceSession(model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name
        self.input_size = input_size

    def _letterbox(
        self,
        img: Image.Image,
        new_shape: tuple[int, int] = (640, 640),
        color: tuple[int, int, int] = (114, 114, 114),
        scaleup: bool = True,
    ) -> tuple[Image.Image, float, tuple[float, float]]:
        """重新调整图像大小，保持纵横比并填充空白区域

        Args:
            img (PIL.Image): Input image.
            new_shape (tuple): New shape for the image (width, height).
            color (tuple): Color for the padding (R, G, B).
            scaleup (bool): Whether to scale up the image if it's smaller than new_shape.

        Returns:
            tuple: Tuple containing the resized image, the resize ratio, and the padding (dw, dh).

        """
        shape = img.size  # (width, height)
        r = min(new_shape[0] / shape[1], new_shape[1] / shape[0])
        if not scaleup:
            r = min(r, 1.0)

        new_unpad = (int(round(shape[0] * r)), int(round(shape[1] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2

        img = img.resize(new_unpad, Image.BILINEAR)
        new_img = Image.new("RGB", new_shape, color)
        new_img.paste(img, (int(dw), int(dh)))
        return new_img, r, (dw, dh)

    def _preprocess(self, img_path):
        img0 = Image.open(img_path).convert("RGB")
        img, ratio, (dw, dh) = self._letterbox(img0, self.input_size)
        img = np.array(img).astype(np.float32) / 255.0  # HWC, RGB
        img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]  # NCHW
        return img, img0, ratio, dw, dh

    def _infer(self, img):
        return self.session.run(None, {self.input_name: img})[0]

    def detect(
        self, img_path: Union[str, Path], conf_thres: float = 0.65
    ) -> tuple[list, Image.Image]:
        """检测图像中的物体

        Args:
            img_path (Union[str, Path]): Path to the input image.
            conf_thres (float): Confidence threshold for filtering detections.

        Returns:
            list: List of detected objects, each represented as a dictionary with keys 'box', 'conf', and 'cls'.
            PIL.Image: Original image.

        Example:
            ```python
            from cfundata import cdata.DX_DET_ONNX
            det = YOLODetector(cdata.DX_DET_ONNX)
            img_path1 = "assets/image_detect_01.png"
            data, original_img = det.detect(img_path1)
            for det in data:
                print(det)
            det.draw_results(original_img, data, save_path="result1.png")
            ```
        """
        img, img0, ratio, dw, dh = self._preprocess(img_path)
        preds = self._infer(img)[0]
        # | 图像对象类型  | 获取尺寸方式            | 备注         |
        # | ------------ | -------------------- | ---------- |
        # | PIL.Image  | img.size → (w, h)     | 宽在前，返回元组   |
        # | np.ndarray | img.shape → (h, w, c) | 高在前，通道数可能有 |
        h0, w0 = img0.size[1], img0.size[0]
        detections = []
        for det in preds:
            x1, y1, x2, y2, conf, dcls = det
            if conf < conf_thres:
                continue
            x1 = np.clip((x1 - dw) / ratio, 0, w0 - 1)
            y1 = np.clip((y1 - dh) / ratio, 0, h0 - 1)
            x2 = np.clip((x2 - dw) / ratio, 0, w0 - 1)
            y2 = np.clip((y2 - dh) / ratio, 0, h0 - 1)
            # 返回 box类型的坐标
            detections.append(
                {
                    "box": [int(x1), int(y1), int(x2), int(y2)],
                    "conf": round(float(conf), 2),
                    "cls": int(dcls),
                }
            )

        return detections, img0

    def draw_results(self, img, detections, save_path="result.png"):
        """在图像上绘制检测结果

        Args:
            img (PIL.Image): Original image.
            detections (list): List of detected objects.
            save_path (str): Path to save the result image.

        Example:
            ```python
            from cfundata import cdata
            det = YOLODetector(cdata.DX_DET_ONNX)
            img_path1 = "assets/image_detect_01.png"
            data, original_img = det.detect(img_path1)
            for det in data:
                print(det)
            det.draw_results(original_img, data, save_path="result1.png")
            ```
        """
        draw = ImageDraw.Draw(img)
        for det in detections:
            box = det["box"]
            conf = det["conf"]
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 0), width=2)
            draw.text((x1, y1 - 10), f"{det['cls']} {conf:.2f}", fill=(255, 0, 0))
        img.save(save_path)


if __name__ == "__main__":
    from cfundata import cdata

    det = YOLODetector(cdata.DX_DET_ONNX)

    img_path1 = "assets/image_detect_01.png"
    data, original_img = det.detect(img_path1)
    for det in data:
        print(det)
    det.draw_results(original_img, data, save_path="result1.png")
