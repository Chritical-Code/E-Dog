async function clickNewPost(){
    //cancel if too many posts
    aJson = await checkPostCount();
    if("error" in aJson){
        alert(aJson.error);
        return;
    }

    //continue to new post page
    window.location.href = "/post/tryCreatePost/";
}

async function checkPostCount(){
    //data sent to server
    var data = {
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken,
        }
    };

    //response
    const aResponse = await fetch("/post/fetchMaxPostsCheck/", data);
    const aJson = await aResponse.json();

    return aJson;
}