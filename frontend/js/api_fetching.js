// D3-based polling and plotting for gyroscope last data
(() => {
    console.log('api_fetching.js loaded');
	const API_URL = 'http://10.7.134.119:5000/api/v1/iotgiroscopio/iotshow';
	const container = d3.select('#gyroscope-data-graphic');
	const statusEl = document.querySelector('#gyroscope-sensor .sensor-status');

	if (container.empty()) return;

	const margin = { top: 10, right: 20, bottom: 20, left: 40 };
	const width = 500;
	const height = 220;

	const svg = container
		.append('svg')
		.attr('width', width)
		.attr('height', height);

	const plotW = width - margin.left - margin.right;
	const plotH = height - margin.top - margin.bottom;
	const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

	const x = d3.scaleTime().range([0, plotW]);
	const y = d3.scaleLinear().range([plotH, 0]);

	const xAxisG = g.append('g').attr('transform', `translate(0,${plotH})`);
	const yAxisG = g.append('g');

	const line = d3
		.line()
		.x(d => x(d.t))
		.y(d => y(d.v))
		.curve(d3.curveMonotoneX);

	const path = g
		.append('path')
		.attr('fill', 'none')
		.attr('stroke', '#00bcd4')
		.attr('stroke-width', 2);

	const title = g
		.append('text')
		.attr('x', 0)
		.attr('y', -2)
		.attr('fill', '#00bcd4')
		.attr('font-size', 12)
		.text('Gyroscope magnitude (|G| from gx, gy, gz)');

	const MAX_POINTS = 120; // store last 2 minutes at 1Hz
	const data = [];
	let lastId = null;

	function safeNum(n) {
		if (n === null || n === undefined || n === '' || Number.isNaN(+n)) return 0;
		const v = +n;
		return Number.isFinite(v) ? v : 0;
	}

	function updateChart() {
		if (!data.length) return;
		const tExtent = d3.extent(data, d => d.t);
		x.domain(tExtent);

		const vExtent = d3.extent(data, d => d.v);
		const pad = 0.1 * (vExtent[1] - vExtent[0] || 1);
		y.domain([vExtent[0] - pad, vExtent[1] + pad]);

		xAxisG.call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat('%H:%M:%S')));
		yAxisG.call(d3.axisLeft(y).ticks(5));

		path.datum(data).attr('d', line);
	}

	function updateTable(magnitude, isoDate) {
		const row = document.querySelector('#table-renderer-data tbody tr:nth-child(1)');
		if (!row) return;
		const tds = row.querySelectorAll('td');
		if (tds[1]) tds[1].textContent = Number.isFinite(magnitude) ? magnitude.toFixed(2) : 'N/A';
		if (tds[2]) tds[2].textContent = isoDate || new Date().toISOString();
	}

	async function poll() {
		try {
			const resp = await d3.json(API_URL, { cache: 'no-cache' });
			const payload = resp && resp.data ? resp.data : null;
			if (!payload || payload.error) {
				if (statusEl) statusEl.textContent = 'Sin datos';
				return;
			}

			const id = payload.id_sensor;
			if (id === lastId) return; // no new data
			lastId = id;

			if (statusEl) statusEl.textContent = 'Activo';

			const gx = safeNum(payload.gx);
			const gy = safeNum(payload.gy);
			const gz = safeNum(payload.gz);
			const magnitude = Math.sqrt(gx * gx + gy * gy + gz * gz);
			const t = payload.date_uploaded ? new Date(payload.date_uploaded) : new Date();
			data.push({ t, v: magnitude });
			if (data.length > MAX_POINTS) data.shift();

			updateChart();
			updateTable(magnitude, payload.date_uploaded);
		} catch (e) {
			// network or parse error, keep silent but update status
			if (statusEl) statusEl.textContent = 'Error de conexión';
		}
	}

	// kick-off and schedule
	poll();
	setInterval(poll, 1000);
})();

