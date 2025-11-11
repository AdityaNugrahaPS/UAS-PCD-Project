import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from modules import basic_ops, about

class ImageProcessingApp:
    def edge_detection(self, method):
        if self.processed_image:
            from modules import edge_detection
            func = getattr(edge_detection, method, None)
            if func:
                result = func(self.processed_image)
                self.processed_image = result
                self.display_image(result)
            else:
                messagebox.showerror("Error", f"Metode edge detection '{method}' tidak ditemukan.")
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def show_about(self):
        from modules import about
        messagebox.showinfo("Tentang Kelompok", about.get_about_text())
    def segmentation_watershed(self):
        if self.processed_image:
            from modules import segmentation
            result = segmentation.watershed(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def segmentation_region_growing(self):
        if self.processed_image:
            from modules import segmentation
            result = segmentation.region_growing(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def segmentation_thresholding(self):
        if self.processed_image:
            from modules import segmentation
            result = segmentation.thresholding(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def enhance_contrast(self):
        if self.processed_image:
            from modules import enhancement
            factor = self.ask_slider_float("Contrast", "Faktor kontras", 0.1, 3.0, 1.2)
            if factor is not None:
                result = enhancement.contrast(self.processed_image, factor)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def enhance_brightness(self):
        if self.processed_image:
            from modules import enhancement
            factor = self.ask_slider_float("Brightness", "Faktor kecerahan", 0.1, 3.0, 1.2)
            if factor is not None:
                result = enhancement.brightness(self.processed_image, factor)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("800x600")
        self.image = None
        self.image_path = None
        self.processed_image = None
        self.undo_stack = []
        self.redo_stack = []
        self.create_menu()
        self.create_toolbar()  # Tambahkan toolbar
        self.create_canvas()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg='#f8fafc')
        # Load icons
        try:
            undo_img = Image.open(os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'undo.png'))
            undo_img = undo_img.resize((16, 16), Image.LANCZOS)
            self.undo_icon = ImageTk.PhotoImage(undo_img)
        except Exception:
            self.undo_icon = None
        try:
            redo_img = Image.open(os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'redo.png'))
            redo_img = redo_img.resize((16, 16), Image.LANCZOS)
            self.redo_icon = ImageTk.PhotoImage(redo_img)
        except Exception:
            self.redo_icon = None
        # Undo Button
        undo_btn = tk.Button(toolbar, image=self.undo_icon, command=self.undo, bg='#f1f5f9', relief=tk.FLAT, bd=0, padx=2, pady=2)
        if not self.undo_icon:
            undo_btn.config(text='Undo')
        undo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        # Redo Button
        redo_btn = tk.Button(toolbar, image=self.redo_icon, command=self.redo, bg='#f1f5f9', relief=tk.FLAT, bd=0, padx=2, pady=2)
        if not self.redo_icon:
            redo_btn.config(text='Redo')
        redo_btn.pack(side=tk.LEFT, padx=2, pady=2)



        toolbar.pack(side=tk.TOP, anchor='w', padx=2, pady=2)



    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_as_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu (Undo/Redo)
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.root.bind_all("<Control-z>", lambda e: self.undo())
        self.root.bind_all("<Control-y>", lambda e: self.redo())

        # Basic Ops Menu
        basic_menu = tk.Menu(menubar, tearoff=0)
        basic_menu.add_command(label="Negative", command=self.negative_image)
        arithmetic_menu = tk.Menu(basic_menu, tearoff=0)
        arithmetic_menu.add_command(label="Add", command=lambda: self.arithmetic_image('add'))
        arithmetic_menu.add_command(label="Subtract", command=lambda: self.arithmetic_image('subtract'))
        arithmetic_menu.add_command(label="Multiply", command=lambda: self.arithmetic_image('multiply'))
        arithmetic_menu.add_command(label="Divide", command=lambda: self.arithmetic_image('divide'))
        basic_menu.add_cascade(label="Arithmetic", menu=arithmetic_menu)
        boolean_menu = tk.Menu(basic_menu, tearoff=0)
        boolean_menu.add_command(label="NOT", command=lambda: self.boolean_image('not'))
        boolean_menu.add_command(label="AND", command=lambda: self.boolean_image('and'))
        boolean_menu.add_command(label="OR", command=lambda: self.boolean_image('or'))
        boolean_menu.add_command(label="XOR", command=lambda: self.boolean_image('xor'))
        basic_menu.add_cascade(label="Boolean", menu=boolean_menu)
        geom_menu = tk.Menu(basic_menu, tearoff=0)
        geom_menu.add_command(label="Translation", command=self.geom_translation)
        geom_menu.add_command(label="Rotation", command=self.geom_rotation)
        geom_menu.add_command(label="Zooming", command=self.geom_zooming)
        geom_menu.add_command(label="Flipping", command=self.geom_flipping)
        geom_menu.add_command(label="Cropping", command=self.geom_cropping)
        basic_menu.add_cascade(label="Geometrics", menu=geom_menu)
        basic_menu.add_command(label="Thresholding", command=self.thresholding_image)
        basic_menu.add_command(label="Convolution", command=self.convolution_image)
        basic_menu.add_command(label="Fourier Transform", command=self.fourier_image)
        colouring_menu = tk.Menu(basic_menu, tearoff=0)
        colouring_menu.add_command(label="Binary", command=lambda: self.colouring_image('binary'))
        colouring_menu.add_command(label="Grayscale", command=lambda: self.colouring_image('grayscale'))
        colouring_menu.add_command(label="RGB", command=lambda: self.colouring_image('rgb'))
        colouring_menu.add_command(label="HSV", command=lambda: self.colouring_image('hsv'))
        colouring_menu.add_command(label="CMY", command=lambda: self.colouring_image('cmy'))
        colouring_menu.add_command(label="YUV", command=lambda: self.colouring_image('yuv'))
        colouring_menu.add_command(label="YIQ", command=lambda: self.colouring_image('yiq'))
        colouring_menu.add_command(label="Pseudo", command=lambda: self.colouring_image('pseudo'))
        basic_menu.add_cascade(label="Colouring", menu=colouring_menu)
        menubar.add_cascade(label="Basic Ops", menu=basic_menu)

        # Enhancement Menu
        enhancement_menu = tk.Menu(menubar, tearoff=0)
        enhancement_menu.add_command(label="Brightness", command=self.enhance_brightness)
        enhancement_menu.add_command(label="Contrast", command=self.enhance_contrast)
        enhancement_menu.add_command(label="Histogram Equalization", command=self.enhance_histogram)
        smoothing_menu = tk.Menu(enhancement_menu, tearoff=0)
        smoothing_menu.add_command(label="Spatial Domain", command=self.smoothing_spatial)
        smoothing_menu.add_command(label="Frequency Domain", command=self.smoothing_frequency)
        enhancement_menu.add_cascade(label="Smoothing", menu=smoothing_menu)
        sharpening_menu = tk.Menu(enhancement_menu, tearoff=0)
        sharpening_menu.add_command(label="Spatial Domain", command=self.sharpening_spatial)
        sharpening_menu.add_command(label="Frequency Domain", command=self.sharpening_frequency)
        enhancement_menu.add_cascade(label="Sharpening", menu=sharpening_menu)
        enhancement_menu.add_command(label="Geometric Correction", command=self.geometric_correction)
        menubar.add_cascade(label="Enhancement", menu=enhancement_menu)

        # Noise Menu
        noise_menu = tk.Menu(menubar, tearoff=0)
        noise_menu.add_command(label="Gaussian", command=self.noise_gaussian)
        noise_menu.add_command(label="Rayleigh", command=self.noise_rayleigh)
        noise_menu.add_command(label="Erlang", command=self.noise_erlang)
        noise_menu.add_command(label="Exponential", command=self.noise_exponential)
        noise_menu.add_command(label="Uniform", command=self.noise_uniform)
        noise_menu.add_command(label="Impulse", command=self.noise_impulse)
        menubar.add_cascade(label="Noise", menu=noise_menu)

        # Edge Detection Menu
        edge_menu = tk.Menu(menubar, tearoff=0)
        edge_menu.add_command(label="Sobel", command=lambda: self.edge_detection('sobel'))
        edge_menu.add_command(label="Prewitt", command=lambda: self.edge_detection('prewitt'))
        edge_menu.add_command(label="Roberts", command=lambda: self.edge_detection('roberts'))
        edge_menu.add_command(label="Laplacian", command=lambda: self.edge_detection('laplacian'))
        edge_menu.add_command(label="LoG", command=lambda: self.edge_detection('log'))
        edge_menu.add_command(label="Canny", command=lambda: self.edge_detection('canny'))
        edge_menu.add_command(label="Compass (Kirsch)", command=lambda: self.edge_detection('compass'))
        menubar.add_cascade(label="Edge Detection", menu=edge_menu)

        # Segmentation Menu
        segmentation_menu = tk.Menu(menubar, tearoff=0)
        segmentation_menu.add_command(label="Thresholding", command=self.segmentation_thresholding)
        segmentation_menu.add_command(label="Region Growing", command=self.segmentation_region_growing)
        segmentation_menu.add_command(label="Watershed", command=self.segmentation_watershed)
        menubar.add_cascade(label="Segmentation", menu=segmentation_menu)

        # About Menu
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Kelompok", command=self.show_about)
        menubar.add_cascade(label="About", menu=about_menu)
        self.root.config(menu=menubar)
    def push_undo(self):
        if self.processed_image:
            self.undo_stack.append(self.processed_image.copy())
            # Clear redo stack on new operation
            self.redo_stack.clear()

    def undo(self, event=None):
        if self.undo_stack:
            if self.processed_image:
                self.redo_stack.append(self.processed_image.copy())
            self.processed_image = self.undo_stack.pop()
            self.display_image(self.processed_image)
        else:
            messagebox.showinfo("Undo", "Tidak ada operasi untuk dibatalkan.")

    def redo(self, event=None):
        if self.redo_stack:
            if self.processed_image:
                self.undo_stack.append(self.processed_image.copy())
            self.processed_image = self.redo_stack.pop()
            self.display_image(self.processed_image)
        else:
            messagebox.showinfo("Redo", "Tidak ada operasi untuk diulang.")

    def enhance_histogram(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.histogram_equalization(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def smoothing_spatial(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.smoothing_spatial(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def smoothing_frequency(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.smoothing_frequency(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def sharpening_spatial(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.sharpening_spatial(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def sharpening_frequency(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.sharpening_frequency(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geometric_correction(self):
        if self.processed_image:
            from modules import enhancement
            result = enhancement.geometric_correction(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def noise_gaussian(self):
        if self.processed_image:
            from modules import noise
            result = noise.gaussian(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def noise_rayleigh(self):
        if self.processed_image:
            from modules import noise
            result = noise.rayleigh(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def noise_erlang(self):
        if self.processed_image:
            from modules import noise
            result = noise.erlang(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def noise_exponential(self):
        if self.processed_image:
            from modules import noise
            result = noise.exponential(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def noise_uniform(self):
        if self.processed_image:
            from modules import noise
            result = noise.uniform(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def noise_impulse(self):
        if self.processed_image:
            from modules import noise
            result = noise.impulse(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='gray')
        self.canvas.pack(pady=20)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not file_path:
            return
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.png', '.jpg', '.jpeg', '.bmp']:
            messagebox.showerror("Error", "File format tidak didukung!")
            return
        try:
            img = Image.open(file_path)
            self.image = img.convert('RGB')
            self.processed_image = self.image.copy()
            self.image_path = file_path
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka gambar: {e}")

    def save_image(self):
        if self.processed_image and self.image_path:
            try:
                self.processed_image.save(self.image_path)
                messagebox.showinfo("Success", "Gambar berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")
        else:
            messagebox.showwarning("Warning", "Tidak ada gambar untuk disimpan.")

    def save_as_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp")]
            )
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Success", "Gambar berhasil disimpan.")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")
        else:
            messagebox.showwarning("Warning", "Tidak ada gambar untuk disimpan.")

    def display_image(self, img):
        img_resized = img.copy()
        img_resized.thumbnail((500, 400))
        self.photo = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        self.canvas.create_image(250, 200, image=self.photo)


    def negative_image(self):
        if self.processed_image:
            self.push_undo()
            result = basic_ops.negative(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def arithmetic_image(self, op):
        if self.processed_image:
            value = self.ask_slider_int("Arithmetic Value", f"Nilai untuk {op.capitalize()}", -255, 255, 50)
            if value is not None:
                self.push_undo()
                result = basic_ops.arithmetic(self.processed_image, value, op)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def boolean_image(self, op):
        if self.processed_image:
            value = 0x0F if op != 'not' else 0
            if op != 'not':
                value = self.ask_slider_int("Boolean Value", f"Nilai integer untuk {op.upper()}", 0, 255, 15)
            self.push_undo()
            result = basic_ops.boolean(self.processed_image, value, op)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geom_translation(self):
        if self.processed_image:
            dx = self.ask_slider_int("Translasi", "dx (kanan/kiri, px)", -500, 500, 20)
            dy = self.ask_slider_int("Translasi", "dy (atas/bawah, px)", -500, 500, 20)
            if dx is not None and dy is not None:
                self.push_undo()
                result = basic_ops.geom_translate(self.processed_image, dx, dy)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geom_rotation(self):
        if self.processed_image:
            angle = self.ask_slider_int("Rotasi", "Sudut rotasi (derajat)", -360, 360, 45)
            if angle is not None:
                self.push_undo()
                result = basic_ops.geom_rotate(self.processed_image, angle)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geom_zooming(self):
        if self.processed_image:
            scale = self.ask_slider_float("Zooming", "Skala zoom", 0.1, 5.0, 1.5)
            if scale is not None:
                self.push_undo()
                result = basic_ops.geom_zoom(self.processed_image, scale)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geom_flipping(self):
        if self.processed_image:
            mode = self.ask_option("Flipping", "Pilih mode flipping:", ["horizontal", "vertical"])
            if mode:
                self.push_undo()
                result = basic_ops.geom_flip(self.processed_image, mode)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def geom_cropping(self):
        if self.processed_image:
            w, h = self.processed_image.size
            left = self.ask_slider_int("Cropping", "Left (px)", 0, w-1, 10)
            upper = self.ask_slider_int("Cropping", "Upper (px)", 0, h-1, 10)
            right = self.ask_slider_int("Cropping", f"Right (px, max {w})", 1, w, w-10)
            lower = self.ask_slider_int("Cropping", f"Lower (px, max {h})", 1, h, h-10)
            if None not in (left, upper, right, lower):
                box = (left, upper, right, lower)
                self.push_undo()
                result = basic_ops.geom_crop(self.processed_image, box)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def thresholding_image(self):
        if self.processed_image:
            thresh = self.ask_slider_int("Thresholding", "Nilai threshold", 0, 255, 127)
            if thresh is not None:
                self.push_undo()
                result = basic_ops.thresholding(self.processed_image, thresh)
                self.processed_image = result
                self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def convolution_image(self):
        if self.processed_image:
            # Contoh kernel: blur
            import numpy as np
            kernel = np.ones((3,3))/9
            self.push_undo()
            result = basic_ops.convolution(self.processed_image, kernel)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def fourier_image(self):
        if self.processed_image:
            self.push_undo()
            result = basic_ops.fourier_transform(self.processed_image)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")

    def colouring_image(self, mode):
        if self.processed_image:
            self.push_undo()
            result = basic_ops.colouring(self.processed_image, mode)
            self.processed_image = result
            self.display_image(result)
        else:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu.")
    def ask_slider_int(self, title, label, minval, maxval, default):
        win = tk.Toplevel(self.root)
        win.title(title)
        tk.Label(win, text=label).pack(pady=5)
        val = tk.IntVar(value=default)
        slider = tk.Scale(win, from_=minval, to=maxval, orient=tk.HORIZONTAL, variable=val)
        slider.pack(padx=10, pady=10)
        result = {'value': None}
        def on_ok():
            result['value'] = val.get()
            win.destroy()
        tk.Button(win, text="OK", command=on_ok).pack(pady=5)
        win.grab_set()
        win.wait_window()
        return result['value']

    def ask_slider_float(self, title, label, minval, maxval, default):
        win = tk.Toplevel(self.root)
        win.title(title)
        tk.Label(win, text=label).pack(pady=5)
        val = tk.DoubleVar(value=default)
        slider = tk.Scale(win, from_=minval, to=maxval, orient=tk.HORIZONTAL, variable=val, resolution=0.01)
        slider.pack(padx=10, pady=10)
        result = {'value': None}
        def on_ok():
            result['value'] = val.get()
            win.destroy()
        tk.Button(win, text="OK", command=on_ok).pack(pady=5)
        win.grab_set()
        win.wait_window()
        return result['value']

    def ask_int(self, title, prompt, default=0):
        from tkinter.simpledialog import askinteger
        return askinteger(title, prompt, initialvalue=default)

    def ask_float(self, title, prompt, default=1.0):
        from tkinter.simpledialog import askfloat
        return askfloat(title, prompt, initialvalue=default)

    def ask_option(self, title, prompt, options):
        import tkinter.simpledialog as sd
        class OptionDialog(sd.Dialog):
            def body(self, master):
                tk.Label(master, text=prompt).pack()
                self.var = tk.StringVar(value=options[0])
                for opt in options:
                    tk.Radiobutton(master, text=opt, variable=self.var, value=opt).pack(anchor='w')
                return None
            def apply(self):
                self.result = self.var.get()
        d = OptionDialog(self.root, title)
        return d.result



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
