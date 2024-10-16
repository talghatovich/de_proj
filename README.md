# Data Engineering Project

This project focuses on building a robust data engineering pipeline with a web scraping and geocoding component. It involves extracting real estate data from **Krisha.kz**, transforming it into a structured format, and geocoding street addresses into geographic coordinates using the **Google Maps API**.

## Project Structure
.
├── README.md                    # Project overview (this file)
├── data/                        
│   └── data_new.csv             # Sample data used in the project
├── script/                      # Directory containing the Python scripts
│   ├── constants.py             # Configuration constants
│   ├── coordinates_converter.py # Uses Google Maps API for geocoding
│   ├── etl.py                   # ETL process implementation
│   ├── parser.py                # Web scraper for Krisha.kz data


## Technologies Used
- **Python**: Primary language for scripting, data extraction, and transformation.
- **Google Maps API**: Converts street addresses from Krisha.kz into geographic coordinates.
- **Web Scraping**: Extracts real estate data from **Krisha.kz**.
- **ETL Framework**: Custom-built ETL pipeline to extract, transform, and load data.
- **Git**: Version control system for tracking changes and collaboration.

## How to Run
1. Clone the repository:  
   ```bash
   git clone <repository_url>
