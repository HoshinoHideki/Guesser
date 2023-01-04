/** Edit table row.
 * reveals a hidden form, picks data from a clicked table row and inserts
 * data into it.
 * @param {Element} button Button pressed. Needed for extracting data from
 * the table row.
 */
function editItem(button) {
  //Inserts Editing table into an empty Div.
  const [CONTAINER, EDITOR] = [
    document.getElementById('editorContainer'),
    document.getElementById('itemEditor'),
  ];
  CONTAINER.innerHTML = EDITOR.innerHTML;

  // stores the data of the row of the clicked button.
  const CELLS = button.closest('tr').cells;
  const DATA = [
    CELLS[0].innerText,
    CELLS[1].innerText,
    CELLS[2].innerText,
  ];
  // Copies data into the form.
  const ROWS = CONTAINER.querySelector('table').rows;
  for (let row of ROWS) {
    let index = row.rowIndex;
    let input = row.querySelector('input');
    input.value = DATA[index];
  }
}

/** reveal adding interface
 * Inserts adding interface into an empty div.
 */
function addItem() {
  const CONTAINER = document.getElementById('editorContainer');
  const ADDER = document.getElementById('itemAdder');
  CONTAINER.innerHTML = ADDER.innerHTML;
}

/** delete a database item.
 * Sends a POST request to web server asking to delete an entry with
 * specified id.
 * @param {Element} click Clicked table row. 
 */
function deleteItem(click) {
  confirm("Are you sure?");
  const ID = click.closest("tr").cells[0].innerText;
  const FORM_DATA = new FormData();
  FORM_DATA.append("action", "delete");
  FORM_DATA.append("id", ID);
  fetch("", {method:"POST", body:FORM_DATA})
    .then(
      response => {
        window.location = response.url;
      }
    )
}

/** Clicking the row makes you follow the link.
 * When clicking anywhere in the row, client goes via the hyperlink in the
 * third column.
 * @param {Element} click Click event. 
 */
function getLink(click) {
  location.href = click.querySelector('a');
}

/** Sort the table by clicked row
 * Sorts the table alphanumerically by clicked row.
 * @param {Element} click clicked row
 */
function sortTable(click) {
  /** Place sorting indicators.
   * Places sort order indicators at the end of the row header.
   * @param {Element} click Clicked row.
   */
  function placeTriangles(click) {
    /** Place sorting order triangle mark.
     * Places a triangle in the specified cell.
     * 
     * If no triangle is already present, sets a ascending order triangle and
     * keeps the reverse bool false.
     * 
     * If ascending triangle is already present, sets a descending order
     * triangle and switches the reverse bool to true.
     * 
     * If descending triangle is present, flips it back to ascending and also
     * switches the reverse bool to false. 
     * @param {Cell} cell Cell to which to add the triangle. 
     */
    function addTriangle(cell) {
      const LAST_CHAR = cell.innerText.slice(-1);
      if (LAST_CHAR ===  '▲') {
        cell.innerText = cell.innerText.slice(0,-1) + '▼';
        reverse = true;
      }
      else if (LAST_CHAR ===  '▼') {
        cell.innerText = cell.innerText.slice(0,-1) + '▲';
        reverse = false;
      }
      else {
        cell.innerText += '▲';
        reverse = false;
      }
    }
    /** Remove sorting order triangle mark.
     * Removes the last character of the header if it' is a sort order
     * indicator triangle.
     * @param {Element} cell Cell from which to remove the triangle. 
     */
    function removeTriangle(cell) {
      let lastChar = cell.innerText.slice(-1)
      if (lastChar === '▲' || lastChar === '▼') {
        cell.innerText = cell.innerText.slice(0,-1);
      }
    }
    let headersRow = click.closest('tr');
    for (let header of headersRow.cells) {
      if (header.cellIndex === click.cellIndex) {
        addTriangle(header);
      }
      else {
        removeTriangle(header);
      }
    }
  }
  /** Load table rows into memory.
   * Reads the table and creates an object in memory, from which to sort and
   * populate the sorted table.
   * @param {Element} click Clicked row. 
   * @return {Object} Object with sorted table rows.
   */
  function load_data(click) {
    /** Sort Array.
     * Sorts array alphanumerically by default, numerically if all the items
     * in the the array are numbers.
     * Reverses it if reverse bool is true.
     * @param {Array} array array to be sorted. 
     * @return {Array} sorted array
     */
    function sortArray(array) {
      if (array.every((a) => !isNaN(a))) {
        array.sort(function(a, b) {return a - b});
      }
      else {
        array.sort();
      }
      if (reverse) {
        array.reverse();
      }
      return array;
    }

    let data = {rows:{}, indices:{}};
    const CELL_INDEX = click.cellIndex;
    const TBODY = document.querySelector('.data');
    for (let row of TBODY.rows) {
      let text = row.cells[CELL_INDEX].innerText;
      while (data.rows[text]) {
        //this will make sure duplicates are not lost.
        let counter = 1;
        text = text + String(counter);
        counter += 1;
      }
      data.rows[text] = row.cloneNode(true);
    }
    data.indices = sortArray(Object.keys(data.rows));
    return data
  }
  /** Place table rows in sorted order
   * Deletes the rows from the table and then repopulates it in order of 
   * indices array, then makes text in whatever row is getting sorted by bold.
   * @param {Element} click Clicked row (used for making sorted row bold).
   * @param {Object} data Table row and indexes array with the order with
   * which to insert rows. 
   */
  function placeRows(click, data) {
    const TBODY = document.querySelector('.data');
    while (TBODY.rows.length > 0) {
      TBODY.deleteRow(0);
    }
    for (let index of data.indices) {
      let newRow = TBODY.insertRow();
      newRow.innerHTML = data.rows[index].innerHTML;
      for (let cell of newRow.cells) {
        if (cell.cellIndex === click.cellIndex) {
          cell.style.fontWeight = 'bold';
        }
        else {
          cell.style.fontWeight = 'normal';
        }
      }
    }
  }

  let reverse = false;
  placeTriangles(click);
  data = load_data(click);
  placeRows(click, data);
}

