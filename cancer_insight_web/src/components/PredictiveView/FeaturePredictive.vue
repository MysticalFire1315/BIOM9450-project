<template>
    <div class="container">
      <table class="table">
        <thead>
          <tr>
            <th>Features</th>
            <th>Expression Level</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in rows" :key="index">
            <td>
              <input type="text" v-model="row.feature" placeholder="Input Features" />
            </td>
            <td>
              <input type="text" v-model="row.expression" placeholder="Input Expression Level (0-100)" />
            </td>
            <td>
              <button
                class="minus-btn"
                v-if="index !== 0"
                @click="removeRow(index)"
              >
                -
              </button>
              <button class="minus-btn disabled" v-else disabled>-</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="addRow" class="add-btn">+</button>
      <br />
      <button @click="submitData" class="submit-btn">Submit</button>

      <!-- Model ID Input Field -->
      <div class="model-id-container">
        <label for="model-id">Model ID:</label>
        <input
          id="model-id"
          type="text"
          v-model="modelId"
          placeholder="Enter Model ID"
        />
      </div>

      <!-- Display result here -->
      <div v-if="submissionResult" class="submission-result">
        <label>Submission Result:</label>
        <p>{{ submissionResult }}</p>
      </div>
    </div>
  </template>

  <script setup>
  import { ref } from "vue";
  import apiService from "@/services/apiService";

  // Define reactive variables for rows, modelId, and submissionResult
  const rows = ref([{ feature: "", expression: "" }]);
  const modelId = ref(""); // Store the Model ID
  const submissionResult = ref(null); // Store the result message

  // Add a new row
  const addRow = () => {
    rows.value.push({ feature: "", expression: "" });
  };

  // Remove a row at a specific index
  const removeRow = (index) => {
    rows.value.splice(index, 1);
  };

  // Handle data submission
  const submitData = async () => {
    // Ensure modelId is a number (parse it as integer if it's a valid number)
    const modelIdValue = parseInt(modelId.value, 10);

    // Prepare the payload in the desired format
    const data = {
      model_id: isNaN(modelIdValue) ? 0 : modelIdValue, // If invalid, set to 0
      "*": {},
    };

    // Loop through the rows and populate the "*" object
    rows.value.forEach((row, index) => {
      const featureKey = row.feature || `additionalProp${index + 1}`; // If no feature name, use default key
      const expressionValue = parseInt(row.expression, 10); // Parse expression as integer

      // Only add the feature to the object if expression is a valid number
      if (!isNaN(expressionValue)) {
        data[featureKey] = expressionValue;
      }
    });

    try {
      const response = await apiService.postData('/ml/probability', data);
    //   console.log(response.data);
      // Display result instead of alert
      submissionResult.value = `The probability for getting the disease from this model is: ${response.data.probability}`;
    } catch (error) {
      console.log(error);
      submissionResult.value = `Error: ${error.message || "Something went wrong"}`;
    }
  };
  </script>

  <style>
  .container {
    text-align: center;
    margin: 20px auto;
    width: 60%;
  }

  .table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 100%;
  }

  .table th,
  .table td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
  }

  input[type="text"] {
    width: 90%;
    padding: 5px;
  }

  .minus-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    display: inline-flex;
    justify-content: center;
    align-items: center;
  }

  .minus-btn.disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .add-btn {
    width: 150px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }

  .submit-btn {
    margin-top: 20px;
    width: 150px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .model-id-container {
    margin-top: 20px;
  }

  .model-id-container label {
    font-size: 16px;
    margin-right: 10px;
  }

  input[type="text"] {
    width: 80%;
    padding: 5px;
    margin-top: 10px;
  }

  button:hover {
    opacity: 0.9;
  }

  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  /* Style for displaying the result */
  .submission-result {
    margin-top: 20px;
    font-size: 18px;
    font-weight: bold;
    color: #007bff;
  }
  </style>
