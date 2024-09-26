<template>
    <div class="top-bar">
      <div class="icons">
        <i class="icon-menu">☰</i>
        <i class="icon-back">←</i>
        <i class="icon-logout">⎋</i>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "TopBar",
  };
  </script>
  
  <style scoped>
  .top-bar {
    background-color: #007bff; /* Blue color */
    color: white;
    height: 50px;
    display: flex;
    align-items: center;
    padding: 0 20px;
  }
  
  .icons {
    display: flex;
    gap: 15px;
    font-size: 20px;
    cursor: pointer;
  }
  
  .icons .icon-menu,
  .icons .icon-back,
  .icons .icon-logout {
    padding: 10px;
  }
  
  .icons .icon-menu:hover,
  .icons .icon-back:hover,
  .icons .icon-logout:hover {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 5px;
  }
  </style>
  