//begin
//get post pk
docPostPK = document.getElementById("postPK").value;
postPK = parseInt(docPostPK);

//initialize pin button
fetchTogglePin("getToggle");


//pin the post
function pinPost(){
    //send a fetch
    fetchTogglePin(document.getElementById("pinButton").textContent);
}

//Fetch call the function to pin the post
async function fetchTogglePin(inAction){
    //make dictionary to send to server
    const data = new FormData();
    data.append("postPK", postPK);

    //set boolpin based on button text
    data.append("action", inAction);
    
    //data sent to server
    var postData = {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
        },
        body: data,
    };

    //response
    const aResponse = await fetch("/user/fetchTogglePin/", postData);
    const aJson = await aResponse.json();
    console.log(aJson.buttonToggle);

    //update button
    updatePinButton(aJson.buttonToggle);
}

//update button to either unpin or pin now
function updatePinButton(buttonToggle){
    //set text
    pinButton = document.getElementById("pinButton");
    pinButton.textContent = buttonToggle;
}