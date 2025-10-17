# Shri Jayasakthi Billing Software

An offline billing and invoice generation software for Shri Jayasakthi Traders.

## Features

- Customer Management with JSON storage
- Product catalog management
- GST calculation (CGST + SGST)
- Invoice generation with HTML output
- Configurable tax rates
- Print-ready invoices

## Installation

### For macOS Users:

1. Download the `BillingSoftware.app` from the dist folder
2. Double-click to run the application
3. If you see a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"

### For Command Line:

Run the executable directly:

```bash
./dist/BillingSoftware
```

## Configuration

The application uses `config.json` for business settings and tax rates:

- **Tax Settings**: Configure CGST and SGST rates (default: 2.5% each)
- **Business Details**: Update company information, GSTIN, bank details
- **Product Settings**: Configure default HSN codes

## Files

- `config.json` - Business configuration and tax settings
- `customer_data.json` - Customer database
- `Cone_names.txt` - Product catalog
- `invoice.html` - Generated invoice output

## Usage

1. **Add Customer**: Click "Add New Customer" to add new customers
2. **Select Customer**: Choose from dropdown to auto-fill customer details
3. **Add Items**:
   - Select product from dropdown
   - Enter quantity and rate
   - Click "Add To Bill"
4. **Print Invoice**: Click "Print" to generate and open invoice in browser

## Tax Rates

Current tax configuration:

- CGST: 2.5%
- SGST: 2.5%
- Total GST: 5%

To change tax rates, edit `config.json`:

```json
"tax_settings": {
  "cgst_rate": 2.5,
  "sgst_rate": 2.5
}
```

## Building from Source

Requirements:

- Python 3.8+
- tkinter (usually comes with Python)
- Dependencies: `pip install -r requirements.txt`

Build command:

```bash
pyinstaller --clean BillingSoftware.spec
```

## Support

For issues or questions, please contact Shri Jayasakthi Traders.

## License

© 2024 Shri Jayasakthi Traders. All rights reserved.
