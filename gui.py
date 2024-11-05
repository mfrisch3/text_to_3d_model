import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import threading
from text_to_image import TextToImage
from depth_estimation import DepthEstimator
from point_cloud import PointCloudGenerator
from mesh_generation import MeshGenerator

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to 3D Model Generator")

        self.text_to_image = TextToImage()
        self.depth_estimator = DepthEstimator()
        self.point_cloud_generator = PointCloudGenerator()
        self.mesh_generator = MeshGenerator()

        # UI Layout
        self.prompt_label = ttk.Label(root, text="Enter description:")
        self.prompt_label.grid(row=0, column=0, padx=10, pady=10)

        self.prompt_entry = ttk.Entry(root, width=40)
        self.prompt_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ttk.Button(root, text="Generate 3D Model", command=self.generate_model)
        self.generate_button.grid(row=1, column=1, padx=10, pady=10)

        self.progress_label = ttk.Label(root, text="")
        self.progress_label.grid(row=2, column=1)

    def generate_model(self):
        user_prompt = self.prompt_entry.get()
        if not user_prompt:
            messagebox.showerror("Input Error", "Please enter a description.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".obj", filetypes=[("OBJ file", "*.obj"), ("STL file", "*.stl")])
        if not output_path:
            return

        self.progress_label.config(text="Generating...")

        # Background processing to prevent freezing
        def process():
            image_path = self.text_to_image.generate_image(user_prompt)
            depth_map = self.depth_estimator.estimate_depth(image_path)
            point_cloud = self.point_cloud_generator.depth_to_point_cloud(depth_map, image_path)
            self.mesh_generator.create_mesh_from_point_cloud(point_cloud, output_path)
            messagebox.showinfo("Success", f"3D model saved at: {output_path}")
            self.progress_label.config(text="Generation complete")

        threading.Thread(target=process).start()

# Start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
