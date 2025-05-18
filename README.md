# Earth View Wallpaper Changer

A simple application that sets beautiful satellite images from Google Earth as your desktop wallpaper.

![Earth View Example](https://www.gstatic.com/prettyearth/assets/full/1003.jpg)

## Features

- System tray indicator for easy access
- One-click wallpaper changing
- Beautiful satellite imagery from Google Earth
- Compatible with Ubuntu and other GNOME-based Linux distributions
- Works with Ubuntu 20.04, 22.04, and newer versions

## Installation

### Prerequisites

```bash
# Install required system dependencies
sudo apt update
sudo apt install -y python3-pip python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 gir1.2-notify-0.7 libcairo2-dev libgirepository1.0-dev

# Install Python dependencies
pip3 install -r requirements.txt
```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/earthview.git
   cd earthview
   ```

2. Ensure the wallpaper changer script is executable:
   ```bash
   chmod +x wallpaper-changer/indicator.py
   ```

3. (Optional) To run the application at startup:
   - Open "Startup Applications" (gnome-session-properties)
   - Click "Add"
   - Name: Earth View Wallpaper Changer
   - Command: `/full/path/to/earthview/wallpaper-changer/indicator.py`
   - Comment: Changes desktop wallpaper to Google Earth images

## Usage

### Running the Application

```bash
cd /path/to/earthview
./wallpaper-changer/indicator.py
```

### Using the Application

1. Look for the Earth View icon in your system tray (top-right corner of your screen)
2. Click on the icon to open the menu
3. Select "Change Wallpaper" to set a new random wallpaper
4. A notification will appear when the wallpaper has been changed successfully

## Troubleshooting

### System Tray Icon Not Showing

If you're using Ubuntu with GNOME and the system tray icon doesn't appear:

1. Install the AppIndicator extension:
   ```bash
   sudo apt install gnome-shell-extension-appindicator
   ```

2. Enable the extension using GNOME Extensions app or through command line:
   ```bash
   gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
   ```

3. Log out and log back in

### Wallpaper Not Changing

If the wallpaper doesn't change:

1. Check if you have the correct permissions to write to the wallpaper file:
   ```bash
   chmod 644 wallpaper-changer/wallpaper.jpg
   ```

2. Verify that your desktop environment supports the gsettings command:
   ```bash
   gsettings get org.gnome.desktop.background picture-uri
   ```

3. For Ubuntu 22.04+ (GNOME 42+), also check:
   ```bash
   gsettings get org.gnome.desktop.background picture-uri-dark
   ```

4. Check the network connection to ensure images can be downloaded

### Other Issues

If you encounter any other issues:

1. Make sure all dependencies are correctly installed
2. Check that the data.json file exists in the wallpaper-changer directory
3. Try running the script from the terminal to see any error messages:
   ```bash
   cd /path/to/earthview
   python3 wallpaper-changer/indicator.py
   ```

## Data Sources

The application uses data from the Earth View by Google project:
- Website: https://earthview.withgoogle.com
- Data collection script: `script/parser.py`

## About Earth View

Earth View is a collection of the most beautiful and striking landscapes found in Google Earth. The full list of images is available in this repository or in JSON format at https://raw.githubusercontent.com/limhenry/earthview/master/earthview.json.

## License

This project is open source and available under the MIT License.
