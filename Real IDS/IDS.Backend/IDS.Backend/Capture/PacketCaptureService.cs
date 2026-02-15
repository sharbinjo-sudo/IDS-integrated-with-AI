using IDS.Backend.Flow;
using PacketDotNet;
using SharpPcap;

namespace IDS.Backend.Capture
{
    public class PacketCaptureService
    {
        private readonly FlowTracker _tracker;

        public PacketCaptureService(FlowTracker tracker)
        {
            _tracker = tracker;
        }

        public void Start()
        {
            var devices = CaptureDeviceList.Instance;
            if (devices.Count == 0)
                throw new Exception("No capture devices found");

            for (int i = 0; i < devices.Count; i++)
                Console.WriteLine($"{i}: {devices[i].Description}");

            Console.Write("Select device number: ");
            var index = int.Parse(Console.ReadLine()!);

            var device = devices[index];
            device.OnPacketArrival += OnPacketArrival;
            device.Open(DeviceModes.Promiscuous);
            device.StartCapture();

            Console.WriteLine($"Capturing on {device.Description}");
        }

        private void OnPacketArrival(object sender, PacketCapture e)
        {
            var packet = Packet.ParsePacket(
                e.GetPacket().LinkLayerType,
                e.GetPacket().Data
            );

            var ip = packet.Extract<IPPacket>();
            if (ip == null) return;

            _tracker.Add(
                ip.SourceAddress.ToString(),
                ip.DestinationAddress.ToString(),
                ip.TotalLength
            );
        }
    }
}
