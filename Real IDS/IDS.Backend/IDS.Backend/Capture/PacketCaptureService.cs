using PacketDotNet;
using SharpPcap;
using IDS.Backend.Flow;
using System;

namespace IDS.Backend.Capture
{
    public class PacketCaptureService
    {
        private readonly FlowTracker _tracker;
        private ICaptureDevice? _device;

        public PacketCaptureService(FlowTracker tracker)
        {
            _tracker = tracker;
        }

        public void Start()
        {
            var devices = CaptureDeviceList.Instance;
            if (devices.Count == 0)
                throw new Exception("No capture devices found");

            Console.WriteLine("Available devices:\n");
            for (int i = 0; i < devices.Count; i++)
                Console.WriteLine($"{i}: {devices[i].Description}");

            Console.Write("\nSelect device number: ");
            if (!int.TryParse(Console.ReadLine(), out int index) ||
                index < 0 || index >= devices.Count)
                throw new Exception("Invalid device selection");

            _device = devices[index];
            _device.OnPacketArrival += OnPacketArrival;
            _device.Open(DeviceModes.Promiscuous);
            _device.StartCapture();

            Console.WriteLine($"\nCapturing on: {_device.Description}");
        }

        private void OnPacketArrival(object sender, PacketCapture e)
        {
            try
            {
                var raw = e.GetPacket();
                var packet = Packet.ParsePacket(raw.LinkLayerType, raw.Data);
                var ip = packet.Extract<IPPacket>();
                if (ip == null) return;

                _tracker.Add(
                    ip.SourceAddress.ToString(),
                    ip.DestinationAddress.ToString(),
                    ip.TotalLength
                );
            }
            catch
            {
                // Ignore malformed packets
            }
        }

        public void Stop()
        {
            _device?.StopCapture();
            _device?.Close();
        }
    }
}
