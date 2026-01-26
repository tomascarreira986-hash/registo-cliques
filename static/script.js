function registarClique(botao) {
    fetch(`/click/${botao}`)
        .then(response => response.json())
        .then(data => {

            document.getElementById("resultado").innerHTML = `
                <p><strong>Número do clique:</strong> ${data.numero}</p>
                <p><strong>Data:</strong> ${data.data}</p>
                <p><strong>Hora:</strong> ${data.hora}</p>
            `;

            const lista = document.getElementById("listaDias");
            lista.innerHTML = "";

            data.dias.forEach(dia => {
                const li = document.createElement("li");
                li.textContent = `${dia.data} – ${dia.total} cliques`;
                lista.appendChild(li);
            });
        });
}
