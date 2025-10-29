export function renderChart(canvasId, config) {
    if (!window.Chart) {
        return;
    }
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        return;
    }
    return new Chart(canvas.getContext('2d'), config);
}
