# MCP Air Quality Analyzer (NY & Bronx)

## 📖 Project Overview

This project implements a Model Context Protocol (MCP) server to transform Gemini into a professional **Environmental** Analyst.  
We transitioned from a small sample to a large-scale dataset of 11,000 records regarding air quality in New York and the Bronx to test the true power of the protocol.  
This system enables Gemini to query thousands of rows with 100% mathematical accuracy, avoiding the common hallucinations of standard LLMs when handling big data.

## 🏗️ Technical Infrastructure & Core Logic

The project is built on a robust foundation designed for performance and security:

- **Server core**: Developed using the FastMCP framework for seamless communication between Python and the MCP protocol.
- **Database engine**: Integrated a specialized SQLite helper to manage an in-memory database, ensuring high-speed processing for 11,000 rows.
- **Safety layer**: Implemented a security filter to block destructive commands like `DROP`, `DELETE`, or `UPDATE`, keeping the environmental data safe.
- **Resource tracking**: Added a global query history to monitor every interaction and a schema resource for real-time metadata access.

## 🛠️ Data Tools & Analysis Capabilities

We developed five specialized tools to allow the AI to interact with the air quality data:

- `load_csv`: Efficiently imports the 11k dataset into the structured SQL environment.
- `describe_schema`: Informs the AI about available columns (pollutants, geography, timestamps) to ensure precise questions.
- `run_query`: The analytical heart of the server, allowing the AI to perform complex filtering and statistical calculations.
- `get_statistics`: Provides instant count, min, max, and average values for any pollutant column.
- `list_tables`: Verifies the status of the database tables during the session.

## 🧪 Testing & Validation Results

As part of the final integration, we validated the system through three key business scenarios:

- **Geographic analysis**: Identifying which area has the worst air quality on average.
- **Regulatory standards**: Determining the different AQI categories present across the 11,000 records.
- **Pollutant precision**: Calculating the average value per specific pollutant (NO₂, PM2.5) with absolute accuracy.

**Performance note**: During tests in the MCP Inspector and Claude Desktop, the server processed the 11,000 entries instantly, confirming that the MCP integration is superior to manual data pasting for large files.

## 🚀 Installation

### 1. Environment

Create and activate a virtual environment with `uv`:

```bash
uv venv
source .venv/bin/activate  # Linux / macOS
# or
.venv\Scripts\activate     # Windows
