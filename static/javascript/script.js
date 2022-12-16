var editorContainer, itemEditor, itemAdder, reverse

window.onload = function(){
  // this assigns html elements to JS variables.

  //empty div containing item editor interface.
  editorContainer = document.getElementById("editorContainer");

  // div containing item editing form
  itemEditor = document.getElementById("itemEditor");

  // div containing item adding form
  itemAdder = document.getElementById("itemAdder");
  reverse = false;
};


function editItem(button){
  // picks data from a table row, reveals a hidden form and inserts
  // data into it.
  // The data is fetched from the HTML after page render,
  // not from the database.

  // stores the data from the nearest row of clicking.
  var row = button.closest("tr");
  
  //Gets item ID, key_0 and key_1 from HTML.
  var id = row.cells[0].innerText;
  var key_0 = row.cells[1].innerText;
  var key_1 = row.cells[2].innerText;

  //Inserts Editing table into an empty Div.
  editorContainer.innerHTML = itemEditor.innerHTML;

  //populates the table with data.
  editorContainer.querySelector("#id").value = id;
  editorContainer.querySelector("#key0").value = key_0;
  editorContainer.querySelector("#key1").value = key_1;
};


function addItem(){
  // Inserts adding table into an empty div.

  editorContainer.innerHTML = itemAdder.innerHTML;
};


function getLink(row){
  //When clicking anywhere in the row, 
  //client goes via the hyperlink in the third row.

  location.href = row.cells[3].querySelector("a");
};


function sortItems(row){
  //sorts the table alphanumerically by clicked row.
  
  //assign table element to a variable
  var tableHTML = document.getElementById("data-table");

  //clone data into a different variable.
  var tableData = tableHTML.cloneNode(true);

  //deletes the headers row 
  tableData.deleteRow(0);

  //create empty list of row values to sort.
  var indices = [];

  //gets index of the row we need to sort by. 
  var cellIndex = row.cellIndex
  
  // clears the table on the page, leaving only headers.
  while (tableHTML.rows.length > 1) {
      tableHTML.deleteRow(1);
  };

  // adds row contents to the list.
  for (var i=0;  i < tableData.rows.length; i++){
      var text = tableData.rows[i].cells[cellIndex].innerText;
      indices.push(text);
  };

  // checks if it's all numbers, then sorts numerically if yes.
  if (indices.every(isNumber)){
    indices.sort(function(a, b){
      return a - b}
      )
  }

  // sorts usually if not.
  else {indices.sort()};

  // reverses indices when the row header is clicked again.
  if (reverse) {indices.reverse()}

  // takes value from the indices list, then scans the data-table and finds
  // the corresponding row, then inserts row in the html-table.
  for (var i=0;  i < indices.length; i++){
      for (var j=0; j<tableData.rows.length; j++){
          if (indices[i] == tableData.rows[j].cells[cellIndex].innerText){
              var rowdata = tableHTML.insertRow();
              rowdata.innerHTML = tableData.rows[j].innerHTML;
          };
      };
  };

  // switches the reverse bool, also changes the sorting icon.
  var lastChar = row.innerText.slice(-1) // last character of the header.

  // set ascending order.
  if (reverse == false){
      if (lastChar != "▲" && lastChar != "▼" ){
      row.innerText += "▲";}
      else {row.innerText = row.innerText.slice(0,-1) + "▲"};
      reverse = true;
  }
  // set descending order.
  else if (reverse == true){
      if (lastChar != "▲" && lastChar != "▼" ){
      row.innerText += "▼";}
      else {row.innerText = row.innerText.slice(0,-1) + "▼"};
      reverse = false;
  };
};


function isNumber(element){
  //returns True if element is number, false if not.

    return !isNaN(element);
};


function makeGreen(){
  // selects all rows with the CSS class deck-row, then changes CSS class
  // to due-deck (making background color green) if there are due cards.

  let rows = document.querySelectorAll(".deck-row")
  for (var row = 0; row < rows.length; row++) {
      if (rows[row].cells[1].innerText != "0"){
          rows[row].className = "due-deck";
      };
  };
};


function showAnswer() {
// hides check button, shows the answer div.

  answer = document.querySelector("#answer");
  checkButton = document.querySelector("#check");

  checkButton.style.display = "none";
  answer.style.display = "inline";
};


function setCountDown(){
  // Changes the static date of next due card to a dynamic countdown.

  // picks up every cell with the class "next-due"
  dueCells = document.querySelectorAll(".next-due");

  // make an empty global list to store the data, then populate it from the
  // node list.
  // we need it to continuosly refresh the countodwn.
  originalDueCells = [];
  for (var i=0; i < dueCells.length; i++){
    originalDueCells.push(dueCells[i].cloneNode(true))
  };
  
  // does the actual deed.
  refreshCountDown();
};

function refreshCountDown(){
  
  var now = new Date().getTime();
  
  // cycles through the list, excluding cells that have "right now"
  // in them.
  // substracts now from the due date and then converts it to days\hr\m\s.
  for (var i = 0; i < originalDueCells.length; i++){
    if (dueCells[i].innerText != "Right now") {

      let countDownDate = new Date(originalDueCells[i].innerText).getTime();
      let difference = countDownDate - now;

      let days = Math.floor(difference / 86400000);
      let hours = Math.floor((difference % 86400000) / 3600000);
      let minutes = Math.floor((difference % 3600000) / 60000);
      let seconds = Math.floor((difference % 60000) / 1000);

      let message = ""; // text to be displayed instead of static date.

      // adds only significant time units.
      if (days != 0){message += days + "d "};
      if (hours != 0){message += hours + "h "};
      if (minutes != 0){message += minutes + "m "};
      if (seconds != 0){message += seconds + "s "};

      if (seconds < 0) {message = "Right now"};

      dueCells[i].innerText = message;
    };
  };
};
