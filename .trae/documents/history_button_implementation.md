## History Button Implementation Documentation

### 1. Feature Overview

Add a "Show History" button before the existing "Save to DB" button that:

* Fetches all records from marksix.db

* Displays them in reverse chronological order (newest first)

* Shows in a modal or dedicated section

### 2. Implementation Steps

#### 2.1 Frontend Changes

1. Add button to HTML before save-to-db button:

```html
<button id="show-history">Show History</button>
```

1. Add event listener in script.js:

```javascript
const showHistoryButton = document.getElementById('show-history');
showHistoryButton.addEventListener('click', showHistory);

async function showHistory() {
  try {
    const response = await fetch('/get-history');
    const historyData = await response.json();
    displayHistory(historyData);
  } catch (error) {
    console.error('Error fetching history:', error);
  }
}

function displayHistory(data) {
  // Sort by date descending
  const sortedData = data.sort((a,b) => new Date(b.drawDate) - new Date(a.drawDate));
  
  // Display logic here
}
```

#### 2.2 Backend API

1. Create new endpoint `/get-history` in api/proxy.py:

```python
@app.route('/get-history')
def get_history():
    # Connect to marksix.db and fetch all records
    # Return as JSON sorted by date
```

### 3. UI Design

* Use same styling as existing buttons

* Display history in a scrollable modal

* Each entry should show:

  * Draw date

  * Winning numbers

  * Extra number

### 4. Testing

1. Verify button appears correctly
2. Test fetching and displaying history
3. Confirm sorting is newest-first
4. Check error handling

