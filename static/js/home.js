let setting=document.getElementById('setting');
let setbox = document.getElementById("set");
// let comment =document.getElementById("comment")
let openn=false;
let openForcomm=false;

function ro(){
  
if(openn==false){
    setbox.style.display='block';
  
  console.log('wrk');
  openn=true;
  console.log(openn);

}
else{
    setbox.style.display='none';
  openn=false;
}

}


function comments(post_id){
  let comment =document.getElementById(`comment-${post_id}`)
  if(openForcomm==false){
comment.style.display='block';
openForcomm=true;
}
else{
  comment.style.display='none';
  openForcomm=false;
}
}
// console.log("befoe entry",open);
// setting.addEventListener("click",()=>{
// // setting.className +=' rotate'
// if(open == false){
    
//     setting.classList.toggle('rotate')
//     open=true;
//     console.log("after entry",open);


// }
//  if(open == true){
//     console.log("wrk")
// }

// })


let createpost =document.getElementById("creatpost")
createpost.addEventListener("click",()=>{
    createpost.style.zIndex = "1";
})



setbox.addEventListener("click",()=>{
    createpost.style.zIndex="0";
})

