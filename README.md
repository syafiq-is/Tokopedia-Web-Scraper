# DISCLAIMER

This code was made purely for education purpose and not to be misused in any means.
This code haven't been fully optimized due to concern that too much request at a short time would burden Tokopedia Server.

# How This Works

Tokopedia utilizing a dynamic loading or lazy loading where certain part of the elements only loads when it visible by the web browser, therefore this code utilize the selenium python library to simulate the opening of the web browser, scrolling down to the bottom, and pressing the next page button.

## New Way (Infinite dynamic scrolling)

So in a summary it works like this:

1. Simulate the opening of a web browser using selenium driver
2. Then it waits until all the products element containers loads
3. Let user do a search
4. User scroll and load all products
5. User input anything in terminal, than start scraping
6. Using Beautiful Soup to parse the HTML and extract the data we need
7. Close the web browser driver

## Old (Pagination is removed)

So in a summary it works like this:

1. Simulate the opening of a web browser using selenium driver
2. Then it waits until all the products element containers loads
3. Progressively scroll to the bottom
4. Using Beautiful Soup to parse the HTML and extract the data we need
5. Press the next page button.
6. Close the web browser driver

# How to run

Just like running every python code

```bash
python -u "[PATH_TO_FILE]/main.py"
```
