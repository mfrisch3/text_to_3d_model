import open3d as o3d

class MeshGenerator:
    def __init__(self):
        pass

    def create_mesh_from_point_cloud(self, point_cloud, output_path="output_model.obj"):
        point_cloud.estimate_normals()
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)
        o3d.io.write_triangle_mesh(output_path, mesh)
        return output_path
