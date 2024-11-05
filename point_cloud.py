import numpy as np
import open3d as o3d
import cv2

class PointCloudGenerator:
    def __init__(self):
        pass

    def depth_to_point_cloud(self, depth_map, img_path):
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width = depth_map.shape
        point_cloud = o3d.geometry.PointCloud()
        points, colors = [], []
        fx = fy = 500  # Focal length
        cx, cy = width / 2, height / 2

        for v in range(height):
            for u in range(width):
                z = depth_map[v, u]
                if z == 0:
                    continue
                x = (u - cx) * z / fx
                y = (v - cy) * z / fy
                points.append([x, y, z])
                colors.append(img_rgb[v, u] / 255.0)

        point_cloud.points = o3d.utility.Vector3dVector(np.array(points))
        point_cloud.colors = o3d.utility.Vector3dVector(np.array(colors))
        return point_cloud
