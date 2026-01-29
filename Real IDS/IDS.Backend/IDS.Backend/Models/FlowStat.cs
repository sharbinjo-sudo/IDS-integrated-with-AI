namespace IDS.Backend.Models
{
    public class FlowStat
    {
        public string SourceIP { get; set; }
        public string DestinationIP { get; set; }
        public double SpeedKbps { get; set; }
        public string Severity { get; set; }
        public DateTime Time { get; set; }
    }
}
