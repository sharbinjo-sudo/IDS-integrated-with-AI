using System;
using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace IDS.Frontend.Converters
{
    public class SeverityToBrushConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var severity = value as string;
            bool isSelected = parameter?.ToString() == "Selected";

            return severity switch
            {
                "High"   => new SolidColorBrush(isSelected ? Color.FromRgb(140, 40, 40)
                                                           : Color.FromRgb(180, 60, 60)),
                "Medium" => new SolidColorBrush(isSelected ? Color.FromRgb(160, 110, 30)
                                                           : Color.FromRgb(200, 140, 40)),
                "Low"    => new SolidColorBrush(isSelected ? Color.FromRgb(140, 140, 40)
                                                           : Color.FromRgb(180, 180, 60)),
                "Info"   => new SolidColorBrush(isSelected ? Color.FromRgb(60, 110, 160)
                                                           : Color.FromRgb(80, 140, 200)),
                _        => new SolidColorBrush(Color.FromRgb(60, 60, 60))
            };
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
