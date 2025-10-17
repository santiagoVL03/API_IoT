// Real-time gyroscope graphics using D3.js

class GyroscopeGraphics {
    constructor() {
        this.realtimeData = [];
        this.maxRealtimePoints = 20; // Keep last 20 points for real-time graph
        this.apiUrl = 'http://localhost:8000/';
        
        this.initializeGraphics();
        this.startDataFetching();
    }

    initializeGraphics() {
        this.createRealtimeGraph();
        this.createDayGraph();
    }

    createRealtimeGraph() {
        const container = d3.select("#gyroscope-data-graphic");
        container.selectAll("*").remove(); // Clear any existing content

        // Set dimensions and margins
        const margin = { top: 30, right: 40, bottom: 30, left: 40 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        // Create SVG
        const svg = container
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        const g = svg.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Create scales
        this.realtimeXScale = d3.scaleTime()
            .range([0, width]);

        this.realtimeYScale = d3.scaleLinear()
            .range([height, 0]);

        // Create axes
        this.realtimeXAxis = g.append("g")
            .attr("transform", `translate(0,${height})`)
            .attr("class", "x-axis");

        this.realtimeYAxis = g.append("g")
            .attr("class", "y-axis");

        // Create line generators
        this.realtimeLineGx = d3.line()
            .x(d => this.realtimeXScale(d.date))
            .y(d => this.realtimeYScale(d.gx))
            .curve(d3.curveMonotoneX);

        this.realtimeLineGy = d3.line()
            .x(d => this.realtimeXScale(d.date))
            .y(d => this.realtimeYScale(d.gy))
            .curve(d3.curveMonotoneX);

        this.realtimeLineGz = d3.line()
            .x(d => this.realtimeXScale(d.date))
            .y(d => this.realtimeYScale(d.gz))
            .curve(d3.curveMonotoneX);

        // Create paths
        this.realtimePathGx = g.append("path")
            .attr("class", "line-gx")
            .attr("fill", "none")
            .attr("stroke", "#ff6b6b")
            .attr("stroke-width", 2);

        this.realtimePathGy = g.append("path")
            .attr("class", "line-gy")
            .attr("fill", "none")
            .attr("stroke", "#4ecdc4")
            .attr("stroke-width", 2);

        this.realtimePathGz = g.append("path")
            .attr("class", "line-gz")
            .attr("fill", "none")
            .attr("stroke", "#45b7d1")
            .attr("stroke-width", 2);

        // Add legend
        const legend = g.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${width - 100}, 20)`);

        legend.append("rect")
            .attr("width", 90)
            .attr("height", 60)
            .attr("fill", "rgba(0,0,0,0.5)")
            .attr("stroke", "#666");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 15).attr("y2", 15).attr("stroke", "#ff6b6b").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 19).text("GX").attr("fill", "white").attr("font-size", "12px");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 30).attr("y2", 30).attr("stroke", "#4ecdc4").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 34).text("GY").attr("fill", "white").attr("font-size", "12px");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 45).attr("y2", 45).attr("stroke", "#45b7d1").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 49).text("GZ").attr("fill", "white").attr("font-size", "12px");

        // Add axis labels
        g.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .style("fill", "white")

        g.append("text")
            .attr("transform", `translate(${width / 2}, ${height + margin.bottom})`)
            .style("text-anchor", "middle")
            .style("fill", "white")
            .text("Time");
    }

    createDayGraph() {
        const container = d3.select("#gyroscope-day-graphic");
        container.selectAll("*").remove(); // Clear any existing content

        // Set dimensions and margins
        const margin = { top: 30, right: 40, bottom: 30, left: 40 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        // Create SVG
        const svg = container
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        const g = svg.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Create scales
        this.dayXScale = d3.scaleTime()
            .range([0, width]);

        this.dayYScale = d3.scaleLinear()
            .range([height, 0]);

        // Create axes
        this.dayXAxis = g.append("g")
            .attr("transform", `translate(0,${height})`)
            .attr("class", "x-axis");

        this.dayYAxis = g.append("g")
            .attr("class", "y-axis");

        // Create line generators
        this.dayLineGx = d3.line()
            .x(d => this.dayXScale(d.date))
            .y(d => this.dayYScale(d.gx))
            .curve(d3.curveMonotoneX);

        this.dayLineGy = d3.line()
            .x(d => this.dayXScale(d.date))
            .y(d => this.dayYScale(d.gy))
            .curve(d3.curveMonotoneX);

        this.dayLineGz = d3.line()
            .x(d => this.dayXScale(d.date))
            .y(d => this.dayYScale(d.gz))
            .curve(d3.curveMonotoneX);

        // Create paths
        this.dayPathGx = g.append("path")
            .attr("class", "line-gx")
            .attr("fill", "none")
            .attr("stroke", "#ff6b6b")
            .attr("stroke-width", 2);

        this.dayPathGy = g.append("path")
            .attr("class", "line-gy")
            .attr("fill", "none")
            .attr("stroke", "#4ecdc4")
            .attr("stroke-width", 2);

        this.dayPathGz = g.append("path")
            .attr("class", "line-gz")
            .attr("fill", "none")
            .attr("stroke", "#45b7d1")
            .attr("stroke-width", 2);

        // Add legend
        const legend = g.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${width - 100}, 20)`);

