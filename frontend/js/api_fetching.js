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

// Main data fetching functions
// Graphics are now handled by api_graphics.js

document.addEventListener('DOMContentLoaded', function() {
	console.log('API fetching module loaded');
});