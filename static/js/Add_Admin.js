function add_Admin(userId) {
    console.log("heloo admin")
    fetch("/add_admin", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/admin";
      
    });
  }

