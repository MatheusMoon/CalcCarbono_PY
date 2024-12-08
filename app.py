from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Média global de CO2e (em kg) por dia
MEDIA_GLOBAL_CO2E = 40

@app.route('/')
def index():
    return render_template('index.html')

# Rota para calcular a pegada de carbono
@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()
    transporte = float(dados.get('transporte', 0))
    carne = float(dados.get('carne', 0))
    energia = float(dados.get('energia', 0))

    # Fatores de emissão (kg CO2e)
    emissao_transporte = transporte * 0.21
    emissao_carne = carne * 27
    emissao_energia = energia * 0.5

    # Total
    total_emissao = emissao_transporte + emissao_carne + emissao_energia

    # Comparativo com a média
    comparativo_media = "menor"
    if total_emissao > MEDIA_GLOBAL_CO2E:
        comparativo_media = "maior"
    elif total_emissao == MEDIA_GLOBAL_CO2E:
        comparativo_media = "igual"

    return jsonify({
        'transporte': round(emissao_transporte, 2),
        'carne': round(emissao_carne, 2),
        'energia': round(emissao_energia, 2),
        'total': round(total_emissao, 2),
        'comparativo': comparativo_media
    })

# Função para salvar relatório em arquivo .txt
def salvar_relatorio_txt(data):
    # Abra o arquivo no modo de anexação (a), para não sobrescrever os dados antigos
    with open("relatorio.txt", "a", encoding="utf-8") as f:
        f.write(f"Transporte: {data['transporte']} kg CO₂e\n")
        f.write(f"Carne: {data['carne']} kg CO₂e\n")
        f.write(f"Energia: {data['energia']} kWh CO₂e\n")
        f.write(f"Total: {data['total']} kg CO₂e\n")
        f.write(f"Comparativo: {data['comparativo']}\n")
        f.write("-" * 40 + "\n")  # Separador entre os relatórios

# Rota para gerar e salvar o relatório
@app.route('/relatorio', methods=['POST'])
def relatorio():
    dados = request.get_json()
    transporte = float(dados.get('transporte', 0))
    carne = float(dados.get('carne', 0))
    energia = float(dados.get('energia', 0))

    # Calcula emissões
    emissao_transporte = transporte * 0.21
    emissao_carne = carne * 27
    emissao_energia = energia * 0.5
    total_emissao = emissao_transporte + emissao_carne + emissao_energia

    data = {
        'transporte': round(emissao_transporte, 2),
        'carne': round(emissao_carne, 2),
        'energia': round(emissao_energia, 2),
        'total': round(total_emissao, 2)
    }

    # Salvar relatório em arquivo .txt
    salvar_relatorio_txt(data)

    return "Relatório salvo com sucesso!", 200

if __name__ == '__main__':
    app.run(debug=True)
