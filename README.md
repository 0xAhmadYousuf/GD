# GD
For Those Who don't use GitClone
![image](https://github.com/0xAhmadYousuf/GD/assets/139548576/4516a55c-8ffe-4235-8ebd-82f6ecaebad2)
Sure, here's a more detailed README for the Git Downloader executable:



# Git Downloader

Git Downloader is a user-friendly tool designed to simplify the process of downloading and extracting ZIP files from GitHub repositories. This standalone executable can be used on both Windows and Linux systems without requiring Python or additional dependencies.

## Features

- **Download ZIP files:** Easily download ZIP files from GitHub repositories.
- **Extract ZIP contents:** Extract the contents of downloaded ZIP files with just a click.
- **Cross-platform compatibility:** Works seamlessly on both Windows and Linux systems.
- **Simple graphical user interface:** Intuitive interface for effortless usage.

## How to Use

### Windows

1. Double-click the `Git_Downloader.exe` executable to launch the application.
2. Enter the GitHub URL of the repository you want to download in the provided field.
3. Click the "Download" button to initiate the download process.
4. Once the download is complete, you'll be prompted to extract the contents of the ZIP file.
5. Choose whether to extract the contents or not.
6. The extracted files will be saved in the same directory as the executable.

### Linux

1. Open a terminal and navigate to the directory containing the `Git_Downloader` executable.
2. Run the executable using the following command:

#  ./Git_Downloader

3. Follow steps 2-6 from the Windows instructions above to use the application.

## Requirements

- No additional requirements or dependencies are needed. The executable contains all necessary components for seamless operation.

## Installation

1. Download the Git Downloader executable for your operating system:
   - For Windows: `Git_Downloader.exe`
   - For Linux: `Git_Downloader`
2. Place the executable in a convenient location on your system.
3. Follow the usage instructions provided above to start using Git Downloader.

## Building from Source

If you wish to build the executable from source, follow these steps:

1. Clone the Git Downloader repository to your local machine.
2. Navigate to the repository directory.
3. Use Nuitka to compile the Python script into an executable:
   ```
   nuitka --mingw64 --standalone --show-progress --show-memory --output-dir=out --onefile --windows-icon-from-ico=a.ico git_downloader.py
   ```
   This command will generate the `Git_Downloader.exe` executable for Windows.
4. For Linux, use the following command:
   ```
   nuitka --standalone --show-progress --show-memory --output-dir=out --onefile git_downloader.py
   ```
   This command will generate the `Git_Downloader` executable for Linux.

## Disclaimer

This tool is provided for educational and personal use only. Use it responsibly and respect the terms and conditions of GitHub repositories.
```

This README provides detailed instructions for both Windows and Linux users, including how to use the application, requirements, installation steps, and building from source.
