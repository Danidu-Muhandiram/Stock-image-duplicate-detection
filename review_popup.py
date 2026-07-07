import customtkinter as ctk
from PIL import Image, ImageTk


class ReviewPopup:
    def __init__(self, suspicious_data):
        # Store the duplicate candidates passed in from the scanner.
        self.data = suspicious_data or []

        # Track the current pending image and the current published match.
        self.current_image_index = 0
        self.current_match_index = 0

        # Reserved for review state if the checkbox is used later.
        self.selected = {}

        # Use the dark CustomTkinter theme for the popup.
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Build the main popup window.
        self.root = ctk.CTk()
        self.root.geometry("1280x840")
        self.root.minsize(1100, 760)
        self.root.title("Duplicate Review")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        # Build the header, content area, and footer controls.
        self._build_header()
        self._build_content()
        self._build_footer()

        self.update_view()
        self.root.mainloop()

    def _build_header(self):
        # Header card with title, instructions, and live summary
        header_frame = ctk.CTkFrame(self.root, corner_radius=24)
        header_frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Duplicate Review",
            font=("Segoe UI", 28, "bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=24, pady=(20, 4))

        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Compare the pending image with the closest published match and decide whether it should stay in the duplicate queue.",
            font=("Segoe UI", 14),
            text_color=("gray75", "gray75"),
            wraplength=980,
            justify="left",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        summary_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        summary_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.review_count_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
        )
        self.review_count_label.grid(row=0, column=0, sticky="w")

        self.match_count_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
        )
        self.match_count_label.grid(row=0, column=1, sticky="w")

        self.similarity_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
        )
        self.similarity_label.grid(row=0, column=2, sticky="w")

    def _build_content(self):
        # Main split view that shows the published and pending images side by side.
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=24)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)
        self.content_frame.grid_columnconfigure((0, 1), weight=1, uniform="image_columns")
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.left_panel = self._build_image_panel(
            self.content_frame,
            row=0,
            column=0,
            title="Published image",
        )
        self.right_panel = self._build_image_panel(
            self.content_frame,
            row=0,
            column=1,
            title="Pending image",
        )

    def _build_image_panel(self, parent, row, column, title):
        # Each panel uses the same structure: title, image, and caption.
        panel = ctk.CTkFrame(parent, corner_radius=20)
        panel.grid(row=row, column=column, sticky="nsew", padx=18, pady=18)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            panel,
            text=title,
            font=("Segoe UI", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 10))

        image_label = ctk.CTkLabel(
            panel,
            text="Loading image...",
            font=("Segoe UI", 14),
            justify="center",
        )
        image_label.grid(row=1, column=0, sticky="nsew", padx=18, pady=8)

        caption_label = ctk.CTkLabel(
            panel,
            text="",
            font=("Segoe UI", 12),
            text_color=("gray75", "gray75"),
            wraplength=500,
            justify="left",
        )
        caption_label.grid(row=2, column=0, sticky="w", padx=18, pady=(4, 16))

        if column == 0:
            self.left_image_label = image_label
            self.left_caption_label = caption_label
        else:
            self.right_image_label = image_label
            self.right_caption_label = caption_label

        return panel

    def _build_footer(self):
        # Footer holds the review checkbox and the image/match navigation buttons.
        footer_frame = ctk.CTkFrame(self.root, corner_radius=24)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=(12, 24))
        footer_frame.grid_columnconfigure(1, weight=1)

        # Review decision control.
        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(
            footer_frame,
            text="Mark as duplicate",
            variable=self.checkbox_var,
        )
        self.checkbox.grid(row=0, column=0, sticky="w", padx=20, pady=18)

        # Group the navigation controls together on the right.
        nav_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="e", padx=20, pady=18)

        ctk.CTkButton(
            nav_frame,
            text="Previous image",
            command=self.previous_image,
            width=140,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            nav_frame,
            text="Next image",
            command=self.next_image,
            width=120,
        ).pack(side="left", padx=(0, 18))

        ctk.CTkButton(
            nav_frame,
            text="Previous match",
            command=self.previous_match,
            width=150,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            nav_frame,
            text="Next match",
            command=self.next_match,
            width=120,
        ).pack(side="left", padx=(0, 18))

        ctk.CTkButton(
            nav_frame,
            text="Close",
            command=self.root.destroy,
            width=100,
        ).pack(side="left")

    def load_image(self, path):
        # Load and scale an image for display inside the popup.
        try:
            image = Image.open(path)
            image.thumbnail((520, 520))
            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def update_view(self):
        # Update the popup for the current pending image and match.
        if not self.data:
            self.review_count_label.configure(text="No duplicate candidates found")
            self.match_count_label.configure(text="")
            self.similarity_label.configure(text="")
            self.left_image_label.configure(text="No published image", image=None)
            self.right_image_label.configure(text="No pending image", image=None)
            self.left_caption_label.configure(text="")
            self.right_caption_label.configure(text="")
            return

        current_item = self.data[self.current_image_index]
        current_match = current_item["matches"][self.current_match_index]

        left_image = self.load_image(current_match["published_path"])
        right_image = self.load_image(current_item["pending_path"])

        self._set_image(
            self.left_image_label,
            left_image,
            current_match["published_name"],
        )
        self._set_image(
            self.right_image_label,
            right_image,
            current_item["pending_name"],
        )

        self.review_count_label.configure(
            text=f"Pending image {self.current_image_index + 1} of {len(self.data)}"
        )
        self.match_count_label.configure(
            text=f"Match {self.current_match_index + 1} of {len(current_item['matches'])}"
        )
        self.similarity_label.configure(
            text=f"Similarity {current_match['similarity']}%"
        )

        self.left_caption_label.configure(
            text=f"{current_match['published_name']}\n{current_match['published_path']}"
        )
        self.right_caption_label.configure(
            text=f"{current_item['pending_name']}\n{current_item['pending_path']}"
        )

    def _set_image(self, label, image, fallback_text):
        # Keep a strong reference to the rendered image so Tkinter does not drop.
        if image is None:
            label.configure(image=None, text=f"Unable to load\n{fallback_text}")
            label.image = None
            return

        label.configure(image=image, text="")
        label.image = image

    def next_image(self):
        # Move to the next pending image candidate.
        if self.current_image_index < len(self.data) - 1:
            self.current_image_index += 1
            self.current_match_index = 0
            self.update_view()

    def previous_image(self):
        # Move to the previous pending image candidate.
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.current_match_index = 0
            self.update_view()

    def next_match(self):
        # Move to the next published match for the current pending image.
        current_item = self.data[self.current_image_index]
        if self.current_match_index < len(current_item["matches"]) - 1:
            self.current_match_index += 1
            self.update_view()

    def previous_match(self):
        # Move to the previous published match for the current pending image.
        if self.current_match_index > 0:
            self.current_match_index -= 1
            self.update_view()