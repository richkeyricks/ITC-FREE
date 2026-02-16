// GLOBAL STATE
let chart;
let areaSeries, barSeries, mainSeries, volumeSeries, maSeries;
let activeTab = 'alpha';

document.addEventListener('DOMContentLoaded', () => {
    const chartContainer = document.getElementById('tv-chart');
    if (!chartContainer) return;

    // --- 1. SETUP ---
    // Force a height if specific style is missing, though CSS should handle it.
    if (chartContainer.clientHeight === 0) {
        chartContainer.style.height = '500px';
    }

    try {
        chart = LightweightCharts.createChart(chartContainer, {
            layout: {
                textColor: '#888',
                background: { type: 'solid', color: '#050505' },
            },
            grid: {
                vertLines: { color: 'rgba(40, 40, 40, 0.3)' },
                horzLines: { color: 'rgba(40, 40, 40, 0.3)' },
            },
            timeScale: {
                borderColor: 'rgba(60, 60, 60, 0.5)',
                timeVisible: true,
                secondsVisible: false,
            },
            rightPriceScale: {
                borderColor: 'rgba(60, 60, 60, 0.5)',
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
            },
            handleScale: { axisPressedMouseMove: true, mouseWheel: true, pinch: true },
            handleScroll: { mouseWheel: true, pressedMouseMove: true, vertTouchDrag: true },
        });

        // --- 2. SERIES ---
        areaSeries = chart.addAreaSeries({
            lineColor: '#d4af37', topColor: 'rgba(212, 175, 55, 0.4)', bottomColor: 'rgba(212, 175, 55, 0.0)', lineWidth: 2,
            visible: true // Default
        });

        barSeries = chart.addBarSeries({
            upColor: '#26a69a', downColor: '#ef5350', thinBars: false,
            visible: false
        });

        mainSeries = chart.addCandlestickSeries({
            upColor: '#26a69a', downColor: '#ef5350', borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350',
            visible: false
        });

        volumeSeries = chart.addHistogramSeries({
            priceFormat: { type: 'volume' },
            priceScaleId: 'vol', // Custom scale
            visible: false
        });

        chart.priceScale('vol').applyOptions({
            scaleMargins: { top: 0.8, bottom: 0 },
            visible: false
        });

        maSeries = chart.addLineSeries({
            color: '#2962ff', lineWidth: 2,
            visible: false
        });

        // --- 3. DATA ---
        const data = generateData();
        areaSeries.setData(data.line);
        barSeries.setData(data.candles);
        mainSeries.setData(data.candles);
        volumeSeries.setData(data.volume);
        maSeries.setData(data.ma);

        // --- 4. TAB SWITCHER ---
        window.switchChartTab = function (tabName) {
            activeTab = tabName;

            // UI
            document.querySelectorAll('.chart-tab').forEach(b => {
                b.style.background = 'transparent';
                b.style.color = '#888';
            });
            const btn = document.querySelector(`button[onclick="switchChartTab('${tabName}')"]`);
            if (btn) {
                btn.style.background = 'rgba(255,255,255,0.1)';
                btn.style.color = '#fff';
            }

            // Logic
            areaSeries.applyOptions({ visible: false });
            barSeries.applyOptions({ visible: false });
            mainSeries.applyOptions({ visible: false });
            volumeSeries.applyOptions({ visible: false });
            maSeries.applyOptions({ visible: false });
            mainSeries.setMarkers([]);

            if (tabName === 'alpha') {
                areaSeries.applyOptions({ visible: true });
            } else if (tabName === 'hlc') {
                barSeries.applyOptions({ visible: true });
            } else if (tabName === 'volume') {
                mainSeries.applyOptions({ visible: true });
                volumeSeries.applyOptions({ visible: true });
            } else if (tabName === 'markers') {
                mainSeries.applyOptions({ visible: true });
                mainSeries.setMarkers(data.markers);
            } else if (tabName === 'ma') {
                mainSeries.applyOptions({ visible: true });
                maSeries.applyOptions({ visible: true });
            }
        };

        // --- 5. RESIZE & INITIAL RENDER ---
        new ResizeObserver(entries => {
            if (entries.length === 0 || !entries[0].contentRect) return;
            const { width, height } = entries[0].contentRect;
            chart.applyOptions({ width, height });
            // Defer fitContent to allow painting
            requestAnimationFrame(() => {
                chart.timeScale().fitContent();
            });
        }).observe(chartContainer);

        // Force initial fit
        setTimeout(() => chart.timeScale().fitContent(), 100);

        // --- 6. LIVE SIMULATION ---
        setInterval(() => {
            updateData(data.candles, data.volume, data.ma, data.line);
        }, 1000);

    } catch (err) {
        console.error("Chart Init Error:", err);
    }
});

function generateData() {
    let candles = [], volume = [], ma = [], line = [], markers = [];
    let price = 10000;
    let time = Math.floor(Date.now() / 1000) - (365 * 86400);

    for (let i = 0; i < 365; i++) {
        const change = (Math.random() - 0.45) * 40;
        const open = price;
        const close = price + change;
        const high = Math.max(open, close) + Math.random() * 10;
        const low = Math.min(open, close) - Math.random() * 10;

        time += 86400;
        price = close;

        const c = { time, open, high, low, close };
        candles.push(c);
        line.push({ time, value: close });

        const isUp = close >= open;
        volume.push({ time, value: Math.abs(change) * 1000 + 1000, color: isUp ? 'rgba(38, 166, 154, 0.5)' : 'rgba(239, 83, 80, 0.5)' });

        // MA
        let avg = close;
        if (i > 9) { let sum = 0; for (let k = 0; k < 10; k++) sum += candles[i - k].close; avg = sum / 10; }
        ma.push({ time, value: avg });

        if (i % 25 === 0) {
            markers.push({
                time, position: isUp ? 'belowBar' : 'aboveBar',
                color: isUp ? '#2196F3' : '#FF5252',
                shape: isUp ? 'arrowUp' : 'arrowDown',
                text: 'Signal'
            });
        }
    }
    return { candles, volume, ma, line, markers };
}

function updateData(candles, volume, ma, line) {
    const last = candles[candles.length - 1];
    const change = (Math.random() - 0.5) * 10;
    last.close += change;
    last.high = Math.max(last.high, last.close);
    last.low = Math.min(last.low, last.close);

    // Update
    areaSeries.update({ time: last.time, value: last.close });
    barSeries.update(last);
    mainSeries.update(last);

    // Volume & MA update simplified for demo
    // (In real app, we'd update them precisely)
}
