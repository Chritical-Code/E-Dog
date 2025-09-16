//save pending pictures and submit the form
async function submitEditPostForm(){
    await uploadPicture();
    
    //submit the form
    const form = document.getElementById("editPostFormID");
    form.submit();
}

//Add picture button
async function uploadPicture(){
    //get data from document
    imageField = document.getElementById("selectFile");
    postPK = document.getElementById("postPK").value;

    if(imageField.files.length > 0){
        //check file size first
        if(true){
            //make a formdata instead
            const image = imageField.files[0];
            const formData = new FormData();
            formData.append("photo", image);
            formData.append("postPK", postPK);
            
            //fetch upload it
            await upload(formData);
        }
    } else{
        console.log("No file selected");
    }
}


//fetch upload file data
async function upload(inData){
    //data sent to server
    var postData = {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
        },
        body: inData
    };

    //response
    const aResponse = await fetch("/post/fetchUploadImage/", postData);
    const aJson = await aResponse.json();
    
    //append new photo
    appendImage(aJson);

    //clear selected photo
    clearSelectedPhoto();
}


//append added image to div
function appendImage(inJson){
    //cancel if error
    if("error" in inJson){
        alert(inJson.error);
        return;
    }
    
    //get photo div
    const photoDiv = document.getElementById("photoDiv");

    //create the html
    //image and button div
    const imgAndButton = document.createElement("div");
    imgAndButton.classList.add("imageBox");
    imgAndButton.id = "imageAndButton" + inJson.imgPK;

    //append imageAndButton before the last glue
    photoDiv.insertBefore(imgAndButton, photoDiv.children[photoDiv.children.length - 1]);

    //image div
    const imageBox = document.createElement("div");
    imageBox.classList.add("imageBox");
    imgAndButton.appendChild(imageBox);
    //img
    const img = document.createElement("img");
    img.classList.add("image");
    img.id = "image" + inJson.imgPK;
    img.src = inJson.imgUrl;
    imageBox.appendChild(img);

    //delete button row
    const deleteRow = document.createElement("div");
    deleteRow.classList.add("row");
    imgAndButton.appendChild(deleteRow);

    //delete button
    const deleteButton = document.createElement("button");
    deleteButton.classList.add("deleteImageButton");
    deleteButton.id = "button" + inJson.imgPK;
    deleteButton.type = "button";
    deleteButton.setAttribute("onclick", "deleteImage(" + inJson.imgPK + ")");
    deleteRow.appendChild(deleteButton);

    //delete button text
    const deleteButtonText = document.createElement("p");
    deleteButtonText.innerText = "🗑️";
    deleteButton.appendChild(deleteButtonText);
}

function clearSelectedPhoto(){
    //get the element
    const photoSelector = document.getElementById("selectFile");

    //clear the element
    photoSelector.value = "";
}