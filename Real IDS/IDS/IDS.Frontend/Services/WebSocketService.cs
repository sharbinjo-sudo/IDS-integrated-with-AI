using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using IDS.Frontend.Models;

namespace IDS.Frontend.Services
{
    public class BackendWebSocketService
    {
        private readonly ClientWebSocket _socket = new();

        public async Task StartAsync(Action<List<Alert>> onData)
        {
            await _socket.ConnectAsync(
                new Uri("ws://127.0.0.1:8181"),
                CancellationToken.None
            );

            var buffer = new byte[64 * 1024];

            while (_socket.State == WebSocketState.Open)
            {
                var result = await _socket.ReceiveAsync(
                    new ArraySegment<byte>(buffer),
                    CancellationToken.None
                );

                if (result.MessageType == WebSocketMessageType.Text)
                {
                    var json = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    var alerts = JsonSerializer.Deserialize<List<Alert>>(json);

                    if (alerts != null)
                        onData(alerts);
                }
            }
        }
    }
}
