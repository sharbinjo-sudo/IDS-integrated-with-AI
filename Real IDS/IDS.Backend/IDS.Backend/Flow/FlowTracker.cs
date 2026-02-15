using IDS.Backend.Models;
using System.Collections.Concurrent;

namespace IDS.Backend.Flow
{
    public class FlowTracker
    {
        private readonly ConcurrentDictionary<string, long> _bytes = new();

        public void Add(string src, string dst, int length)
        {
            var key = $"{src}->{dst}";
            _bytes.AddOrUpdate(key, length, (_, old) => old + length);
        }

        public List<FlowStat> SnapshotAndReset(double seconds)
        {
            var list = new List<FlowStat>();

            foreach (var kv in _bytes)
            {
                var parts = kv.Key.Split("->");
                var kbps = (kv.Value / 1024.0) / seconds;

                var severity =
                    kbps > 5000 ? "High" :
                    kbps > 1000 ? "Medium" : "Low";

                list.Add(new FlowStat
                {
                    Time = DateTime.Now,
                    SourceIP = parts[0],
                    DestinationIP = parts[1],
                    SpeedKbps = Math.Round(kbps, 1),
                    Severity = severity,
                    DetectionType = kbps > 5000 ? "Anomaly" : "Flow",
                    Summary = $"Traffic {Math.Round(kbps, 1)} KB/s"
                });
            }

            _bytes.Clear();
            return list;
        }
    }
}
