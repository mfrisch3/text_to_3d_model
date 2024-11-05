import torch
import cv2

class DepthEstimator:
    def __init__(self):
        self.midas = torch.hub.load("intel-isl/MiDaS", "MiDaS").to("cuda").eval()
        self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").default_transform

    def estimate_depth(self, image_path):
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_batch = self.transform(img_rgb).to("cuda")

        # Estimate depth
        with torch.no_grad():
            prediction = self.midas(input_batch)
            depth_map = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_rgb.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        return depth_map.cpu().numpy()
