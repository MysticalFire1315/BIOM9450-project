export const data = {
    labels: ['DB1', 'DB2', 'DB3', 'DB4'],
    datasets: [
      {
        backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16'],
        data: [40, 20, 80, 10]
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
  