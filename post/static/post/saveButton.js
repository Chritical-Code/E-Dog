function savePost(){
    //upload pic if they forgot to click upload
    uploadPicture();
    
    //submit form
    var form = document.getElementById("editPostFormID");
    form.submit();
}