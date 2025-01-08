# Lottery Filter Application

A web application for generating and filtering lottery combinations with advanced statistical analysis.

## Features

- Generate all possible lottery combinations
- Random set generation with filters:
  - Exact number of even numbers
  - Consecutive number filtering
- Statistical analysis:
  - Average sum
  - Even/Odd distribution
  - Consecutive number patterns
- Modern UI with:
  - Color-coded even/odd numbers
  - Real-time statistics
  - Pagination for large sets
  - Export to CSV

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mgilady99/lottery-filters.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python lottery_filter.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:8080
```

## Usage

1. Enter total numbers in lottery (e.g., 49)
2. Enter numbers to pick (e.g., 6)
3. Click "Generate Combinations"
4. Use filters to generate random sets:
   - Set exact number of even numbers
   - Filter out sets with 3+ consecutive numbers
5. Export results to CSV

## Technologies Used

- Python Flask
- Bootstrap 5
- JavaScript
- CSS3
