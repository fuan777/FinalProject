export const logManager = {
    panel: document.querySelector('.log-panel'),

    addEntry(text, extra = {}) {
        const entry = document.createElement('div');
        entry.className = 'log-entry';

        const header = document.createElement('div');
        header.className = 'log-header';
        header.textContent = text;
        entry.appendChild(header);

        // 使用橙色圆点代替按钮
        if (extra.cells) {
            const dot = document.createElement('div');
            dot.className = 'render-dot';
            dot.onclick = () => this.toggleHighlight(dot, extra.cells); // 点击圆点触发放大和展示

            entry.appendChild(dot);
        }

        this.panel.appendChild(entry);
        this.panel.scrollTop = this.panel.scrollHeight;
    },

    // 处理高亮展示/隐藏
    toggleHighlight(dot, cells) {
        const isActive = dot.classList.contains('active');  // 判断是否已经放大
        document.querySelectorAll('.grid-item').forEach(div => {
            div.classList.remove('highlight');
        });

        if (isActive) {
            dot.classList.remove('active');
            cells.forEach(([x, y]) => {
                const cell = document.querySelector(`.grid-item[data-x="${x}"][data-y="${y}"]`);
                if (cell) {
                    cell.classList.remove('highlight');
                }
            });
        } else {
            dot.classList.add('active');
            cells.forEach(([x, y]) => {
                const cell = document.querySelector(`.grid-item[data-x="${x}"][data-y="${y}"]`);
                if (cell) {
                    cell.classList.add('highlight');
                }
            });
        }
    }
};
