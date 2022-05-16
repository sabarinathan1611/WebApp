function deleteUser(userId) {
    console.log("heloo admin")
    fetch("/delete_user", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }

