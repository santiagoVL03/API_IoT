// apiurl = 'http://10.7.134.119:5000/';
apiurl = 'http://localhost:8000/';

async function fetchData(endpoint) {
	try {
		const response = await fetch(endpoint);
		if (!response.ok) {
			throw new Error('Network response was not ok ' + response.statusText);
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('There has been a problem with your fetch operation:', error);
		return null;
	}
}

document.addEventListener('DOMContentLoaded', async function() {
	const endpoint_giroscopio_actual_data = apiurl + 'api/v1/iotgiroscopio/iotshow'; // Replace with your API endpoint
	const endpoint_giroscopio_dia_data = apiurl + 'api/v1/iotgiroscopio/iotshowday'; // Replace with your API endpoint

	while (true) {
		var last_data = await fetchData(endpoint); 

	}
});