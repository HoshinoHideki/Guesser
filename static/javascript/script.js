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
  editorContainer.querySelector("#card_id").value = id;
  editorContainer.querySelector("#key_0").value = key_0;
  editorContainer.querySelector("#key_1").value = key_1;
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

  if (reverse == false){
      reverse = true;
  } else if (reverse == true){
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
  
  dueCells = document.querySelectorAll(".next-due");
  originalDueCells = [];

  for (var i=0; i < dueCells.length; i++){
    originalDueCells.push(dueCells[i].cloneNode(true))
  };
  
  refreshCountDown();
};

function refreshCountDown(){
  
  var now = new Date().getTime();

  for (var i = 0; i < originalDueCells.length; i++){
    if (dueCells[i].innerText != "Right now") {
      let countDownDate = new Date(originalDueCells[i].innerText).getTime();
      let difference = countDownDate - now;

      let days = Math.floor(difference / (1000 * 60 * 60 * 24));
      let hours = Math.floor(
        (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
      let minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      let seconds = Math.floor((difference % (1000 * 60)) / 1000);
      dueCells[i].innerText = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
    };
  };
};
