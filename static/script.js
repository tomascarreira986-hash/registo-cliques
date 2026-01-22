function registarClique(botao) {
    fetch(`/click/${botao}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("resultado").innerHTML = `
                <p><strong>Número do registo:</strong> ${data.numero}</p>
                <p><strong>Data:</strong> ${data.data}</p>
                <p><strong>Hora:</strong> ${data.hora}</p>
            `;
        });
}
