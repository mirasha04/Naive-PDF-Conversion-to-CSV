Turns a text based statement PDF into a clean CSV with columns.
Uses pdfplumber to read pages offline. 
Ignores non-transaction lines like headers (Date, Balance,...), opening balance, page footers, etc
The script supports two shapes of transaction lines, with type code and without. .
Numeric fields are properly formated (float type, commas removed)
For each matched row, the script compares the current balance to the previous balance.
If the current balance increases its a deposit (positive amount)
If the current balance decreases its a withdrawal (negative amount)
Rows are then collected and written to statement.csv with a header. 
