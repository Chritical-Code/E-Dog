//global variables
var deleteButton = document.getElementById("deleteButton");
var cancelButton = document.getElementById("cancelButton");
var confirmButton = document.getElementById("confirmButton");

//hide cancel and confirm button by default
cancelButton.style.display = "none";
confirmButton.style.display = "none";

//when we click the delete button
function clickDelete(){
    //show confirm and cancel button
    cancelButton.style.display = "block";
    confirmButton.style.display = "block";

    //hide this button
    deleteButton.style.display = "none";
}


//when we click cancel
function clickCancel(){
    //show delete button
    deleteButton.style.display = "block";

    //hide this and confirm button
    cancelButton.style.display = "none";
    confirmButton.style.display = "none";
}