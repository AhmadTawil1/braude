import customtkinter as ctk
from course import Course
from scheduler import scheduler

class GUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.app = ctk.CTk()
        self.app.title("Brauler - בניית מערכת שעות")
        self.app.geometry("1200x800")
        
        self.courses = []
        self.schedule_labels = {}  # Store grid labels for updating
        self.course_colors = [
            "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6",
            "#ec4899", "#14b8a6", "#f97316", "#06b6d4", "#84cc16"
        ]
        
        self.layout()
        self.app.mainloop()

    def layout(self):
        # Main container
        self.main_frame = ctk.CTkFrame(master=self.app)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        self.topic_label = ctk.CTkLabel(
            master=self.main_frame, 
            text="Brauler - בניית מערכת שעות", 
            font=('Narkisim', 40, 'bold')
        )
        self.topic_label.pack(pady=10)

        # Top section: Course input and list
        self.top_section = ctk.CTkFrame(master=self.main_frame)
        self.top_section.pack(pady=10, padx=10, fill="x")

        # Course input
        self.input_frame = ctk.CTkFrame(master=self.top_section)
        self.input_frame.pack(side="right", padx=10, pady=10)

        self.input_label = ctk.CTkLabel(
            master=self.input_frame, 
            text="הוספת קורס", 
            font=('Narkisim', 20)
        )
        self.input_label.pack(pady=5)

        self.add_course_entry = ctk.CTkEntry(
            master=self.input_frame, 
            placeholder_text="מספר קורס",
            width=150
        )
        self.add_course_entry.pack(pady=5)
        self.add_course_entry.bind("<Return>", lambda e: self.add_course())

        self.add_course_button = ctk.CTkButton(
            master=self.input_frame, 
            text="הוסף", 
            font=("Narkisim", 16), 
            command=self.add_course
        )
        self.add_course_button.pack(pady=5)

        # Error message label
        self.error_label = ctk.CTkLabel(
            master=self.input_frame,
            text="",
            font=('Narkisim', 12),
            text_color="red"
        )
        self.error_label.pack(pady=5)

        # Course list
        self.course_list_frame = ctk.CTkFrame(master=self.top_section)
        self.course_list_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.course_list_label = ctk.CTkLabel(
            master=self.course_list_frame, 
            text="קורסים שנוספו", 
            font=('Narkisim', 20)
        )
        self.course_list_label.pack(pady=5)

        self.course_list_container = ctk.CTkScrollableFrame(
            master=self.course_list_frame,
            height=150
        )
        self.course_list_container.pack(pady=5, padx=5, fill="both", expand=True)

        # Schedule grid
        self.schedule_frame = ctk.CTkFrame(master=self.main_frame)
        self.schedule_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.schedule_title = ctk.CTkLabel(
            master=self.schedule_frame, 
            text="מערכת שעות", 
            font=('Narkisim', 24, 'bold')
        )
        self.schedule_title.pack(pady=10)

        self.create_schedule_grid()

    def create_schedule_grid(self):
        """Create the weekly schedule grid"""
        self.grid_frame = ctk.CTkFrame(master=self.schedule_frame)
        self.grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Days of the week (Sunday to Friday in Hebrew)
        days = ['', 'א\'', 'ב\'', 'ג\'', 'ד\'', 'ה\'', 'ו\'']
        
        # Time slots
        time_slots = [
            "08:30", "09:30", "10:30", "11:30", "12:50", 
            "13:50", "14:50", "15:50", "16:50", "17:50", 
            "18:50", "19:50", "20:50", "21:50"
        ]

        # Create header row (days)
        for col, day in enumerate(days):
            label = ctk.CTkLabel(
                master=self.grid_frame,
                text=day,
                font=('Narkisim', 16, 'bold'),
                width=100
            )
            label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

        # Create time slots and grid cells
        for row, time in enumerate(time_slots, start=1):
            # Time label
            time_label = ctk.CTkLabel(
                master=self.grid_frame,
                text=time,
                font=('Narkisim', 14),
                width=80
            )
            time_label.grid(row=row, column=0, padx=2, pady=2, sticky="nsew")

            # Day cells
            for col in range(1, 7):
                cell_label = ctk.CTkLabel(
                    master=self.grid_frame,
                    text="",
                    font=('Narkisim', 11),
                    fg_color="#2b2b2b",
                    corner_radius=5,
                    width=100,
                    height=40
                )
                cell_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                
                # Store reference for updating
                self.schedule_labels[(time, col-1)] = cell_label

        # Configure grid weights for responsiveness
        for i in range(len(time_slots) + 1):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def add_course(self):
        """Add a course and regenerate schedule"""
        course_id = self.add_course_entry.get().strip()
        
        # Clear error message
        self.error_label.configure(text="")
        
        if not course_id:
            self.show_error("אנא הזן מספר קורס")
            return
        
        try:
            course_id_int = int(course_id)
        except ValueError:
            self.show_error("מספר קורס לא תקין")
            return

        try:
            # Show loading state
            self.add_course_button.configure(state="disabled", text="טוען...")
            self.app.update()
            
            course = Course(course_id_int)
            
            # Check if course already added
            if any(c.id == course.id for c in self.courses):
                self.show_error("קורס זה כבר נוסף")
                self.add_course_button.configure(state="normal", text="הוסף")
                return
            
            self.courses.append(course)
            self.add_course_to_list(course)
            self.add_course_entry.delete(0, 'end')
            self.update_schedule_display()
            
        except ValueError as e:
            self.show_error(f"שגיאה: {str(e)}")
        except Exception as e:
            self.show_error(f"שגיאה בטעינת קורס: {str(e)}")
        finally:
            self.add_course_button.configure(state="normal", text="הוסף")

    def add_course_to_list(self, course):
        """Add course to the displayed list"""
        course_index = len(self.courses) - 1
        color = self.course_colors[course_index % len(self.course_colors)]
        
        course_frame = ctk.CTkFrame(
            master=self.course_list_container,
            fg_color=color,
            corner_radius=8
        )
        course_frame.pack(pady=5, padx=5, fill="x")

        course_text = f"{course.id} - {course.name}"
        course_label = ctk.CTkLabel(
            master=course_frame,
            text=course_text,
            font=('Narkisim', 14),
            anchor="e"
        )
        course_label.pack(side="right", padx=10, pady=5)

        remove_button = ctk.CTkButton(
            master=course_frame,
            text="הסר",
            font=("Narkisim", 12),
            width=60,
            command=lambda: self.remove_course(course, course_frame)
        )
        remove_button.pack(side="left", padx=10, pady=5)

    def remove_course(self, course, frame):
        """Remove course and regenerate schedule"""
        self.courses.remove(course)
        frame.destroy()
        self.update_schedule_display()

    def update_schedule_display(self):
        """Update the schedule grid based on current courses"""
        # Clear all cells
        self.clear_schedule_grid()
        
        if not self.courses:
            return
        
        # Generate schedule
        schedule, latest = scheduler(self.courses)
        
        if not schedule:
            self.show_error("לא ניתן ליצור מערכת שעות עם הקורסים שנבחרו")
            return
        
        # Day mapping - using full day names as returned by parser
        days = {
            'יום ראשון': 0,    # Sunday
            'יום שני': 1,      # Monday  
            'יום שלישי': 2,    # Tuesday
            'יום רביעי': 3,    # Wednesday
            'יום חמישי': 4,    # Thursday
            'יום שישי': 5      # Friday
        }
        
        # Time to row mapping
        time_slots = {
            "08:30": 0, "09:30": 1, "10:30": 2, "11:30": 3,
            "12:20": 4, "12:50": 4, "13:50": 5, "14:50": 6,
            "15:50": 7, "16:50": 8, "17:50": 9, "18:50": 10,
            "19:50": 11, "20:50": 12, "21:50": 13
        }
        
        time_list = [
            "08:30", "09:30", "10:30", "11:30", "12:50",
            "13:50", "14:50", "15:50", "16:50", "17:50",
            "18:50", "19:50", "20:50", "21:50"
        ]
        
        # Populate schedule
        for course_idx, (course, lessons) in enumerate(schedule):
            color = self.course_colors[course_idx % len(self.course_colors)]
            
            for lesson in lessons:
                day_index = days.get(lesson.day)
                if day_index is None:
                    continue
                
                start_index = time_slots.get(lesson.start)
                finish_index = time_slots.get(lesson.finish)
                
                if start_index is None or finish_index is None:
                    continue
                
                # Fill cells for lesson duration
                for time_idx in range(start_index, finish_index):
                    time_slot = time_list[time_idx]
                    key = (time_slot, day_index)
                    
                    if key in self.schedule_labels:
                        # Abbreviate course name if too long
                        course_name = course.name
                        if len(course_name) > 15:
                            course_name = course_name[:12] + "..."
                        
                        lesson_info = f"{course_name}\n{lesson.type}"
                        self.schedule_labels[key].configure(
                            text=lesson_info,
                            fg_color=color
                        )

    def clear_schedule_grid(self):
        """Clear all schedule cells"""
        for label in self.schedule_labels.values():
            label.configure(text="", fg_color="#2b2b2b")

    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
        self.add_course_entry.configure(border_color="red")
        self.add_course_entry.after(2000, lambda: self.add_course_entry.configure(border_color="gray"))
        self.error_label.after(3000, lambda: self.error_label.configure(text=""))
