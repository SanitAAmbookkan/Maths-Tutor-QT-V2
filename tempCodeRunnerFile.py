    def load_section(self, name):
        print(f"[INFO] Loading section: {name}")

        if not hasattr(self, 'section_pages'):
            self.section_pages = {}

        if name not in self.section_pages:
            # Always call load_pages to load/reload based on current difficulty
            page = load_pages(name, self.back_to_main_menu, difficulty_index=self.current_difficulty, main_window=self)

            if hasattr(self, "current_theme"):
                page.setProperty("theme", self.current_theme)
                page.style().unpolish(page)
                page.style().polish(page)

            self.section_pages[name] = page
            self.stack.addWidget(page)

        self.stack.setCurrentWidget(self.section_pages[name])
        self.menu_widget.hide()
        self.main_footer.hide()
        self.section_footer.show()
        back_to_ops_btn = self.section_footer.findChild(QPushButton, "back_to_operations")
        if back_to_ops_btn:
            back_to_ops_btn.setVisible(name.lower() != "operations")
