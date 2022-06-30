var editorContainer, itemEditor, itemAdder, reverse

window.onload = function(){
  editorContainer = document.getElementById("editorContainer");
  itemEditor = document.getElementById("itemEditor");
  itemAdder = document.getElementById("itemAdder");
  reverse = false;
};

function editItem(button){
  
  var data = button.closest("tr");
  var id = data.cells[0].innerText;
  var key_0 = data.cells[1].innerText;
  var key_1 = data.cells[2].innerText;

  editorContainer.innerHTML = itemEditor.innerHTML;

  editorContainer.querySelector("#card_id").value = id;
  editorContainer.querySelector("#key_0").value = key_0;
  editorContainer.querySelector("#key_1").value = key_1;
};


function addItem(){
  editorContainer.innerHTML = itemAdder.innerHTML;
};


function getLink(row){
  location.href = row.cells[3].querySelector("a");
};


function sortItems(row){
  var table = document.getElementById("data-table");
  var tableData = table.cloneNode(true);
  var indices = [];
  var cellIndex = row.cellIndex

  function isNumber(element){
      return !isNaN(element);
  };

  tableData.deleteRow(0);

  while (table.rows.length > 1) {
      table.deleteRow(1);
  };

  for (var i=0;  i < tableData.rows.length; i++){
      var text = tableData.rows[i].cells[cellIndex].innerText;
      indices.push(text);
  };

  if (indices.every(isNumber)){indices.sort(function(a, b){return a - b})}

  else {indices.sort()};

  if (reverse) {indices.reverse()}

  for (var i=0;  i < indices.length; i++){
      for (var j=0; j<tableData.rows.length; j++){
          if (indices[i] == tableData.rows[j].cells[cellIndex].innerText){
              var rowdata = table.insertRow();
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

function makeGreen(){
  let rows = document.querySelectorAll(".deck-row")
  for (row in rows) {
      if (rows[row].cells[1].innerText != "0"){
          rows[row].className = "due-deck";
      };
  };
};

function showAnswer() {
  answer = document.querySelector("#answer");
  checkButton = document.querySelector("#check");
  checkButton.style.display = "none";
  answer.style.display = "inline";
};