 def create_main_footer_buttons(self):
        return create_footer_buttons(
            ["Upload", "Help", "About", "Settings"],
            callbacks={
                "Upload": self.handle_upload,
                }
        )
    