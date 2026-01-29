using System;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Windows.Data;
using IDS.Frontend.Models;
using IDS.Frontend.Services;
using System.Threading.Tasks;

namespace IDS.Frontend.ViewModels
{

    public class AlertListViewModel : INotifyPropertyChanged
    {
        public ObservableCollection<Alert> Alerts { get; }

        public ICollectionView AlertsView { get; }

        private Alert _selectedAlert;
        public Alert SelectedAlert
        {
            get => _selectedAlert;
            set
            {
                if (_selectedAlert != value)
                {
                    _selectedAlert = value;
                    OnPropertyChanged();
                }
            }
        }

        /* ---------- FILTER STATE ---------- */

        private string _searchText = "";
        public string SearchText
        {
            get => _searchText;
            set
            {
                if (_searchText != value)
                {
                    _searchText = value;
                    OnPropertyChanged();
                    AlertsView.Refresh();
                }
            }
        }
        public void UpdateAlerts(IEnumerable<Alert> newAlerts)
        {
            App.Current.Dispatcher.Invoke(() =>
            {
                Alerts.Clear();
                foreach (var alert in newAlerts)
                    Alerts.Add(alert);

                SelectedAlert = Alerts.FirstOrDefault();
                BackendStatus = "Connected";
            });
        }


        private string _severityFilter = "All";
        public string SeverityFilter
        {
            get => _severityFilter;
            set
            {
                if (_severityFilter != value)
                {
                    _severityFilter = value;
                    OnPropertyChanged();
                    AlertsView.Refresh();
                }
            }
        }

        /* ---------- STATUS BAR ---------- */

        public int TotalAlerts => Alerts.Count;
        public int HighSeverityCount => Alerts.Count(a => string.Equals(a.Severity, "High", StringComparison.OrdinalIgnoreCase));


        private string _backendStatus = "Disconnected";
        public string BackendStatus
        {
            get => _backendStatus;
            set
            {
                _backendStatus = value;
                OnPropertyChanged();
            }
        }

        private DateTime _lastUpdated;
        public DateTime LastUpdated
        {
            get => _lastUpdated;
            private set
            {
                _lastUpdated = value;
                OnPropertyChanged();
            }
        }

        /* ---------- CONSTRUCTOR ---------- */

        public AlertListViewModel()
{
    Alerts = new ObservableCollection<Alert>();
    Alerts.CollectionChanged += OnAlertsChanged;

    AlertsView = CollectionViewSource.GetDefaultView(Alerts);
    AlertsView.Filter = FilterAlert;

    SelectedAlert = null;
    LastUpdated = DateTime.Now;

    // 🔴 CONNECT TO BACKEND WEBSOCKET
    var ws = new BackendWebSocketService();

    Task.Run(() =>
    {
        ws.StartAsync(alerts =>
        {
            App.Current.Dispatcher.Invoke(() =>
            {
                UpdateAlerts(alerts);
            });
        });
    });
}
        /* ---------- FILTER LOGIC ---------- */

        private bool FilterAlert(object obj)
        {
            if (obj is not Alert alert)
                return false;

            if (SeverityFilter != "All" &&
                !string.Equals(alert.Severity, SeverityFilter, StringComparison.OrdinalIgnoreCase))
                return false;

            if (!string.IsNullOrWhiteSpace(SearchText))
            {
                var text = SearchText.ToLower();

                return alert.SourceIP.ToLower().Contains(text) ||
                       alert.DestinationIP.ToLower().Contains(text) ||
                       alert.Summary.ToLower().Contains(text) ||
                       alert.DetectionType.ToLower().Contains(text);
            }

            return true;
        }

        public void SetBackendDisconnected()
        {
            BackendStatus = "Disconnected";
        }

        private void OnAlertsChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            OnPropertyChanged(nameof(TotalAlerts));
            OnPropertyChanged(nameof(HighSeverityCount));
            LastUpdated = DateTime.Now;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}
