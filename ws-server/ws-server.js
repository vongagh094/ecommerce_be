const WebSocket = require('ws');
const { createClient } = require('redis');
const http = require('http');

// Create a single HTTP server that will also host the WebSocket server
const server = http.createServer((req, res) => {
	// Simple REST endpoint to accept push messages from backend
	if (req.method === 'POST' && req.url === '/push') {
		let body = '';
		req.on('data', chunk => { body += chunk; });
		req.on('end', () => {
			try {
				const data = JSON.parse(body || '{}');
				// Expecting { userId: string, message: object }
				const outbound = JSON.stringify(data.message ?? data);
				wss.clients.forEach((client) => {
					if (client.readyState === WebSocket.OPEN) {
						client.send(outbound);
					}
				});
				res.writeHead(200, { 'Content-Type': 'application/json' });
				res.end(JSON.stringify({ ok: true }));
			} catch (e) {
				res.writeHead(400, { 'Content-Type': 'application/json' });
				res.end(JSON.stringify({ ok: false, error: 'Invalid JSON' }));
			}
		});
		return;
	}

	if (req.method === 'POST' && req.url === '/broadcast') {
		let body = '';
		req.on('data', chunk => { body += chunk; });
		req.on('end', () => {
			try {
				const data = JSON.parse(body || '{}');
				const outbound = JSON.stringify(data.message ?? data);
				wss.clients.forEach((client) => {
					if (client.readyState === WebSocket.OPEN) {
						client.send(outbound);
					}
				});
				res.writeHead(200, { 'Content-Type': 'application/json' });
				res.end(JSON.stringify({ ok: true }));
			} catch (e) {
				res.writeHead(400, { 'Content-Type': 'application/json' });
				res.end(JSON.stringify({ ok: false, error: 'Invalid JSON' }));
			}
		});
		return;
	}

	if (req.method === 'GET' && req.url === '/') {
		res.writeHead(200, { 'Content-Type': 'application/json' });
		res.end(JSON.stringify({ status: 'ok' }));
		return;
	}

	res.writeHead(404, { 'Content-Type': 'text/plain' });
	res.end('Not Found');
});

// Create WebSocket server on top of the HTTP server
const wss = new WebSocket.Server({ server });

// Optional Redis subscriber for backwards compatibility
const redisUrl = process.env.REDIS_URL;
if (redisUrl) {
	const redis = createClient({ url: redisUrl });
	(async () => {
		console.log('begin useWebsocket');
		await redis.connect();
		console.log('connecting redis');
		await redis.subscribe('bid_updates', (message) => {
			console.log('message from redis: ', message);
			wss.clients.forEach((client) => {
				if (client.readyState === WebSocket.OPEN) {
					console.log('client connected');
					client.send(message);
				}
			});
		});
	})();
} else {
	console.log('Redis not configured. Running WS server without Redis.');
}

wss.on('connection', (ws) => {
	ws.send(JSON.stringify({ message: 'Connected to bid updates' }));
});

// Start HTTP + WS on port 8080
server.listen(8080, () => {
	console.log('WS/HTTP server listening on port 8080');
});