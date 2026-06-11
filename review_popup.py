# CUSTOMTKINTER

# custom modern tkinter UI
import customtkinter as ctk

# PIL (IMAGE HANDLING)
# Used to open image files
from PIL import Image
# Converts PIL image into Tkinter image
# so it can be shown inside labels
from PIL import ImageTk

# REVIEW POPUP CLASS
class ReviewPopup:

    # CONSTRUCTOR (RUNS AUTOMATICALLY)
    def __init__(
        self,
        suspicious_data
    ):

        # Save suspicious image data
        self.data = suspicious_data

        # Current pending and match image indexes
        self.current_image_index = 0
        self.current_match_index = 0

        # Store selected duplicates
        self.selected = {}

         # APP THEME - dark mode
        ctk.set_appearance_mode(
            "dark"
        )

        # MAIN WINDOW
        self.root = ctk.CTk()

        self.root.geometry(
            "1200x700"
        )

        self.root.title(
            "Duplicate Review"
        )

        # HEADER
        self.header_label = (
            ctk.CTkLabel(
                self.root,
                text="",
                font=(
                    "Arial",
                    22,
                    "bold"
                )
            )
        )

        self.header_label.pack(
            pady=10
        )

        # IMAGE FRAME
        self.image_frame = (
            ctk.CTkFrame(
                self.root
            )
        )

        self.image_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.left_label = (
            ctk.CTkLabel(
                self.image_frame,
                text=""
            )
        )

        self.left_label.pack(
            side="left",
            expand=True,
            padx=20
        )

        self.right_label = (
            ctk.CTkLabel(
                self.image_frame,
                text=""
            )
        )

        self.right_label.pack(
            side="right",
            expand=True,
            padx=20
        )

        # --------------------
        # INFO
        # --------------------
        self.info_label = (
            ctk.CTkLabel(
                self.root,
                text="",
                font=(
                    "Arial",
                    18
                )
            )
        )

        self.info_label.pack()

        # --------------------
        # CHECKBOX
        # --------------------
        self.checkbox_var = (
            ctk.BooleanVar()
        )

        self.checkbox = (
            ctk.CTkCheckBox(
                self.root,
                text=
                "Mark as duplicate",
                variable=
                self.checkbox_var
            )
        )

        self.checkbox.pack(
            pady=10
        )

        # --------------------
        # NAVIGATION
        # --------------------
        nav_frame = (
            ctk.CTkFrame(
                self.root
            )
        )

        nav_frame.pack(
            pady=10
        )

        ctk.CTkButton(
            nav_frame,
            text=
            "← Previous Image",
            command=
            self.previous_image
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            nav_frame,
            text=
            "Next Image →",
            command=
            self.next_image
        ).pack(
            side="left",
            padx=10
        )

        # --------------------
        # MATCH NAVIGATION
        # --------------------
        match_frame = (
            ctk.CTkFrame(
                self.root
            )
        )

        match_frame.pack(
            pady=10
        )

        ctk.CTkButton(
            match_frame,
            text=
            "← Previous Match",
            command=
            self.previous_match
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            match_frame,
            text=
            "Next Match →",
            command=
            self.next_match
        ).pack(
            side="left",
            padx=10
        )

        self.update_view()

        self.root.mainloop()

    # --------------------
    # LOAD IMAGES
    # --------------------
    def load_image(
        self,
        path
    ):

        image = Image.open(
            path
        )

        image.thumbnail(
            (450, 450)
        )

        return ImageTk.PhotoImage(
            image
        )

    # --------------------
    # UPDATE UI
    # --------------------
    def update_view(self):

        current_item = (
            self.data[
                self.current_image_index
            ]
        )

        current_match = (
            current_item[
                "matches"
            ][
                self.current_match_index
            ]
        )

        left_img = (
            self.load_image(
                current_match[
                    "published_path"
                ]
            )
        )

        right_img = (
            self.load_image(
                current_item[
                    "pending_path"
                ]
            )
        )

        self.left_label.configure(
            image=left_img
        )

        self.left_label.image = (
            left_img
        )

        self.right_label.configure(
            image=right_img
        )

        self.right_label.image = (
            right_img
        )

        self.header_label.configure(

            text=
            f"Image "
            f"{self.current_image_index+1}"
            f"/"
            f"{len(self.data)}"
            f" | Match "
            f"{self.current_match_index+1}"
            f"/"
            f"{len(current_item['matches'])}"
        )

        self.info_label.configure(

            text=
            f"{current_match['published_name']}"
            f" | "
            f"Similarity:"
            f" {current_match['similarity']}%"
        )

    # --------------------
    # IMAGE NAVIGATION
    # --------------------
    def next_image(self):

        if (
            self.current_image_index
            <
            len(self.data)-1
        ):

            self.current_image_index += 1

            self.current_match_index = 0

            self.update_view()

    def previous_image(self):

        if (
            self.current_image_index
            > 0
        ):

            self.current_image_index -= 1

            self.current_match_index = 0

            self.update_view()

    # --------------------
    # MATCH NAVIGATION
    # --------------------
    def next_match(self):

        current_item = (
            self.data[
                self.current_image_index
            ]
        )

        if (
            self.current_match_index
            <
            len(
                current_item[
                    "matches"
                ]
            ) - 1
        ):

            self.current_match_index += 1

            self.update_view()

    def previous_match(self):

        if (
            self.current_match_index
            > 0
        ):

            self.current_match_index -= 1

            self.update_view()