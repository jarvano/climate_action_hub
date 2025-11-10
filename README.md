# 🌍 Climate Action Hub

A comprehensive web application for tracking and analyzing global CO2 emissions data with interactive dashboards, forecasting capabilities, and responsive design.

## 🚀 Features

### **Interactive CO2 Emissions Dashboard**
- 📊 **Real-time data visualization** with Chart.js
- 🌏 **Country-specific emissions tracking** for major nations
- 🔮 **Forecasting capabilities** for future emissions (2025-2030)
- 📱 **Fully responsive design** optimized for mobile, tablet, and desktop
- 📈 **Historical data analysis** with the last 10 years of data
- 🎨 **Modern UI/UX** with glassmorphism design and smooth animations

### **Data Processing**
- 📋 **Real data loading** from OWID CO2 dataset
- 🔄 **Smart data filtering** for countries with sufficient data coverage
- 📊 **Statistical analysis** with key metrics and trends
- 💾 **Efficient data processing** using only built-in Python modules

### **Technical Architecture**
- 🐍 **Pure Python implementation** - no external dependencies required
- 🌐 **Built-in HTTP server** - bypass Python environment issues
- 📁 **Modular codebase** with separate data processing and server components
- 🎯 **Cross-platform compatibility** - runs on Windows, macOS, and Linux

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.7+ (uses only built-in modules)
- Git (for cloning the repository)

### **Quick Start**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/climate-action-hub.git
   cd climate-action-hub
   ```

2. **Run the application:**
   ```bash
   python src/simple_server.py 8080
   ```

3. **Open your browser:**
   - Homepage: `http://localhost:8080`
   - Dashboard: `http://localhost:8080/dashboard`

## 📊 Dashboard Features

### **Interactive Controls**
- 🌐 Country selection dropdown
- 📅 Year range forecasting (2025-2030)
- 🔮 Generate forecast button with loading animations

### **Visualizations**
- 📈 **Line Chart**: Historical and forecasted CO2 emissions
- 📋 **Statistics Cards**: Current emissions, forecasts, change rates
- 📊 **Data Table**: Last 10 years of historical data

### **Responsive Design**
- 📱 **Mobile-first approach** with breakpoints at 480px, 768px, and 1024px
- 🎯 **Touch-friendly** interfaces with appropriate tap targets
- 📐 **Flexible layouts** that adapt to screen size
- 🌈 **Optimized visualizations** for different screen sizes

## 🗂️ Project Structure

```
climate_action/
├── 📁 data/
│   └── owid-co2-data.csv          # CO2 emissions dataset
├── 📁 src/
│   ├── data_processor.py          # Data processing and filtering
│   ├── simple_server.py          # HTTP server and request handling
│   ├── app.py                    # Alternative Flask app (optional)
│   └── web_server.py            # Alternative server implementation
├── 📄 index.html                  # Homepage with navigation menu
├── 📄 dashboard.html              # Main CO2 dashboard
├── 📄 requirements.txt            # Python dependencies (minimal)
├── 📄 .gitignore                  # Git ignore rules
└── 📄 README.md                   # This file
```

## 🚀 Technical Details

### **Data Processing (`data_processor.py`)**
- Loads CO2 data from CSV files
- Filters countries with sufficient data coverage (10+ years)
- Converts data types and handles missing values
- Returns structured data for dashboard consumption

### **Web Server (`simple_server.py`)**
- Built-in Python HTTP server (no external dependencies)
- Serves static HTML files and API endpoints
- Handles data requests and serves processed CO2 data
- Fallback to sample data if real data is unavailable

### **Frontend (`dashboard.html`)**
- Pure HTML, CSS, and JavaScript (no frameworks)
- Chart.js for data visualization
- Responsive CSS with media queries
- Modern glassmorphism design with animations

## 📈 Data Sources

The application uses the **Our World in Data CO2 dataset** (`owid-co2-data.csv`) which includes:
- Annual CO2 emissions by country
- Historical data from multiple decades
- Population-adjusted emissions metrics
- Comprehensive global coverage

## 🎯 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Our World in Data** for providing the comprehensive CO2 emissions dataset
- **Chart.js** for the excellent visualization library
- The **climate science community** for their vital research and data collection

## 📞 Support

If you encounter any issues or have questions:
1. Check the browser console for error messages
2. Verify the server is running on the correct port
3. Ensure the data file is present in the `data/` directory
4. Open an issue on GitHub for technical support

---

**🌍 Together, we can make a difference in understanding and addressing climate change!**