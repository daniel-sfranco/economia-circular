# Economia Circular
Um marketplace focado em conectar pessoas recém chegadas a uma universidade que precisam de algum tipo de material a pessoas prestes a sair da universidade que querem doar ou vender esse mesmo material. Esse projeto está inserido no objetivo 12.5, com título "Consumo e produção responsáveis"

## Integrantes
- Daniel Soares Franco - 259083
- Gabriel Pinto Costa - 245912
- Vinícius de Oliveira Silva -251527
- Pedro Bernardo Calou - 186711
- Lucas Beserra Fernandes - 281815

## Como executar
Para garantir o funcionamento do projeto, primeiro é necessário criar e ativar um ambiente virtual Python. Como por exemplo, utilizando: \
```python -m venv venv``` e depois: \
**Linux:** ```source venv/bin/activate```\
**Windows(PowerShell):** ```venv\Scripts\activate.ps1```

Dentro do ambiente, é necessário baixar as dependências do projeto com:\
```pip install -r requirements.txt```

Para iniciar o servidor local da aplicação web, primeiro é preciso rodar o seguinte comando:\
**Linux:** ```export FLASK_APP=desapeg/app.py```\
**Windows(PowerShell):** ```$env:FLASK_APP="desapeg/app.py"```

Depois, basta rodar ```flask run```

**Atenção:** É possível popular um mock do banco de dados utilizando o comando ```python -m desapeg.seed```. Com ele, 20 produtos serão criados. Sempre que o mock é populado por esse comando, qualquer item cadastrado manualmente será apagado, pois antes de popular o banco com a seed, o projeto apaga todos os dados já existentes.