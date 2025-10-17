# Build Instructions for Shri Jayasakthi Billing Software

## Building for Windows

### Prerequisites

1. Install Python 3.8+ from https://python.org
2. Install required packages:

```bash
pip install tkinter inflect==7.3.1 tkcalendar==1.6.1 babel==2.15.0 pyinstaller==6.9.0
```

### Build Steps

1. Clone the repository:

```bash
git clone https://github.com/AmbroseGethu/wx-bill.git
cd wx-bill
```

2. Build the Windows executable:

```bash
pyinstaller --clean BillingSoftware_Windows.spec
```

3. The executable will be created in `dist/BillingSoftware.exe`

4. Create distribution package:
   - Copy `BillingSoftware.exe` from `dist/`
   - Include these files:
     - `config.json`
     - `customer_data.json`
     - `Cone_names.txt`
     - `README.md`
   - Zip all files together as `BillingSoftware_v1.0.0_Windows.zip`

## Building for macOS

### Prerequisites

1. Install Python 3.8+
2. Install required packages:

```bash
pip install tkinter inflect==7.3.1 tkcalendar==1.6.1 babel==2.15.0 pyinstaller==6.9.0
```

### Build Steps

1. Clone the repository:

```bash
git clone https://github.com/AmbroseGethu/wx-bill.git
cd wx-bill
```

2. Build the macOS application:

```bash
pyinstaller --clean BillingSoftware.spec
```

3. The application will be created in `dist/BillingSoftware.app`

4. Create distribution package:

```bash
mkdir -p BillingSoftware_Package
cp -r dist/BillingSoftware.app BillingSoftware_Package/
cp config.json customer_data.json Cone_names.txt README.md BillingSoftware_Package/
cd BillingSoftware_Package
zip -r ../BillingSoftware_v1.0.0_macOS.zip *
```

## Running from Source

### All Platforms

1. Install Python 3.8+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python Main.py
```

## Notes

- The application requires `config.json`, `customer_data.json`, and `Cone_names.txt` to be in the same directory as the executable
- On first run, Windows may show a security warning - click "More info" and "Run anyway"
- On macOS, if you see a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"
