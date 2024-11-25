<template>
    <v-file-input
      accept=".vcf"
      label="Upload VCF File"
      @change="handleFileChange"
    ></v-file-input>
  </template>
  
  <script setup>
//   import { ref } from "vue";
  
  const handleFileChange = (file) => {
    if (!file) {
      alert("No file selected.");
      return;
    }
  
    if (file.name && file.name.split(".").pop().toLowerCase() !== "vcf") {
      alert("Please upload a valid .vcf file!");
      return;
    }
  
    alert("File selected successfully!");
    console.log("Selected file:", file);
  };
  </script>
  