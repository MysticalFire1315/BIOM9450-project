export const data = {
    labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC-ROC'],
    datasets: [
      {
        label: 'Model1',
        data: [0.85, 0.8, 0.75, 0.78, 0.83], // Replace with actual values
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2
      },
      {
        label: 'Model2',
        data: [0.5, 0.9, 0.4, 0.2, 0.1], // Replace with actual values
        backgroundColor: 'rgba(235, 162, 54, 0.2)',
        borderColor: 'rgba(235, 162, 54, 1)',
        borderWidth: 2
      }
    ]
  }
  
  export const options = {
    responsive: true,
    scales: {
      r: {
        beginAtZero: true,
        max: 1,
        min: 0,
        ticks: {
          stepSize: 0.1
        }
      }
    },
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    }
  }
  