

export function showErrorMessage(message) {
    const errorPopup = document.createElement('div');
    errorPopup.className = 'error-popup';
    errorPopup.innerHTML = `
        <div class="error-content">
            <p>${message}</p>
            <button id="close-error" class="error-btn">关闭</button>
        </div>
    `;
    document.body.appendChild(errorPopup);

    // 关闭弹窗的事件处理
    document.getElementById('close-error').addEventListener('click', function () {
        document.body.removeChild(errorPopup);
    });
}
