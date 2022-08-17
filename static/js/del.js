

function deleteNote(noteId) {
   
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    })
  }
  


  function deleteImg(imgId) {
    console.log("heloo")
    fetch("/delete-Img", {
      method: "POST",
      body: JSON.stringify({ imgId: imgId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }


  
function Remove_Profile(){
  window.location.href = "/remove_Profile_photo";

}

