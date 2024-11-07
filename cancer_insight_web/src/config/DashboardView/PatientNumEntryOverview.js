export const data = {
    labels: ['Not linked', 'Linked', 'No account'],
    datasets: [
      {
        backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
        data: [56, 21, 45]
      }
    ]
  }
  
export const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right'  // Set the legend position to 'right'
    }
  }
}
  