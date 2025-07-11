
# API dos Certificados

API simples que serve para validar informações dos certificados digitais, já enviar por e-mail e guardar na pasta correta.



## Ferramentas relacionadas

- ![Google Apps Script](https://img.shields.io/badge/Google%20Apps%20Script-4285F4?style=for-the-badge&logo=google&logoColor=white)
- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
- ![Pico.css](https://img.shields.io/badge/Pico.css-22B8CF?style=for-the-badge&logo=css3&logoColor=white)
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


*Nota: parte do Google Apps Script (com HTML, CSS e PICO.CSS) se encontra na própria plataforma.*



## Documentação da API

Demonstração simples de como utilizar os endpoints fornecidos pela API. 
As requisições devem ser feitas para:  
**https://certificadoapi.onrender.com**

#### Apenas para validação do funcionamento

```http
  GET /
```
**Exemplo de resposta esperada:**
```json
{
    "mensagem":"API do certificado esta funcionando!"
}
```


#### Extração das informações do certificado 
```http
  POST /extrair_certificado
```

| Parâmetro   |Descrição                                   |
| :--------- | :------------------------------------------ |
| `fileId`      | ID do certificado digital no drive. |
| `senha`      | Senha do certificado digital enviado. |


**Exemplo de resposta esperada:**
```json
{
    "nome": "Empresa XPTO Manutenção LTDA",
    "cnpj": "12345789000123",
    "validade": "2025-05-20",
}
```
 `nome`: Nome da empresa do certificado digital.\
 `cnpj`: CNPJ da empresa do certificado digital.\
 `validade`: Validade do certificado digital.
## Autor

- [@RafaelCostrov](https://github.com/RafaelCostrov)
