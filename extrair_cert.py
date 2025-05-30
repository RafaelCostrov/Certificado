from flask import Flask, request, jsonify
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
import re

app = Flask(__name__)


def extrair_cnpj(texto):
    match = re.search(r"\d{14}", texto)
    return match.group(0) if match else None


@app.route('/')
def index():
    return jsonify({"mensagem": "API do certificado esta funcionando!"})


@app.route('/extrair_certificado', methods=['POST'])
def extrair_info_certificado():
    file = request.files.get('certificado')
    senha = request.form.get('senha')

    if not file or not senha:
        return jsonify({"erro": "Certificado e senha são necessários"}), 400

    try:
        resultados = []
        for file in request.files.getlist('certificado'):
            if not file.filename.endswith('.pfx'):
                return jsonify({"erro": "O arquivo deve ser um certificado PFX"}), 400
            pfx_data = file.read()
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                pfx_data, senha.encode(), backend=default_backend()
            )
            subject = certificate.subject
            validade = certificate.not_valid_after_utc.strftime('%Y-%m-%d')
            texto = subject.get_attributes_for_oid(
                NameOID.COMMON_NAME)[0].value
            try:
                nome, cnpj = texto.split(":")
            except ValueError:
                return jsonify({"erro": "Formato do certificado inválido"}), 400
            resultados.append({
                "nome": nome.strip(),
                "cnpj": extrair_cnpj(cnpj.strip()),
                "validade": validade,
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({"Erro": str(e)}), 500
