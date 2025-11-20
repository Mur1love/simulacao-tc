# Definição das Políticas de Senhas

Este documento descreve formalmente as três políticas de senha adotadas no experimento.
Cada política é definida pelos seguintes aspectos:

- Comprimento mínimo permitido  
- Conjunto de caracteres aceitos  
- Requisitos obrigatórios de composição  
- Representação formal da linguagem correspondente  

As políticas foram modeladas como Autômatos Finitos Determinísticos (AFDs) para
uso no JFLAP e posterior automação das simulações via Python.

---

## 1. Política Fraca

### 1.1 Regras
- **Comprimento mínimo:** 4 caracteres  
- **Conjunto permitido:**
  - Letras minúsculas (`a–z`)
  - Dígitos (`0–9`)
- **Requisitos obrigatórios:**
  - Nenhum. Qualquer combinação válida com 4 ou mais caracteres é aceita.

### 1.2 Representação da Linguagem
A linguagem da política fraca é definida como:

\[
L_{\text{fraca}} = \{ w \in (a\!-\!z \cup 0\!-\!9)^* \mid |w| \ge 4 \}
\]

---

## 2. Política Média

### 2.1 Regras
- **Comprimento mínimo:** 6 caracteres  
- **Conjunto permitido:**
  - Letras minúsculas (`a–z`)
  - Letras maiúsculas (`A–Z`)
  - Dígitos (`0–9`)
- **Requisitos obrigatórios:**
  - Pelo menos **1 letra minúscula**
  - Pelo menos **1 letra maiúscula**
  - Pelo menos **1 dígito**

### 2.2 Representação da Linguagem

\[
L_{\text{media}} = \{ w \in (a\!-\!z \cup A\!-\!Z \cup 0\!-\!9)^* \mid 
|w| \ge 6,\; w \text{ contém ao menos: 1 minúscula, 1 maiúscula e 1 dígito} \}
\]

---

## 3. Política Forte

### 3.1 Regras
- **Comprimento mínimo:** 8 caracteres  
- **Conjunto permitido:**
  - Letras minúsculas  
  - Letras maiúsculas  
  - Dígitos  
  - Símbolos especiais:
  - Pelo menos **1 símbolo especial**


- **Requisitos obrigatórios:**
  - Pelo menos **1 letra minúscula**
  - Pelo menos **1 letra maiúscula**
  - Pelo menos **1 dígito**
  - Pelo menos **1 símbolo especial**

### 3.2 Representação da Linguagem

\[
L_{\text{forte}} = \{ w \in \Sigma^* \mid |w| \ge 8,\;
w \text{ contém ao menos 1 minúscula, 1 maiúscula, 1 dígito e 1 símbolo especial} \}
\]

---

## 4. Considerações Gerais

- Cada política define uma linguagem regular distinta.  
- Os AFDs permitem validar e gerar senhas compatíveis com cada política.  
- Estes modelos serão utilizados nos experimentos de simulação de ataques de força bruta e dicionário.
