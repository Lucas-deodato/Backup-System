# 🔐 Sistema de Backup Distribuído em Python

## Sobre o projeto
Este projeto implementa um **sistema de backup cliente-servidor em Python**, utilizando **sockets TCP** para comunicação e **compressão paralela com gzip** para otimização de armazenamento.  

O servidor é capaz de receber arquivos enviados por múltiplos clientes de forma concorrente, salvando-os em um diretório de backup dedicado e registrando todas as operações em um arquivo de log.  

---

## Funcionalidades
- 📂 **Envio de arquivos** de cliente para servidor via socket TCP  
- 🔒 **Controle de concorrência** com `threading.Lock` para logs consistentes  
- 🗜️ **Compressão automática** de arquivos recebidos em formato `.gz`  
- 📝 **Registro de operações** em `backup.log`  
- 🤝 **Suporte a múltiplos clientes simultâneos** com `threading`  

## Como executar

### 1. Clonar o repositório
```
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```
### 2. Iniciar o servidor
```
python3 server.py
```
O servidor ficará escutando na porta 3333 e salvará os arquivos recebidos na pasta backups/.

### 3. Enviar arquivos pelo cliente
```
python3 client.py <caminho-do-arquivo>
```
Exemplo:
```
python3 client.py teste.txt
```