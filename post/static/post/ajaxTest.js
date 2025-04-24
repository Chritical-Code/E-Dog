//Ajax Test

//functions
//test func
async function logMovies() {
    const inResponse = await fetch("/post/fetchRando/");
    const inJson = await inResponse.json();
    console.log(inJson.randoNum);

    document.getElementById("rando").innerText = inJson.randoNum;
  }

//make a new test function for testing this keyboard
function keyboardTest(){
  var counter = 0;
  while(counter < 100){
    console.log(counter);
    counter++;
  }
}