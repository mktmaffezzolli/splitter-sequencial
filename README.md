# 🔄 URL Splitter Sequential V2

Aplicação de distribuição sequencial de URLs com PostgreSQL.

## ✨ Funcionalidades

- **Distribuição Sequencial**: Round Robin perfeito (1→2→3→4→1...)
- **Interface Moderna**: Criar, gerenciar e deletar splits
- **Adicionar Destinos**: Quantos quiser dinamicamente
- **PostgreSQL**: Persistência garantida
- **Logs Detalhados**: Debug completo

## 🔄 Como Funciona

Acesso 1 → Destino 1
Acesso 2 → Destino 2

Acesso 3 → Destino 3
Acesso 4 → Destino 4
Acesso 5 → Destino 1 (reinicia)

## 🚀 Deploy no Railway

1. Conectar este repositório
2. Adicionar PostgreSQL
3. Configurar DATABASE_URL
4. Deploy automático

## 📊 Endpoints

- `GET /` - Interface web
- `GET /api/splits` - Listar splits
- `POST /api/splits` - Criar split
- `DELETE /api/splits/<id>` - Deletar split
- `GET /api/r/<slug>` - Redirecionamento sequencial
- `GET /api/debug/counters` - Debug contadores

## 💡 Vantagens vs Aleatório

- ✅ **Distribuição** perfeitamente igual
- ✅ **Previsível** e controlável
- ✅ **Sem** concentração em um destino
- ✅ **Justo** para todos os atendentes

## 🔧 Desenvolvimento Local

```bash
pip install -r requirements.txt
python app.py

Acesse: http://localhost:5000


4. **Clique** em "Commit new file"

## 🎯 **REPOSITÓRIO COMPLETO!**

**Agora temos todos os 6 arquivos criados! Vamos para o Railway! 🚀**

**Me confirme que criou o README.md para passarmos para o deploy! ✅**

