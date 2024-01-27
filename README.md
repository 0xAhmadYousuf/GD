# GD
`For Those Who don't use GitClone`
![GD](https://github.com/0xAhmadYousuf/GD/assets/139548576/ff0d78ea-5804-45cc-9c57-f417a28c21e8)

*`Git Downloader is a user-friendly tool designed to simplify the process of downloading and extracting ZIP files from GitHub repositories. This standalone executable can be used on both Windows and Linux systems without requiring Python or additional dependencies.`*

## Features

- **Download ZIP files:** Easily download ZIP files from GitHub repositories.
- **Extract ZIP contents:** Extract the contents of downloaded ZIP files with just a click.
- **Cross-platform compatibility:** Works seamlessly on both Windows and Linux systems.
- **Simple graphical user interface:** Intuitive interface for effortless usage.

## How to Use

![image](https://github.com/0xAhmadYousuf/GD/assets/139548576/1ca378ac-3d86-480f-858f-771ee23d130c)
### Windows

1. Double-click the `Git_Downloader.exe` executable to launch the application.
2. Enter the GitHub URL of the repository you want to download in the provided field.
3. Click the "Download" button to initiate the download process.
4. Once the download is complete, you'll be prompted to extract the contents of the ZIP file.
5. Choose whether to extract the contents or not.
6. The extracted files will be saved in the same directory as the executable.

### Linux

1. Open a terminal and navigate to the directory containing the `Git_Downloader` executable.
2. Run the executable using the following command: `./Git_Downloader`
3. Follow steps 2-6 from the Windows instructions above to use the application.

## Requirements

- No additional requirements or dependencies are needed. The executable contains all necessary components for seamless operation.

## Installation

1. Download the Git Downloader executable for your operating system:
   - For Windows: `Git_Downloader.exe`
   - For Linux: `Git_Downloader`
2. Place the executable in a convenient location on your system.
3. Follow the usage instructions provided above to start using Git Downloader.












# Building from Source (For Editors)

If you're interested in contributing to or modifying the Git Downloader source code, follow these steps to build the executable from the source:

1. **Clone the Repository:**
   - Clone the Git Downloader repository to your local machine using the following command:
     ```
     git clone https://github.com/0xAhmadYousuf/GD.git
     ```

2. **Navigate to the Repository Directory:**
   - Change into the repository directory:
     ```
     cd GD
     ```

3. **Install Dependencies:**
   - Ensure you have [Nuitka](https://nuitka.net/) installed on your system.

4. **Compile the Python Script into an Executable:**
   - For Windows, use the following command:
     ```
     nuitka --mingw64 --standalone --show-progress --show-memory --output-dir=out --onefile --windows-icon-from-ico=a.ico git_downloader.py
     ```
     This command will generate the `Git_Downloader.exe` executable in the `out` directory.
   - For Linux, use the following command:
     ```
     nuitka --standalone --show-progress --show-memory --output-dir=out --onefile --linux-icon=icon.png git_downloader.py
     ```
     This command will generate the `Git_Downloader` executable in the `out` directory.

5. **Contribute or Modify:**
   - Open the `git_downloader.py` script using your preferred text editor or integrated development environment (IDE).
   - Make the necessary modifications or contributions to the source code.
   - Save your changes.

6. **Run the Updated Executable:**
   - After making modifications, you can run the updated executable locally for testing:
     - For Windows:
       ```
       ./out/Git_Downloader.exe
       ```
     - For Linux:
       ```
       ./out/Git_Downloader
       ```

7. **Create a Pull Request (Optional):**
   - If you've made valuable contributions and wish to share them with the project, consider creating a pull request.

8. **Share Feedback:**
   - Feel free to open issues or provide feedback on the [GitHub repository](https://github.com/0xAhmadYousuf/GD).

9. **Acknowledgment:**
   - Ensure that you adhere to the project's coding standards and guidelines. Provide clear commit messages and follow the contribution guidelines.
