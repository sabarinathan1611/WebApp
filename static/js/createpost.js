const textarea = document.querySelector("textarea");
textarea.addEventListener("keyup", e => {
  textarea.style.height = "59px";
  let scHeight = e.target.scrollHeight;

  textarea.style.height = `${scHeight}px`;
});
let op=false;
function creatPostu(){

const wrap=document.querySelector('.wrapper');

  
  if(op==false){
      wrap.style.display='block';
    
    console.log('wrk');
    op=true;
    console.log(op);

  }
  else{
      wrap.style.display='none';
    op=false;
  }

}