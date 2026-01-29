using System;
using System.Globalization;
using System.Windows.Data;

namespace IDS.Frontend.Converters
{
    public class SpeedToWidthConverter : IValueConverter
    {
        // 10 MB/s = 10240 KB/s
        private const double MaxSpeedKbps = 10240.0;
        private const double MaxBarWidth = 120.0;

        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is not double speed || speed < 0)
                return 0.0;

            double ratio = Math.Min(speed / MaxSpeedKbps, 1.0);
            return ratio * MaxBarWidth;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
