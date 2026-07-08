function plot_disaster_timeseries(outputs_dir)
%PLOT_DISASTER_TIMESERIES Plot synthetic weather hazard indices from Python output.
% Usage: plot_disaster_timeseries('outputs')

if nargin < 1
    outputs_dir = fullfile('..', 'outputs');
end
input_path = fullfile(outputs_dir, 'results', 'synthetic_weather_series.csv');
if ~isfile(input_path)
    error('Missing %s. Run scripts/run_synthetic_disaster_lab.py first.', input_path);
end
T = readtable(input_path);
T.timestamp = datetime(T.timestamp, 'InputFormat', "yyyy-MM-dd'T'HH:mm:ssXXX", 'TimeZone', 'UTC');
figure('Color', 'w', 'Position', [100 100 1000 430]);
plot(T.timestamp, T.rainfall_index, 'LineWidth', 1.2, 'DisplayName', 'Rainfall index');
hold on;
plot(T.timestamp, T.wind_index, 'LineWidth', 1.2, 'DisplayName', 'Wind index');
plot(T.timestamp, T.temperature_index, 'LineWidth', 1.2, 'DisplayName', 'Temperature index');
grid on;
xlabel('Time (UTC)'); ylabel('Synthetic index value');
title('Synthetic disaster-driving weather indices');
legend('Location', 'best');
exportgraphics(gcf, fullfile(outputs_dir, 'figures', 'synthetic_weather_indices_matlab.png'), 'Resolution', 250);
end
