import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageOps


class OpacityPhotoApp:
    def __init__(self, root):
        """PhotoApp 초기화: GUI 요소와 기본 설정을 초기화"""
        self.root = root
        self.root.title("Opacity Photo App")  # 창 제목 설정
        
        # 초기 크기 설정
        self.layer_max_count = 10 # 최대 레이어 수
        self.actual_width = 500  # 저장할 이미지의 실제 가로 크기
        self.actual_height = 500  # 저장할 이미지의 실제 세로 크기
        self.display_width = 500  # 화면에 표시할 가로 크기 (고정된 크기)
        self.display_height = 500  # 화면에 표시할 세로 크기 (고정된 크기)

        # 표시용 크기 초기화 (실제 크기를 화면 크기에 맞춰 조정)
        self.scaled_width = self.display_width
        self.scaled_height = self.display_height

        self.layers = []  # 레이어 정보를 담을 리스트
        self.current_layer = None  # 현재 선택된 레이어 인덱스

        # 사진 액자 영역 (이미지 표시용 캔버스)
        self.canvas = tk.Canvas(root, width=self.display_width, height=self.display_height, bg="white")
        self.canvas.pack(pady=10)

        # 액자 크기 조정 섹션
        size_frame = tk.Frame(root)
        size_frame.pack(pady=10)

        tk.Label(size_frame, text="Width:").grid(row=0, column=0, padx=5)
        self.width_entry = tk.Entry(size_frame, width=5)  # 가로 크기 입력 필드
        self.width_entry.insert(0, str(self.actual_width))  # 초기값 설정
        self.width_entry.grid(row=0, column=1, padx=5)

        tk.Label(size_frame, text="Height:").grid(row=0, column=2, padx=5)
        self.height_entry = tk.Entry(size_frame, width=5)  # 세로 크기 입력 필드
        self.height_entry.insert(0, str(self.actual_height))  # 초기값 설정
        self.height_entry.grid(row=0, column=3, padx=5)

        # 크기 조정 버튼
        tk.Button(size_frame, text="Resize Frame", command=self.resize_frame).grid(row=0, column=4, padx=5)

        # 버튼 섹션
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Layer", command=self.add_layer).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove Layer", command=self.remove_layer).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Rename Layer", command=self.rename_layer).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Save Composite", command=self.save_composite).grid(row=0, column=3, padx=5)

        # 레이어 리스트
        tk.Label(root, text="Layers:").pack()
        self.layer_listbox = tk.Listbox(root, height=5)  # 레이어 이름을 표시할 리스트박스
        self.layer_listbox.pack(pady=10)
        self.layer_listbox.bind("<<ListboxSelect>>", self.select_layer)  # 레이어 선택 이벤트

        # 투명도 조정 스크롤바
        self.opacity_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Opacity (%)", command=self.update_opacity)
        self.opacity_scale.set(100)  # 초기값을 100으로 설정
        self.opacity_scale.pack(pady=10)

    def resize_frame(self):
        """실제 이미지 크기를 변경하고 화면 표시 크기는 비율에 맞춰 유지"""
        try:
            # 입력된 가로와 세로 크기를 저장용 크기로 설정
            self.actual_width = int(self.width_entry.get())
            self.actual_height = int(self.height_entry.get())

            # 비율 계산: 화면 크기(display)에 맞게 조정
            scale_ratio = min(self.display_width / self.actual_width, self.display_height / self.actual_height)
            self.scaled_width = int(self.actual_width * scale_ratio)
            self.scaled_height = int(self.actual_height * scale_ratio)

            # 캔버스 크기 업데이트
            self.canvas.config(width=self.scaled_width, height=self.scaled_height)

            # 모든 레이어의 이미지를 새로운 표시 크기에 맞춰 조정
            for layer in self.layers:
                layer["scaled_image"] = ImageOps.fit(layer["image"], (self.scaled_width, self.scaled_height), Image.Resampling.LANCZOS)
            self.update_canvas()
        except ValueError:
            tk.messagebox.showerror("Error", "Width and height must be integers.")  # 입력값 오류 처리

    def add_layer(self):
        """새 레이어를 추가하고 레이어 리스트 및 캔버스를 업데이트"""
        if len(self.layers) < self.layer_max_count:  # 최대 10개의 레이어 허용(더 변경하고 싶으면 이걸 바꿔)
            filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if filepath:
                # 새 이미지를 불러오고 크기를 저장용 크기에 맞게 조정
                image = Image.open(filepath)
                image = ImageOps.fit(image, (self.actual_width, self.actual_height), Image.Resampling.LANCZOS)

                # 표시용 크기로 이미지 조정
                scale_ratio = min(self.display_width / self.actual_width, self.display_height / self.actual_height)
                scaled_image = ImageOps.fit(image, (int(self.actual_width * scale_ratio), int(self.actual_height * scale_ratio)), Image.Resampling.LANCZOS)

                # 레이어 정보 저장
                layer_name = f"Layer {len(self.layers) + 1}"
                self.layers.append({"image": image, "scaled_image": scaled_image, "opacity": 100, "name": layer_name})
                self.layer_listbox.insert(tk.END, layer_name)  # 리스트박스에 레이어 추가
                self.current_layer = len(self.layers) - 1  # 새로 추가된 레이어 선택
                self.layer_listbox.select_clear(0, tk.END)
                self.layer_listbox.select_set(self.current_layer)
                self.layer_listbox.activate(self.current_layer)
                self.opacity_scale.set(100)  # 투명도 초기값 설정
                self.update_canvas()
        else:
            tk.messagebox.showerror("Error", f"You can only add up to {self.layer_max_count} layers.")  # 최대 레이어 초과 오류 처리

    def remove_layer(self):
        """선택한 레이어를 제거하고 리스트와 캔버스를 업데이트"""
        if self.current_layer is not None:
            del self.layers[self.current_layer]  # 레이어 삭제
            self.layer_listbox.delete(self.current_layer)  # 리스트박스 항목 삭제
            self.current_layer = len(self.layers) - 1 if self.layers else None  # 현재 레이어 인덱스 업데이트
            self.update_canvas()

    def rename_layer(self):
        """선택한 레이어의 이름 변경"""
        if self.current_layer is not None:
            new_name = simpledialog.askstring("Rename Layer", "Enter new name:")
            if new_name:
                self.layers[self.current_layer]["name"] = new_name  # 내부 데이터 변경
                self.layer_listbox.delete(self.current_layer)
                self.layer_listbox.insert(self.current_layer, new_name)  # 리스트박스 업데이트
                self.layer_listbox.select_set(self.current_layer)

    def select_layer(self, event):
        """레이어 리스트에서 선택한 레이어를 현재 레이어로 설정"""
        selection = self.layer_listbox.curselection()
        if selection:
            self.current_layer = selection[0]
            self.opacity_scale.set(self.layers[self.current_layer]["opacity"])

    def update_opacity(self, value):
        """선택한 레이어의 투명도를 업데이트"""
        if self.current_layer is not None:
            self.layers[self.current_layer]["opacity"] = int(value)
            self.update_canvas()

    def update_canvas(self):
        """캔버스에 합성된 이미지를 업데이트"""
        if not self.layers:
            self.canvas.delete("all")  # 레이어가 없으면 캔버스 초기화
            return

        # 투명도가 적용된 레이어 합성
        composite = Image.new("RGBA", (self.scaled_width, self.scaled_height))
        for layer in self.layers:
            img = layer["scaled_image"].convert("RGBA")
            alpha = int(255 * (layer["opacity"] / 100))
            img.putalpha(alpha)
            composite = Image.alpha_composite(composite, img)

        # 합성 이미지를 캔버스에 표시
        self.tk_image = ImageTk.PhotoImage(composite)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def save_composite(self):
        """합성 이미지를 실제 크기로 저장"""
        if not self.layers:
            tk.messagebox.showerror("Error", "No layers to save.")
            return
    
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",  # 기본 파일 확장자
            filetypes=[("PNG Files", "*.png")],  # 파일 형식 필터
            initialfile="image"  # 기본 파일 이름
        )

        if filepath:
            # 빈 캔버스 생성 (실제 크기)
            composite = Image.new("RGBA", (self.actual_width, self.actual_height))
            for layer in self.layers:
                # 레이어 이미지를 실제 크기로 강제 조정
                img = layer["image"].convert("RGBA")
                if img.size != (self.actual_width, self.actual_height):
                    img = img.resize((self.actual_width, self.actual_height), Image.Resampling.LANCZOS)
    
                # 투명도 적용 후 합성
                alpha = int(255 * (layer["opacity"] / 100))
                img.putalpha(alpha)
                composite = Image.alpha_composite(composite, img)
    
            # 최종 합성 이미지 저장
            composite.save(filepath)
            tk.messagebox.showinfo("Saved", f"Image saved to {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OpacityPhotoApp(root)
    root.mainloop()