/** Make due decks green.
 * Scans the rows and if there are due cards, changes the background color
 * to green.
 */
function makeGreen() {
  const ROWS = document.querySelectorAll('.deck-row')
  for (let row of ROWS) {
    if (row.cells[1].innerText !== '0') {
      row.className = 'due-deck';
    }
  }
}

/** Show Answer.
 * Hides the button, shows the answer part of the card.
 */
function showAnswer() {
  const ANSWER = document.querySelector('#answer');
  const CHECK_BUTTON = document.querySelector('#check');

  CHECK_BUTTON.style.display = 'none';
  ANSWER.style.display = 'inline';
}

/** Set countdown.
 * Changes the data in the "Due next" to constantly refreshing countdown.
 */
function setCountDown() {
  /** Refresh the countdown.
   * Takes the original data saved in an object, then recalculates the
   * countdown.
   * @param {String} data Source data which must be converted to a
   * countdown. 
   * @param {Element} cells Where the countdown must be placed.
   */
  function refreshCountDown(data, cells) {
    /** Convert static date to countdown date.
     * Converts the input date to a an obj, then counts how many Days, Hours,
     * Minutes and Seconds are until this date.
     * Reloads the page if one of the dates is zero or less.
     * @param {String} date Date to be converted.
     * @returns {String} Countdown string to be placed.
     */
    function convertToCountdown(date) {
      let now = new Date().getTime();
      let countDownDate = new Date(date).getTime();
      let difference = countDownDate - now;
      let time = new Map([
        ['d ', Math.floor(difference / 86400000)],
        ['h ', Math.floor((difference % 86400000) / 3600000)],
        ['m ', Math.floor((difference % 3600000) / 60000)],
        ['s', Math.floor((difference % 60000) / 1000)],
      ]);
      let message = '';
      for (let [key, value] of time.entries()) {
        if (value != 0) {
          message += value + key;
        }
      }
      let values = Array.from(time.values());
      if (values.every((a) => a <= 0)) {
        document.location.reload();
      }
      return message;
    }
    for (let cell of data) {
      if (!isNaN(Date.parse(cell.innerText))) {
        let index = data.indexOf(cell);
        let message = convertToCountdown(cell.innerText);
        cells[index].innerText = message;
      }
    }
  }

  const CELLS = document.querySelectorAll('.next-due');
  const DATA = [];
  for (let cell of CELLS) {
    DATA.push(cell.cloneNode(true));
  }
  refreshCountDown(DATA, CELLS);
  setInterval(refreshCountDown, 1000, DATA, CELLS);  
}