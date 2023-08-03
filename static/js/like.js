
  
  // function comment(noteId) {
  //   fetch("/comment", {
  //     method: "POST",
  //     body: JSON.stringify({ noteId: noteId }),
  //   }).then((_res) => {
  //     window.location.href = "/";
      
  //   });
  // }
  
  function like(noteId){
    const likeCount = document.getElementById(`likes-count-${noteId}`);
    const likeButton = document.getElementById(`like-button-${noteId}`);
    
    fetch(`/like-post/${noteId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.src = "static/images/logo/like.svg";
      } else { 
        likeButton.src = "static/images/logo/unlike.svg";
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
        console.log("Like");
        likeButton.src = "static/images/logo/like.svg";
      } else {
        console.log("Like");
        likeButton.src = "static/images/logo/unlike.svg";

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

  document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the input value
    var name = document.getElementById('myInput').value;
    
    // Create the request body
    var data = {
      name: name
    };

    // Send the request to the server
    fetch('/comment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(function(response) {
      // Handle the response from the server
      if (response.ok) {
        console.log('Request sent successfully');
        // Do something with the response, if needed
      } else {
        console.log('Request failed');
      }
    })
    .catch(function(error) {
      console.log('Error:', error);
    });
  });