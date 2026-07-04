# Xendris v1.1 - Provider Adapter Sandbox Status Note

Este documento detalla el estado actual de la implementación de **Xendris v1.1 - Provider Adapter Sandbox**.

---

## 1. Propósito y Arquitectura
El Sandbox de Adaptadores de Proveedores aísla la ejecución de modelos reales (OpenAI, Anthropic) bajo un entorno local controlado:
- **Intercepción de Red Estricta**: Las llamadas directas a red son bloqueadas de forma predeterminada, requiriendo mockups explícitos o permisos específicos.
- **Auditoría de Recursos (`SandboxAudit`)**: Mide el consumo de tokens de entrada/salida y estima el costo financiero de la solicitud.
- **Enjuiciamiento de Límites**: Interrumpe la ejecución antes de enviar la solicitud si excede los límites configurados de tokens o costo máximo.
- **Mocking Determinar**: Permite registrar respuestas simuladas basadas en patrones del prompt o del endpoint.

---

## 2. Componentes Añadidos

| Componente | Archivo | Descripción |
| :--- | :--- | :--- |
| `ProviderAdapter` | [provider_adapter.py](file:///d:/BIOCULTOR/PHYNG/xendris/core/runtime/provider_adapter.py) | Adaptador LLM estándar que implementa `ModelAdapter`. Construye payloads OpenAI y Anthropic. |
| `ProviderAdapterSandbox` | [sandbox.py](file:///d:/BIOCULTOR/PHYNG/xendris/core/runtime/sandbox.py) | Interceptor que actúa como proxy del adaptador controlando la red y enjuiciando límites. |
| `SandboxAudit` | [sandbox_audit.py](file:///d:/BIOCULTOR/PHYNG/xendris/core/runtime/sandbox_audit.py) | Estructura inmutable que registra las llamadas y consumo del sandbox. |

---

## 3. Pruebas y Cobertura
Se añadieron 20 pruebas unitarias en `tests/core/test_provider_sandbox.py` cubriendo la totalidad de las reglas del Sandbox.

### Resultados de Ejecución

#### Pruebas Enfocadas
* **Comando**: `.venv\Scripts\python.exe -m pytest tests/core/test_provider_sandbox.py -q`
* **Resultado**: **`20 passed in 0.26s`**

#### Suite de Pruebas Completa
* **Comando**: `.venv\Scripts\python.exe -m pytest -q`
* **Resultado**: **`1413 passed, 4 warnings in 178.91s`** (100% verde).

---

## 4. Limitaciones y Consideraciones
- **Estimación de Tokens**: Emplea una heurística simplificada localmente (`longitud_texto // 4`), suficiente para control de seguridad local sin acarrear dependencias pesadas de tokenización externa (e.g. tiktoken).
