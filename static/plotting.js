async function dataGraphing() {
	console.log('doing')

	let response = await fetch('/data');
	let data = await response.json();

	Object.keys(data).forEach(stock => {
		const chartCanvas = document.getElementById(stock); // chart

		// TODO: assign to html values
		let cash = data[stock].cash;
		let shares = data[stock].shares;
		let value = data[stock].value;

		let history = data[stock].history;
		let dates = data[stock].dates;

		new Chart(chartCanvas , {
			type: 'line',
			data: {
				labels: dates,
				datasets: [{
					label: 'Price',
					data: history,
					backgroundColor: 'rgba(115, 0, 115, 1.0)',
					borderColor: "rgba(95, 0, 95, 1.0)",
					tension: 0.15
				}]
			},
			options: {
				plugins: {
					legend: {
						display: false
					}
				}
			}
		});

	});
}




// const aapl = document.getElementById('aapl');

// let xVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
// let yVals = [10, 18, 13, 16, 12, 13, 22, 15, 16, 18]

// new Chart(aapl, {
// 	type: 'line',
// 	data: {
// 		labels: xVals,
// 		datasets: [{
// 			label: 'Price',
// 			data: yVals,
// 			backgroundColor: 'rgba(115, 0, 115, 1.0)',
// 			borderColor: "rgba(95, 0, 95, 1.0)",
// 			tension: 0.15
// 		}]
// 	},
// 	options: {
// 		plugins: {
// 			legend: {
// 				display: false
// 			}
// 		}
// 	}
// });

// const amzn = document.getElementById('amzn');

// new Chart(amzn, {
// 	type: 'line',
// 	data: {
// 		labels: xVals,
// 		datasets: [{
// 			label: 'Price',
// 			data: yVals,
// 			backgroundColor: 'rgba(115, 0, 115, 1.0)',
// 			borderColor: "rgba(95, 0, 95, 1.0)",
// 			tension: 0.15
// 		}]
// 	},
// 	options: {
// 		plugins: {
// 			legend: {
// 				display: false
// 			}
// 		}
// 	}
// });


// const goog = document.getElementById('goog');

// new Chart(goog, {
// 	type: 'line',
// 	data: {
// 		labels: xVals,
// 		datasets: [{
// 			label: 'Price',
// 			data: yVals,
// 			backgroundColor: 'rgba(115, 0, 115, 1.0)',
// 			borderColor: "rgba(95, 0, 95, 1.0)",
// 			tension: 0.15
// 		}]
// 	},
// 	options: {
// 		plugins: {
// 			legend: {
// 				display: false
// 			}
// 		}
// 	}
// });

// const voo = document.getElementById('voo');

// new Chart(voo, {
//   type: 'line',
//   data: {
//     labels: xVals,
//     datasets: [{
//       label: 'Price',
//       data: yVals,
//       backgroundColor: 'rgba(115, 0, 115, 1.0)',
//       borderColor: "rgba(95, 0, 95, 1.0)",
//       tension: 0.15
//     }]
//   },
//   options: {
//     plugins:{
//       legend:{
//         display: false
//       }
//     }
//   }
// });

document.addEventListener('DOMContentLoaded', dataGraphing)