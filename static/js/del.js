

function deletePost(postId) {
   
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ postId: postId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }
  




  
function Remove_Profile(){
  window.location.href = "/remove_Profile_photo";

}

