import re
import os
import json
import io
from flask import Flask, request, jsonify
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)


def acessando_drive():
    load_dotenv()
    info = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    cred_dict = json.loads(info)
    SCOPES = os.getenv('SCOPES_DRIVE').split(',')
    creds = service_account.Credentials.from_service_account_info(
        cred_dict, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    return drive_service


def extrair_cnpj(texto):
    match = re.search(r"\d{14}", texto)
    return match.group(0) if match else None


@app.route('/')
def index():
    return jsonify({"mensagem": "API do certificado esta funcionando!"})


@app.route('/extrair_certificado', methods=['POST'])
def extrair_info_certificado():
    file_id = request.form.get('fileId')
    senha = request.form.get('senha')
    if not file_id or not senha:
        return jsonify({"erro": "Arquivo e senha são obrigatórios"}), 400
    try:
        resultado = []
        for file_id in file_id.split(','):
            drive_service = acessando_drive()
            request_drive = drive_service.files().get_media(fileId=file_id)
            buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(buffer, request_drive)
            done = False
            while not done:
                done = downloader.next_chunk()
            buffer.seek(0)
            pfx_data = buffer.read()
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

            resultado.append({
                "nome": nome,
                "cnpj": cnpj,
                "validade": validade,
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"Erro": str(e)}), 500


if __name__ == "__main__":
    app.run()
