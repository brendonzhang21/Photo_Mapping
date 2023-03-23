import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
mapboxgl.accessToken = 'pk.eyJ1IjoiYnJlbmRvbnpoYW5nYXJ1cCIsImEiOiJjbGZjMnl4aTExajV0M3FsN25odzQxd2x3In0.8xjeM46tRziYP_j9clKVEQ';

export default function App() {

	const mapContainer = useRef(null);
	const map = useRef(null);
	const [lng, setLng] = useState(151.21);
	const [lat, setLat] = useState(-33.87);
	const [zoom, setZoom] = useState(9);

	useEffect(() => {
		if (map.current) return; // initialize map only once
		map.current = new mapboxgl.Map({
			container: mapContainer.current,
			style: 'mapbox://styles/mapbox/streets-v12',
			center: [lng, lat],
			zoom: zoom
		});

		fetch("https://brendondataapi.azurewebsites.net/api/getData",{
			mode: 'cors'
		})
			.then(response => response.json())
			.then(data => {
				console.log(data);
				data.forEach(item => {
					const popup = new mapboxgl.Popup({offset: 25})
						.setText(item.id)
					const marker = new mapboxgl.Marker()
						.setLngLat([item.GPS_Long, item.GPS_Lat])
						.setPopup(popup)
						.addTo(map.current)
				});
			});
	});

	useEffect(() => {
		if (!map.current) return; // wait for map to initialize
		map.current.on('move', () => {
			setLng(map.current.getCenter().lng.toFixed(4));
			setLat(map.current.getCenter().lat.toFixed(4));
			setZoom(map.current.getZoom().toFixed(2));
		});
	});

	return (
		<div>
			<div className="sidebar">
				Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
			</div>
			<div ref={mapContainer} className="map-container" />
		</div>
	);
}
