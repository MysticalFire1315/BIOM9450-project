<template>
  <div class="dashboard-container">
    <h1>Welcome, {{ username }}!</h1>
    <div class="button-container">
      <button class="dashboard-button">Patient Overview</button>
      <button class="dashboard-button">Predictive Analysis</button>
      <button class="dashboard-button">New Profile</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserDashboard",
  props: {
    username: String
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 50px); /* Adjust for the top bar */
}

h1 {
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.dashboard-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.dashboard-button:hover {
  background-color: #0056b3;
}
</style>
