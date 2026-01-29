using Fleck;
using IDS.Backend.Models;
using System.Text.Json;

namespace IDS.Backend.WebSocket
{
    public class WebSocketService
    {
        private IWebSocketConnection _client;

        public void Start()
        {
            var server = new WebSocketServer("ws://127.0.0.1:8181");
            server.Start(ws =>
            {
                ws.OnOpen = () => _client = ws;
                ws.OnClose = () => _client = null;
            });

            Console.WriteLine("WebSocket server running");
        }

        public void Send(List<FlowStat> stats)
        {
            if (_client == null) return;
            _client.Send(JsonSerializer.Serialize(stats));
        }
    }
}
