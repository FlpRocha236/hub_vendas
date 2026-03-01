# 🚀 Next Change Solutions — Hub & Plataforma Educacional White Label

Um ecossistema digital completo que atua como Landing Page de alta conversão e Plataforma de Hospedagem de Cursos/Mentorias (E-learning/SaaS) para a **Next Change Solutions**, focada em libertar produtores de conteúdo das taxas abusivas do mercado.

O projeto foi construído com arquitetura monolítica robusta em Django, indo muito além de um "site institucional". Ele já contempla um Backend estruturado com **Área do Membro**, **Painel Administrativo Customizado (Staff)** e autenticação fluida via Modais, servindo como base tecnológica sólida e escalável.

---

## 🎯 Objetivo do Projeto

Criar uma plataforma "White Label" capaz de:

- **Posicionar a marca** com autoridade de "Big Tech" local através de uma UI/UX imersiva (Dark Mode, Neon e Glassmorphism).
- **Capturar leads qualificados** direto para o funil de vendas.
- **Hospedar infoprodutos** entregando uma experiência cinematográfica aos alunos (Área de Membros com player integrado).
- **Gerenciar o negócio em uma única tela** através de um Super Dashboard Staff (CRUD de Cursos e Aulas 100% via modais, sem recarregar a página).
- Eliminar o "aluguel digital" e as taxas por venda das plataformas tradicionais.

---

## ✨ Funcionalidades Já Implementadas

### 🌐 1. UI/UX Premium (Glassmorphism & Dark Mode)

- Design inteiramente customizado com Tailwind CSS e CSS Puro (Glassmorphism).
- Modais interativos de resposta rápida para Login, Termos de Uso e Políticas de Privacidade.
- Totalmente responsivo (Mobile First).

### 📨 2. Sistema de Captação (Lead Gen)

- Landing page focada em conversão com gatilhos de "Acesso Antecipado" e "Vagas Limitadas".
- Formulário de contato seguro com proteção CSRF nativa do Django.
- Feedback visual imediato com Modal de Sucesso animado.

### 🎓 3. Área do Aluno (Dashboard & Player)

- Autenticação inteligente e silenciosa (Login via popup modal, sem telas cinzas padrão do Django).
- Redirecionamento dinâmico baseado no nível de acesso (Aluno vs. Staff).
- Interface de streaming para consumo das aulas com organização cronológica.

### ⚙️ 4. Super Dashboard Administrativo (Staff)

- Substituição completa do `/admin/` padrão do Django por um painel front-end elegante.
- Criação, Edição e Exclusão de Cursos e Aulas na mesma tela utilizando JavaScript Vanilla integrado ao backend MVT.
- Injeção inteligente de dados em formulários ocultos para edições rápidas.

### 🧪 5. Cobertura de Testes Automatizados

- Bateria com mais de 20 testes unitários cobrindo Modelos, Views Públicas, Autenticação, Rotas Protegidas e Permissões de Staff.

---

## 🚧 Roadmap: O que estamos implementando (Em Breve)

Para mostrar que a plataforma está em constante evolução, as seguintes features já estão no pipeline de desenvolvimento:

- [ ] **Gateway de Pagamento Integrado:** Checkout transparente (Stripe / Mercado Pago / Pagar.me) para processamento de cartões e PIX direto na plataforma.
- [ ] **Webhooks e Automação:** Disparo automático de e-mails (SMTP) e mensagens no WhatsApp para recuperação de carrinho e boas-vindas.
- [ ] **Progresso de Aulas:** Rastreamento de conclusão de aulas (Aulas Assistidas) e barra de progresso do aluno.
- [ ] **Emissão de Certificados:** Geração dinâmica de certificados em PDF ao concluir 100% do curso.
- [ ] **Dashboard de Inteligência de Dados:** Gráficos de vendas, LTV, Churn Rate e alunos ativos para o produtor.
- [ ] **Integração Assíncrona:** Uso de Celery/Redis para processamento em background (como conversão de vídeos ou disparos em massa).

---

## 🛠️ Tecnologias Utilizadas

| Camada                   | Tecnologias                                                                                         |
| :----------------------- | :-------------------------------------------------------------------------------------------------- |
| **Backend**        | Python 3.13, Django 5.x                                                                             |
| **Frontend**       | HTML5, Tailwind CSS, Custom Glassmorphism CSS, Bootstrap 5.3 (Grid/Modais utilitários), JS Vanilla |
| **Banco de Dados** | SQLite (Ambiente Dev) / PostgreSQL (Preparado para Produção)                                      |
| **Arquitetura**    | Padrão MVT (Model-View-Template)                                                                   |
| **Testes**         | Django `TestCase` e `Client`                                                                    |

---

## 🚀 Como Executar o Projeto Localmente

```bash
# 1. Clonar o repositório
git clone [https://github.com/SEU_USUARIO/hub_vendas.git](https://github.com/SEU_USUARIO/hub_vendas.git)

# 2. Acessar a pasta do projeto
cd hub_vendas

# 3. Criar o ambiente virtual (Virtualenv)
python -m venv venv

# 4. Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 5. Instalar as dependências
pip install -r requirements.txt

# 6. Executar migrações do Banco de Dados
python manage.py migrate

# 7. Popular o banco com dados de teste (Nosso script mágico!)
# (Cria o usuário 'aluno_teste' com senha 'aluno123', curso fictício e aulas com vídeo)
python manage.py shell -c "exec(open('setup_inicial.py', encoding='utf-8').read())"

# 8. Iniciar o servidor local
python manage.py runserver
```


O sistema estará disponível em `http://127.0.0.1:8000`

---

## 🧪 Rodando os Testes

A plataforma conta com uma suíte de testes rigorosa para garantir estabilidade em rotas e regras de negócio.

**Bash**

```
python manage.py test
```

---

## 📄 Licença

Este projeto é de propriedade da  **Next Change Solutions** . O código-fonte está fechado para fins comerciais não autorizados, mas disponível publicamente no GitHub para visualização e avaliação de portfólio técnico.

---

## 👨‍💻 Autor

**Felipe Rocha** *Estrategista de Negócios Digitais & Desenvolvedor de Software* Construindo tecnologia acessível e escalável para negócios que não querem parar no tempo.
