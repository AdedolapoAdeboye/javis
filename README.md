# Javis: Your Ultimate To-Do Application

![Javis Logo](path/to/logo.png)

Javis is a powerful and feature-rich to-do application designed to help you manage your tasks efficiently across multiple platforms including Android, iOS, Windows, MacOS, and Debian. With a user-friendly interface and advanced features like theme customization, security options, cloud synchronization, and task management, Javis is your go-to productivity tool.

## Features

- **Multi-platform Support**: Available on Android, iOS, Windows, MacOS, and Debian.
- **Theme Customization**: Choose from various themes like Light Mode, Dark Mode, AMOLED Dark Mode, Blue on White, Pink on White, Yellow on Black, and Blue on Black.
- **Security Options**: Toggle between Face ID (for supported devices), PIN code, and no security lock.
- **Task Management**: Add, modify, delete, and mark tasks as done with an intuitive interface.
- **Cloud Synchronization**: Save your tasks to the cloud using Firebase for seamless access across devices.
- **Export as PDF**: Easily export your to-do list as a PDF file for sharing or printing.

## Screenshots

![Javis Light Mode](path/to/light-mode-screenshot.png)
![Javis Dark Mode](path/to/dark-mode-screenshot.png)

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Setting Up

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/javis.git
    cd javis
    ```

2. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up Firebase**

    - Download your `GoogleService-Info.json` from Firebase console.
    - Place it in the project directory and update the path in the code if necessary.

4. **Run the Application**

    ```sh
    python main.py
    ```

## Usage

- **Add Tasks**: Use the input field to type your task and click "Add Task".
- **Modify Tasks**: Double-click a task to open the context menu and select "Modify".
- **Delete Tasks**: Double-click a task to open the context menu and select "Delete".
- **Mark Tasks as Done**: Double-click a task to open the context menu and select "Mark as Done".
- **Change Theme**: Use the theme spinner to select your preferred theme.
- **Set Security**: Use the security spinner to set your preferred security option (Face ID, PIN, or None).
- **Save to Cloud**: Click "Save to Cloud" to synchronize your tasks with Firebase.
- **Export as PDF**: Click "Export as PDF" to save your tasks as a PDF file.

## Contributing

We welcome contributions to enhance Javis. Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Firebase](https://firebase.google.com/)
- [ReportLab](https://www.reportlab.com/)
- [Tkinter](https://wiki.python.org/moin/TkInter)
- Icons by [Apple Design Resources](https://developer.apple.com/design/resources/)

---

Feel free to reach out if you have any questions or need support!

Happy Tasking with Javis! 🚀
