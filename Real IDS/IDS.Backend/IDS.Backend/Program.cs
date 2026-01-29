using IDS.Backend.Capture;
using IDS.Backend.Flow;
using IDS.Backend.WebSocket;
using System.Diagnostics;

namespace IDS.Backend
{
    class Program
    {
        static void Main()
        {
            Console.Title = "IDS Backend - Live Packet Capture";

            var tracker = new FlowTracker();
            var capture = new PacketCaptureService(tracker);
            var ws = new WebSocketService();

            ws.Start();
            capture.Start();

            var timer = Stopwatch.StartNew();

            while (true)
            {
                Thread.Sleep(1000);

                var flows = tracker.SnapshotAndReset(timer.Elapsed.TotalSeconds);
                timer.Restart();

                ws.Send(flows);

                Console.Clear();
                Console.WriteLine("LIVE NETWORK FLOWS (KB/s)");
                Console.WriteLine("--------------------------------");
                foreach (var f in flows)
                    Console.WriteLine($"{f.SourceIP} -> {f.DestinationIP} | {f.SpeedKbps}");
            }
        }
    }
}
