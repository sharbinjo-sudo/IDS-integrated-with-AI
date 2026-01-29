using System;

namespace IDS.Frontend.Models
{
    public class Alert
    {

        public double SpeedKbps { get; set; }
        public DateTime Time { get; set; }
        public string Severity { get; set; }
        public string SourceIP { get; set; }
        public string DestinationIP { get; set; }
        public string Summary { get; set; }
        public string DetectionType { get; set; } // Rule / AI
    }
}
