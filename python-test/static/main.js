async function toggleFollow(followedId) {
  const button = document.getElementById(`follow-button-${followedId}`);
  const isFollowing = button.innerText === "Unfollow";
  const endpoint = isFollowing ? "/api/unfollow" : "/api/follow";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ followed_id: followedId }),
    });

    if (response.ok) {
      button.innerText = isFollowing ? "Follow" : "Unfollow";
    } else {
      const data = await response.json();
      alert(data.message);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
