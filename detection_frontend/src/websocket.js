export function createWebSocket(onMessageCallback) {
    const ws = new WebSocket(`ws://${window.location.host}/stats`);

        ws.onopen = () => {
           console.log("WebSocket Connected:");
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                onMessageCallback(data);
            }catch (error) { 
                console.error("WebSocket failed fetching message:", error);
            };
        };

        ws.onerror = (error) => {
            console.error("WebSocket failed:", error);
        };

        ws.onclose = (event) => {
            console.warn("WebSocket Disconnected");
        };

return ws;
};