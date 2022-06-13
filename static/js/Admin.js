function deleteUser(userId) {
  console.log("heloo admin")
  fetch("/delete_user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/admin";
    
  });
}






function add_Admin(userId) {
    console.log("heloo admin")
    fetch("/add_admin", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }


  function removeAdmin(userId) {
    console.log("heloo admin")
    fetch("/remove_admin", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }


