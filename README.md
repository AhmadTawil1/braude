# Tanzim Braude (تنظيم برعودة) - Course Scheduler

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Automatically generate optimal course schedules for Braude College students by entering course IDs.

## Features

- 🗓️ **Weekly Schedule View** - Visual calendar grid showing your classes
- 🎨 **Color-Coded Courses** - Each course gets a unique color
- ⚡ **Auto-Generation** - Schedule updates in real-time as you add courses
- 🔍 **Conflict Detection** - Automatically avoids overlapping classes
- 🌐 **No Authentication Required** - Fetches course data directly from Braude's public pages

## Screenshots

![Tanzim Braude Interface](screenshots/main_interface.png)

## Installation

### Option 1: Download Executable (Easiest)

1. Download `TanzimBraude.exe` from [Releases](https://github.com/yourusername/braude-scheduler/releases)
2. Double-click to run
3. No installation needed!

### Option 2: Run from Source

**Requirements:**
- Python 3.8 or higher
- Windows OS

**Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/braude-scheduler.git
   cd braude-scheduler
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r brauler/requirements.txt
   ```

4. **Run the application:**
   ```bash
   python brauler/main.py
   ```

## Usage

1. **Launch the application**
2. **Enter a course ID** (e.g., `61954` for Deep Generative Learning)
3. **Click "הוסף" (Add)**
4. **View your schedule** in the weekly grid
5. **Add more courses** - the schedule updates automatically
6. **Remove courses** by clicking "הסר" (Remove) next to the course

### Finding Course IDs

Course IDs can be found on the Braude College course catalog:
- Visit: https://info.braude.ac.il/yedion/fireflyweb.aspx?prgname=Enter_Search
- Search for your course
- The course ID is the number in the URL

## How It Works

1. **Fetches course data** from Braude's public course pages
2. **Parses lecture/lab/practice times** for each course
3. **Generates all possible combinations** of non-overlapping lessons
4. **Selects the optimal schedule** with maximum course coverage
5. **Displays the schedule** in a visual weekly grid

## Technical Details

- **Language:** Python 3.8+
- **GUI Framework:** CustomTkinter
- **Web Scraping:** BeautifulSoup4, Requests
- **Algorithm:** Constraint satisfaction with backtracking

## Project Structure

```
braude-scheduler/
├── brauler/
│   ├── main.py           # Entry point
│   ├── gui.py            # GUI implementation
│   ├── scheduler.py      # Scheduling algorithm
│   ├── course.py         # Course data model
│   ├── data_parser.py    # Web scraping logic
│   └── requirements.txt  # Dependencies
└── README.md
```

## Known Limitations

- Only supports courses from Braude College
- Requires internet connection to fetch course data
- Currently optimized for Windows (GUI may look different on Mac/Linux)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Braude College for providing public course data
- CustomTkinter for the modern GUI framework

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for Braude College students**
