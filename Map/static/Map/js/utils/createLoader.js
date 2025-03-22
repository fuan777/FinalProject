export function createLoader() {
    const loader = document.createElement('div');
    loader.className = 'loader-container';
    loader.innerHTML = `
        <div class="loader-box">
            <div class="loader"></div>
            Processing...
        </div>
    `;
    document.body.appendChild(loader);

    return {
        show: () => loader.style.display = 'flex',
        hide: () => loader.style.display = 'none',
    };
}
