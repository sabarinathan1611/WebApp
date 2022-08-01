

function deleteNote(noteId) {
    alert('Do you wante to delete this post');
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
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