        legend.append("rect")
            .attr("width", 90)
            .attr("height", 60)
            .attr("fill", "rgba(0,0,0,0.5)")
            .attr("stroke", "#666");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 15).attr("y2", 15).attr("stroke", "#ff6b6b").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 19).text("GX").attr("fill", "white").attr("font-size", "12px");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 30).attr("y2", 30).attr("stroke", "#4ecdc4").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 34).text("GY").attr("fill", "white").attr("font-size", "12px");

        legend.append("line").attr("x1", 5).attr("x2", 20).attr("y1", 45).attr("y2", 45).attr("stroke", "#45b7d1").attr("stroke-width", 2);
        legend.append("text").attr("x", 25).attr("y", 49).text("GZ").attr("fill", "white").attr("font-size", "12px");

        // Add axis labels
        g.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .style("fill", "white")

        g.append("text")
            .attr("transform", `translate(${width / 2}, ${height + margin.bottom})`)
            .style("text-anchor", "middle")
            .style("fill", "white")
            .text("Time");
    }

    async fetchData(endpoint) {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
            return null;
        }
    }

    async updateRealtimeGraph() {
        const endpoint = this.apiUrl + 'api/v1/iotgiroscopio/last';
        const response = await this.fetchData(endpoint);
        
        if (response && response.data) {
            const data = response.data;
            const now = new Date();
            
            // Filter out null values and create data point
            const dataPoint = {
                date: new Date(data.date_uploaded),
                gx: data.gx !== null ? data.gx : 0,
                gy: data.gy !== null ? data.gy : 0,
                gz: data.gz !== null ? data.gz : 0
            };
            
            // Add to realtime data array
            this.realtimeData.push(dataPoint);
            
            // Keep only the last maxRealtimePoints
            if (this.realtimeData.length > this.maxRealtimePoints) {
                this.realtimeData = this.realtimeData.slice(-this.maxRealtimePoints);
            }
            
            // Update scales
            const xExtent = d3.extent(this.realtimeData, d => d.date);
            const yExtent = d3.extent(this.realtimeData, d => Math.max(Math.abs(d.gx), Math.abs(d.gy), Math.abs(d.gz)));
            
            this.realtimeXScale.domain(xExtent);
            this.realtimeYScale.domain([-yExtent[1] * 1.1, yExtent[1] * 1.1]);
            
            // Update axes
            this.realtimeXAxis.call(d3.axisBottom(this.realtimeXScale)
                .ticks(5)
                .tickFormat(d3.timeFormat("%H:%M:%S")));
            this.realtimeYAxis.call(d3.axisLeft(this.realtimeYScale));
            
            // Update lines
            this.realtimePathGx.datum(this.realtimeData.filter(d => d.gx !== 0))
                .attr("d", this.realtimeLineGx);
            this.realtimePathGy.datum(this.realtimeData.filter(d => d.gy !== 0))
                .attr("d", this.realtimeLineGy);
            this.realtimePathGz.datum(this.realtimeData.filter(d => d.gz !== 0))
                .attr("d", this.realtimeLineGz);
            
            // Update status
            document.querySelector("#gyroscope-sensor .sensor-status").textContent = "Activo";
            document.querySelector("#gyroscope-sensor .sensor-status").style.color = "#28a745";
        } else {
            document.querySelector("#gyroscope-sensor .sensor-status").textContent = "Error";
            document.querySelector("#gyroscope-sensor .sensor-status").style.color = "#dc3545";
        }
    }

    async updateDayGraph() {
        const endpoint = this.apiUrl + 'api/v1/iotgiroscopio/last_day';
        const response = await this.fetchData(endpoint);
        
        if (response && response.data && Array.isArray(response.data)) {
            const rawData = response.data;
            
            // Process data and filter out null values
            const processedData = rawData.map(d => ({
                date: new Date(d.date_uploaded),
                gx: d.gx !== null ? d.gx : null,
                gy: d.gy !== null ? d.gy : null,
                gz: d.gz !== null ? d.gz : null
            })).sort((a, b) => a.date - b.date);
            
            // Filter out data points where all values are null
            const validData = processedData.filter(d => d.gx !== null || d.gy !== null || d.gz !== null);
            
            if (validData.length > 0) {
                // Update scales
                const xExtent = d3.extent(validData, d => d.date);
                const allValues = [];
                validData.forEach(d => {
                    if (d.gx !== null) allValues.push(Math.abs(d.gx));
                    if (d.gy !== null) allValues.push(Math.abs(d.gy));
                    if (d.gz !== null) allValues.push(Math.abs(d.gz));
                });
                const yMax = d3.max(allValues) || 1;
                
                this.dayXScale.domain(xExtent);
                this.dayYScale.domain([-yMax * 1.1, yMax * 1.1]);
                
                // Update axes
                this.dayXAxis.call(d3.axisBottom(this.dayXScale)
                    .ticks(6)
                    .tickFormat(d3.timeFormat("%H:%M")));
                this.dayYAxis.call(d3.axisLeft(this.dayYScale));
                
                // Update lines
                this.dayPathGx.datum(validData.filter(d => d.gx !== null))
                    .attr("d", this.dayLineGx);
                this.dayPathGy.datum(validData.filter(d => d.gy !== null))
                    .attr("d", this.dayLineGy);
                this.dayPathGz.datum(validData.filter(d => d.gz !== null))
                    .attr("d", this.dayLineGz);
                
                // Update status
                document.querySelector("#accelerometer-sensor .sensor-status").textContent = "Activo";
                document.querySelector("#accelerometer-sensor .sensor-status").style.color = "#28a745";
            }
        } else {
            document.querySelector("#accelerometer-sensor .sensor-status").textContent = "Error";
            document.querySelector("#accelerometer-sensor .sensor-status").style.color = "#dc3545";
        }
    }

    startDataFetching() {
        // Update real-time graph every 1 second
        setInterval(() => {
            this.updateRealtimeGraph();
        }, 1000);
        
        // Update day graph every 30 seconds
        setInterval(() => {
            this.updateDayGraph();
        }, 30000);
        
        // Initial updates
        this.updateRealtimeGraph();
        this.updateDayGraph();
    }
}

// Initialize graphics when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new GyroscopeGraphics();
});
