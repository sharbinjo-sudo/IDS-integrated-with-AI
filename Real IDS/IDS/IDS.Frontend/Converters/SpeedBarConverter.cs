using System;
using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace IDS.Frontend.Converters
{
    public class SpeedToBrushConverter : IValueConverter
    {
        // Max expected throughput: 10 MB/s = 10240 KB/s
        private const double MaxExpectedSpeedKbps = 10240.0;

        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is not double speed || speed < 0)
                return Brushes.Transparent;

            // Normalize speed to 0.0 – 1.0 range
            double ratio = Math.Min(speed / MaxExpectedSpeedKbps, 1.0);

            // LOW / NORMAL traffic (< 30%)
            if (ratio < 0.30)
            {
                // Calm blue (Task-Manager style)
                return new SolidColorBrush(Color.FromRgb(70, 110, 160));
            }

            // MEDIUM / SUSPICIOUS traffic (30% – 70%)
            if (ratio < 0.70)
            {
                // Amber / warning
                return new SolidColorBrush(Color.FromRgb(200, 160, 60));
            }

            // HIGH / DANGEROUS traffic (> 70%)
            // Red = heavy consumption or possible exfiltration
            return new SolidColorBrush(Color.FromRgb(180, 70, 70));
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
