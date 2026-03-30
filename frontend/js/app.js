/**
 * SISTEMA INTELIGENTE MIO CALI - Frontend
 */

const API_URL = 'http://localhost:5000/api';
let estaciones = [];

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Iniciando Sistema MIO Cali');
    await cargarEstaciones();
    await cargarRutas();
    configurarEventListeners();
    configurarSliderHora();
});

async function cargarEstaciones() {
    try {
        const response = await fetch(`${API_URL}/estaciones`);
        const data = await response.json();
        estaciones = data.estaciones;
        
        const origenSelect = document.getElementById('origen');
        const destinoSelect = document.getElementById('destino');
        
        estaciones.forEach(estacion => {
            const opt1 = document.createElement('option');
            opt1.value = estacion;
            opt1.textContent = estacion;
            origenSelect.appendChild(opt1);
            
            const opt2 = document.createElement('option');
            opt2.value = estacion;
            opt2.textContent = estacion;
            destinoSelect.appendChild(opt2);
        });
        
        console.log(`Cargadas ${estaciones.length} estaciones`);
    } catch (error) {
        console.error('Error:', error);
        mostrarError('No se pudo conectar con el servidor');
    }
}

async function cargarRutas() {
    try {
        const response = await fetch(`${API_URL}/rutas`);
        const data = await response.json();
        const grid = document.getElementById('rutas-grid');
        
        if (grid && data.rutas) {
            grid.innerHTML = '';
            data.rutas.forEach(ruta => {
                const card = document.createElement('div');
                card.className = 'info-card';
                card.style.borderTopColor = ruta.color;
                card.innerHTML = `
                    <h3 style="color: ${ruta.color}">${ruta.nombre}</h3>
                    <span class="ruta-tipo" style="background: ${ruta.color}20; color: ${ruta.color}">${ruta.tipo}</span>
                    <p class="ruta-descripcion">${ruta.descripcion}</p>
                    <div class="ruta-estaciones"><i class="fas fa-map-marker-alt"></i> ${ruta.numero_estaciones} estaciones</div>
                `;
                grid.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error cargando rutas:', error);
    }
}

function configurarEventListeners() {
    const form = document.getElementById('route-form');
    if (form) {
        form.addEventListener('submit', calcularRuta);
    }
}

function configurarSliderHora() {
    const slider = document.getElementById('hora');
    const span = document.getElementById('hora-value');
    if (slider && span) {
        slider.addEventListener('input', (e) => {
            const hora = parseInt(e.target.value);
            span.textContent = `${hora.toString().padStart(2, '0')}:00`;
            if ((hora >= 6 && hora <= 9) || (hora >= 17 && hora <= 19)) {
                span.style.background = '#ffc107';
            } else {
                span.style.background = '#f8f9fa';
            }
        });
        slider.dispatchEvent(new Event('input'));
    }
}

async function calcularRuta(event) {
    event.preventDefault();
    
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    const hora = parseInt(document.getElementById('hora').value);
    
    if (!origen || !destino) {
        mostrarError('Selecciona origen y destino');
        return;
    }
    
    if (origen === destino) {
        mostrarError('Origen y destino no pueden ser iguales');
        return;
    }
    
    mostrarLoading(true);
    ocultarResultados();
    
    try {
        const response = await fetch(`${API_URL}/ruta`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, destino, hora })
        });
        
        const resultado = await response.json();
        
        if (response.ok && resultado.exito) {
            mostrarResultados(resultado);
        } else {
            mostrarError(resultado.mensaje || 'Error al calcular ruta');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarError('Error de conexión con el servidor');
    } finally {
        mostrarLoading(false);
    }
}

function mostrarResultados(resultado) {
    const resultsDiv = document.getElementById('results');
    const summaryDiv = document.getElementById('route-summary');
    const stepsDiv = document.getElementById('route-steps');
    const statsDiv = document.getElementById('algorithm-stats');
    
    if (!resultado.exito) {
        summaryDiv.innerHTML = `<div style="background:#f8d7da;padding:20px;border-radius:12px;color:#721c24">${resultado.mensaje}</div>`;
        stepsDiv.innerHTML = '';
        statsDiv.innerHTML = '';
        resultsDiv.style.display = 'block';
        return;
    }
    
    summaryDiv.innerHTML = `
        <div class="summary-item"><i class="fas fa-map-marker-alt"></i><div><div class="label">Origen</div><div class="value">${resultado.origen}</div></div></div>
        <div class="summary-item"><i class="fas fa-flag-checkered"></i><div><div class="label">Destino</div><div class="value">${resultado.destino}</div></div></div>
        <div class="summary-item"><i class="fas fa-clock"></i><div><div class="label">Tiempo</div><div class="value">${resultado.costo_total_minutos} min</div></div></div>
        <div class="summary-item"><i class="fas fa-exchange-alt"></i><div><div class="label">Transbordos</div><div class="value">${resultado.numero_transbordos}</div></div></div>
    `;
    
    if (resultado.detalles_pasos && resultado.detalles_pasos.length > 0) {
        stepsDiv.innerHTML = resultado.detalles_pasos.map(paso => `
            <div class="step">
                <div class="step-number">${paso.paso}</div>
                <div class="step-content">
                    <div>
                        <span>${paso.desde}</span> → <span>${paso.hasta}</span>
                        <span class="step-ruta">${paso.ruta}</span>
                        ${paso.es_transbordo ? '<span class="transbordo-badge">🔄 Transbordo</span>' : ''}
                    </div>
                    <div class="step-time">⏱️ ${paso.tiempo} minutos</div>
                </div>
            </div>
        `).join('');
    } else if (resultado.ruta) {
        stepsDiv.innerHTML = `<div class="step"><div class="step-number">1</div><div class="step-content">${resultado.ruta.join(' → ')}</div></div>`;
    }
    
    statsDiv.innerHTML = `<i class="fas fa-chart-line"></i> Rutas exploradas: ${resultado.nodos_explorados} | Algoritmo de tiempos`;
    
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function mostrarLoading(mostrar) {
    const loading = document.getElementById('loading');
    const btn = document.getElementById('calcular-btn');
    if (mostrar) {
        if (loading) loading.style.display = 'block';
        if (btn) btn.disabled = true;
    } else {
        if (loading) loading.style.display = 'none';
        if (btn) btn.disabled = false;
    }
}

function ocultarResultados() {
    const results = document.getElementById('results');
    if (results) results.style.display = 'none';
}

function mostrarError(mensaje) {
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${mensaje}`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}