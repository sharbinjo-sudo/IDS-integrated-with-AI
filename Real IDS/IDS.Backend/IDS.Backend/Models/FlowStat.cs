namespace IDS.Backend.Models
{
    public class FlowStat
    {
        public DateTime Time { get; set; }
        public string SourceIP { get; set; } = "";
        public string DestinationIP { get; set; } = "";
        public double SpeedKbps { get; set; }
        public string Severity { get; set; } = "";
        public string DetectionType { get; set; } = "";
        public string Summary { get; set; } = "";
    }
}
