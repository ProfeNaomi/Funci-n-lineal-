<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explorador de Números Enteros</title>
    <style>
        :root {
            --primary: #4A90E2;
            --secondary: #50E3C2;
            --background: #F4F7F6;
            --text: #333333;
            --card-bg: #FFFFFF;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background);
            color: var(--text);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            margin: 0;
        }

        .container {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            max-width: 900px;
            width: 100%;
            text-align: center;
        }

        h1 {
            color: var(--primary);
            margin-bottom: 5px;
        }

        p.subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .controls {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            font-size: 24px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        input[type="number"] {
            width: 80px;
            padding: 10px;
            font-size: 20px;
            text-align: center;
            border: 2px solid #ccc;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus {
            border-color: var(--primary);
        }

        .result-box {
            min-width: 80px;
            padding: 10px;
            font-size: 24px;
            font-weight: bold;
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
            display: inline-block;
        }

        button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.1s;
        }

        button:hover {
            background-color: #357ABD;
        }

        button:active {
            transform: scale(0.98);
        }

        canvas {
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 20px;
            max-width: 100%;
        }

        .audio-player {
            margin-top: 30px;
            padding: 10px;
            background-color: #eef2f5;
            border-radius: 8px;
            display: inline-block;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Suma y Resta en Movimiento</h1>
        <p class="subtitle">Descubre cómo se mueven los números en la recta</p>

        <div class="controls">
            <input type="number" id="num1" min="-20" max="20" placeholder="Posición" title="Número inicial (-20 a 20)">
            <span>+</span>
            <input type="number" id="num2" min="-20" max="20" placeholder="Paso" title="Movimiento (-20 a 20)">
            <span>=</span>
            <div class="result-box" id="result">?</div>
        </div>

        <button onclick="animarMovimiento()">Ver Movimiento</button>

        <canvas id="numberLine" width="800" height="200"></canvas>

        <div class="audio-player">
            <p style="margin: 0 0 10px 0; font-size: 14px; color: #555;">🎧 Música de concentración (Lo-fi)</p>
            <audio controls loop>
                <source src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
                Tu navegador no soporta el elemento de audio.
            </audio>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('numberLine');
        const ctx = canvas.getContext('2d');
        const minVal = -40;
        const maxVal = 40;
        const range = maxVal - minVal;
        
        // Función para convertir un número a su coordenada X en el canvas
        function getX(val) {
            const margin = 30; // Margen a los lados
            const usableWidth = canvas.width - (margin * 2);
            return margin + ((val - minVal) / range) * usableWidth;
        }

        // Dibujar la recta numérica estática
        function dibujarRectaBase() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const y = canvas.height / 2 + 30; // Posición Y de la línea

            // Línea principal
            ctx.beginPath();
            ctx.moveTo(getX(minVal), y);
            ctx.lineTo(getX(maxVal), y);
            ctx.lineWidth = 3;
            ctx.strokeStyle = '#333';
            ctx.stroke();

            // Marcas y números
            ctx.textAlign = 'center';
            ctx.font = '12px Arial';
            ctx.fillStyle = '#333';

            for (let i = minVal; i <= maxVal; i++) {
                const x = getX(i);
                
                // Dibujar solo las marcas cada 5 unidades para no saturar visualmente
                if (i % 5 === 0) {
                    ctx.beginPath();
                    ctx.moveTo(x, y - 8);
                    ctx.lineTo(x, y + 8);
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    
                    // Destacar el cero
                    if (i === 0) {
                        ctx.fillStyle = 'red';
                        ctx.font = 'bold 14px Arial';
                    } else {
                        ctx.fillStyle = '#333';
                        ctx.font = '12px Arial';
                    }
                    ctx.fillText(i, x, y + 25);
                } else {
                    // Marcas pequeñas para los unos
                    ctx.beginPath();
                    ctx.moveTo(x, y - 3);
                    ctx.lineTo(x, y + 3);
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        }

        function animarMovimiento() {
            const input1 = document.getElementById('num1').value;
            const input2 = document.getElementById('num2').value;
            const resultBox = document.getElementById('result');

            if (input1 === '' || input2 === '') {
                alert('Por favor, ingresa ambos números.');
                return;
            }

            const val1 = parseInt(input1);
            const val2 = parseInt(input2);

            // Validar límites
            if (val1 < -20 || val1 > 20 || val2 < -20 || val2 > 20) {
                alert('Por favor, ingresa números entre -20 y 20.');
                return;
            }

            const resultadoFinal = val1 + val2;
            resultBox.innerText = resultadoFinal;

            // Redibujar la recta limpia
            dibujarRectaBase();

            const startX = getX(val1);
            const endX = getX(resultadoFinal);
            const y = canvas.height / 2 + 30;

            // 1. Dibujar punto de inicio (Posición)
            ctx.beginPath();
            ctx.arc(startX, y, 6, 0, Math.PI * 2);
            ctx.fillStyle = '#4A90E2';
            ctx.fill();

            // Texto "Inicio"
            ctx.fillStyle = '#4A90E2';
            ctx.font = 'bold 14px Arial';
            ctx.fillText('Inicio', startX, y - 15);

            // 2. Dibujar flecha de movimiento
            if (val2 !== 0) {
                // Control para hacer un arco saltando
                const controlX = (startX + endX) / 2;
                const controlY = y - Math.abs(val2) * 2 - 30; // La altura del salto depende de cuán grande es el número

                ctx.beginPath();
                ctx.moveTo(startX, y);
                ctx.quadraticCurveTo(controlX, controlY, endX, y - 5);
                ctx.strokeStyle = val2 > 0 ? '#50E3C2' : '#E94A4A'; // Verde si avanza, Rojo si retrocede
                ctx.lineWidth = 3;
                ctx.setLineDash([5, 5]); // Línea punteada
                ctx.stroke();
                ctx.setLineDash([]); // Restaurar línea sólida

                // Cabeza de la flecha
                ctx.beginPath();
                ctx.moveTo(endX, y - 5);
                ctx.lineTo(endX - (val2 > 0 ? 10 : -10), y - 15);
                ctx.lineTo(endX - (val2 > 0 ? 5 : -5), y - 20);
                ctx.fillStyle = val2 > 0 ? '#50E3C2' : '#E94A4A';
                ctx.fill();
            }

            // 3. Dibujar punto de destino (Resultado)
            ctx.beginPath();
            ctx.arc(endX, y, 6, 0, Math.PI * 2);
            ctx.fillStyle = '#333';
            ctx.fill();
            
            ctx.fillStyle = '#333';
            ctx.fillText('Llegada', endX, y - 15);
        }

        // Dibujar la recta al cargar la página
        window.onload = dibujarRectaBase;
    </script>
</body>
</html>
