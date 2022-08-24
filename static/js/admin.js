function deleteUser(userId) {
  console.log("heloo admin")
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/admin";
    
  });
}






function add_Admin(userId) {
    console.log("heloo admin")
    fetch("/add-admin", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }


  function removeAdmin(userId) {
    console.log("heloo admin")
    fetch("/remove-admin", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }


