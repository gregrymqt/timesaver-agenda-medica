// ============================================================================
// 📐 DEFINIÇÃO DOS TIPOS DE DADOS (JSDoc / TypeScript Style)
// ============================================================================

/**
 * Representa um objeto de agendamento médico vindo da API.
 * @typedef {Object} Agendamento
 * @property {number} id
 * @property {string} paciente
 * @property {string} cpf
 * @property {string} medico
 * @property {string} especialidade
 * @property {string} data_hora
 * @property {'Confirmado' | 'Pendente' | 'Cancelado'} status
 */

/**
 * Resposta padrão retornada pelo endpoint Flask /api/agenda.
 * @typedef {Object} ApiResponse
 * @property {'success' | 'error'} status
 * @property {Agendamento[]} [data]
 * @property {string} [message]
 */

// ============================================================================
// 🚀 LÓGICA PRINCIPAL DO FRONT-END
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Referências aos elementos do DOM
    const errorAlert = document.getElementById("api-error-alert");
    const errorMessage = document.getElementById("api-error-message");
    const searchInput = document.getElementById("search-input");

    // 1. Configuração e Instanciação do Tabulator.js
    const table = new Tabulator("#agenda-table", {
        layout: "fitColumns",
        responsiveLayout: "collapse",
        pagination: "local",
        paginationSize: 10,
        placeholder: "Carregando agendamentos...",
        columns: [
            { title: "ID", field: "id", width: 70, sorter: "number", hozAlign: "center" },
            { title: "Paciente", field: "paciente", sorter: "string" },
            { title: "CPF", field: "cpf", width: 140, hozAlign: "center" },
            { title: "Médico", field: "medico", sorter: "string" },
            { title: "Especialidade", field: "especialidade", sorter: "string" },
            { title: "Data / Hora", field: "data_hora", hozAlign: "center" },
            { 
                title: "Status", 
                field: "status", 
                hozAlign: "center",
                formatter: (cell) => {
                    const status = cell.getValue();
                    let badgeClass = "bg-secondary";
                    
                    if (status === "Confirmado") badgeClass = "bg-success";
                    if (status === "Pendente") badgeClass = "bg-warning text-dark";
                    if (status === "Cancelado") badgeClass = "bg-danger";
                    
                    return `<span class="badge ${badgeClass}">${status}</span>`;
                }
            }
        ]
    });

    // 2. Função Assíncrona para Consumir a API via Fetch Nativo
    async function carregarAgenda() {
        try {
            // Executa a requisição HTTP GET usando Fetch com Await
            const response = await fetch("/api/agenda");

            /** @type {ApiResponse} */
            const result = await response.json();

            // Trata erros de status HTTP (4xx / 5xx) ou status lógico de erro na API
            if (!response.ok || result.status !== "success") {
                const msgErro = result.message || "Erro desconhecido ao carregar a agenda.";
                throw new Error(msgErro);
            }

            // Popula a tabela com o array tipado de agendamentos
            const agendamentos = result.data || [];
            table.setData(agendamentos);

        } catch (error) {
            // Exibe mensagem amigável no alerta visual
            errorMessage.textContent = `⚠️ ${error.message}`;
            errorAlert.classList.remove("d-none");
            table.setPlaceholder("Não foi possível carregar os dados.");
        }
    }

    // 3. Executa a busca de dados
    carregarAgenda();

    // 4. Filtro de Busca em Tempo Real (Paciente, CPF ou Médico)
    searchInput.addEventListener("keyup", () => {
        const term = searchInput.value.toLowerCase().trim();

        if (!term) {
            table.clearFilter();
            return;
        }

        // Aplica o predicado de busca nas colunas
        table.setFilter((data) => {
            /** @type {Agendamento} */
            const item = data;
            
            const paciente = item.paciente ? item.paciente.toLowerCase() : "";
            const cpf = item.cpf ? item.cpf.toLowerCase() : "";
            const medico = item.medico ? item.medico.toLowerCase() : "";

            return paciente.includes(term) || cpf.includes(term) || medico.includes(term);
        });
    });
});