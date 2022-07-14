function like(noteId) {
    fetch("/like-post", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }
  
  
  function img_like(imgId) {
    fetch("/img_post-like", {
      method: "POST",
      body: JSON.stringify({ imgId: imgId }),
    }).then((_res) => {
      window.location.href = "/";
      
    });
  }