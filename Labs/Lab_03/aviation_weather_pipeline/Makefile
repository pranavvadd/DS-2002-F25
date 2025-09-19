.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "Running fetch script..."
	./fetch_metars.sh
	@echo "Fetch complete. Data saved in raw_metars/."

analyze: fetch
	@echo "Running analysis script..."
	./analyze_data.sh
	@echo "Analysis complete. Output: weather_report.csv"

clean:
	@echo "Cleaning up generated files..."
	rm -rf raw_metars weather_report.csv
	@echo "Cleanup complete."
