//Delete the selected picture
function deleteImage(inPK){
    console.log("deleting " + inPK);
    //get element
    div = document.getElementById("imageAndButton" + inPK);

    //hide element
    div.style.display = "none";

    //fetch delete element
    deleteImageOnServer(inPK)
}

//Fetch function to delete the image on server
async function deleteImageOnServer(inPK){
    //make dictionary to send to server
    data = {
        "imagePK": inPK,
    };
    
    //data sent to server
    var postData = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
    };

    //response
    const aResponse = await fetch("/post/fetchEditDeletePic/", postData);
    const aJson = await aResponse.json();
}