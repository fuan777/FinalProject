export const api = {
    post: (url, data) => fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': window.csrfToken,  // 在main.js统一注入
        },
        body: new URLSearchParams(data),
    }).then(res => res.json()),

    parking: (coords) => api.post('/map/parking/', coords),
    finding: (coords) => api.post('/map/finding/', coords),
    reset: () => api.post('/map/reset/'),
};
