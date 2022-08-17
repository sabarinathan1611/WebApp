// function like(noteId) {
//     fetch("/like-post", {
//       method: "POST",
//       body: JSON.stringify({ noteId: noteId }),
//     }).then((_res) => {
//       window.location.href = "/";
      
//     });
//   }
  
  function comment(noteId) {
    fetch("/comment", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }
  
  function like(noteId){
    const likeCount = document.getElementById(`likes-count-${noteId}`);
    const likeButton = document.getElementById(`like-button-${noteId}`);
    
    fetch(`/like-post/${noteId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";
      } else { 
        likeButton.className = "far fa-thumbs-up";
      }
    })
    .catch((e) => alert("Could not like post."));
  }



function img_like(imgId){
    const likeCount = document.getElementById(`likes-count-${imgId}`);
    const likeButton = document.getElementById(`like-button-${imgId}`);
    
    fetch(`/img_post-like/${imgId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      
      console.log(data["liked"]);
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";
      } else { 
        likeButton.className = "far fa-thumbs-up";
      }
    })
    .catch((e) => alert("Could not like post."));
  }


  // function img_like(imgId) {
  //   fetch("/img_post-like", {
  //     method: "POST",
  //     body: JSON.stringify({ imgId: imgId }),
  //   }).then((_res) => {
  //     window.location.href = "/";
      
  //   });
  // }