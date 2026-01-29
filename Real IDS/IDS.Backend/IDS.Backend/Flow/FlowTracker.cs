using IDS.Backend.Models;
using System.Collections.Concurrent;

namespace IDS.Backend.Flow
{
    public class FlowTracker
    {
        private readonly ConcurrentDictionary<string, long> _bytes = new();

        public void Add(string src, string dst, int length)
        {
            string key = $"{src}->{dst}";
            _bytes.AddOrUpdate(key, length, (_, old) => old + length);
        }

        public List<FlowStat> SnapshotAndReset(double seconds)
        {
            var list = _bytes.Select(f =>
            {
                var parts = f.Key.Split("->");
                double kbps = (f.Value / 1024.0) / seconds;

                return new FlowStat
                {
                    SourceIP = parts[0],
                    DestinationIP = parts[1],
                    SpeedKbps = Math.Round(kbps, 1),
                    Severity = kbps > 5000 ? "High" : "Medium",
                    Time = DateTime.Now
                };
            }).ToList();

            _bytes.Clear();
            return list;
        }
    }
}
