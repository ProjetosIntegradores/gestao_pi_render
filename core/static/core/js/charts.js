document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Clientes por Mês
    const ctxClientes = document.getElementById('clientesPorMesChart');
    if (ctxClientes && typeof endpointGraficoClientes !== 'undefined') {
        fetch(endpointGraficoClientes) // Usa a variável global definida no template
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
    if (data.labels && data.data) {
        
        ctxClientes.height = 300; 

        new Chart(ctxClientes, {
            type: 'bar', // Tipo de gráfico: barra
                        data: {
                            labels: data.labels, // Rótulos do eixo X (ex: "Jan/2024")
                            datasets: [{
                                label: data.title || 'Número de Clientes', // Título do conjunto de dados
                                data: data.data, // Valores do eixo Y
                                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Cor das barras
                                borderColor: 'rgba(54, 162, 235, 1)', // Cor da borda das barras
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true, // Começa o eixo Y no zero
                                    ticks: {
                                        // Garante que apenas inteiros sejam mostrados no eixo Y
                                        stepSize: 1,
                                        callback: function(value) { if (Number.isInteger(value)) { return value; } },
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    display: true,
                                    position: 'top',
                                },
                                title: {
                                    display: true,
                                    text: data.title || 'Gráfico de Clientes'
                                }
                            }
                        }
                    });
                } else {
                    console.warn('Dados para o gráfico de clientes não estão no formato esperado:', data);
                    ctxClientes.parentElement.innerHTML += '<p>Não foi possível carregar os dados do gráfico de clientes.</p>';
                }
            })
            .catch(error => {
                console.error('Erro ao buscar dados para o gráfico de clientes:', error);
                if (ctxClientes.parentElement) {
                     ctxClientes.parentElement.innerHTML += `<p>Erro ao carregar dados do gráfico: ${error.message}. Verifique o console.</p>`;
                }
            });
    } else {
        if (!ctxClientes) console.warn('Elemento canvas "clientesPorMesChart" não encontrado.');
        if (typeof endpointGraficoClientes === 'undefined') console.warn('Variável "endpointGraficoClientes" não definida.');
    }

    // Exemplo: Carregar lista de clientes da API
    const listaClientesEl = document.getElementById('lista-clientes');
    if (listaClientesEl) {
        fetch('/api/clientes/?limit=5') // Pega os 5 clientes mais recentes (ajuste o 'limit' conforme sua API)
            .then(response => response.json())
            .then(data => {
                listaClientesEl.innerHTML = ''; // Limpa o "Carregando..."
                // A API do DRF pode retornar resultados paginados em 'results'
                const clientes = data.results || data; 
                if (clientes.length > 0) {
                    clientes.forEach(cliente => {
                        const li = document.createElement('li');
                        li.textContent = `${cliente.nome} - ${cliente.email}`;
                        listaClientesEl.appendChild(li);
                    });
                } else {
                    listaClientesEl.innerHTML = '<li>Nenhum cliente encontrado.</li>';
                }
            })
            .catch(error => {
                console.error('Erro ao buscar lista de clientes:', error);
                listaClientesEl.innerHTML = '<li>Erro ao carregar clientes.</li>';
            });
    }

});