# API IoT — Sistema Híbrido de Detección Temprana de Incendios

Este proyecto implementa un sistema híbrido de Internet de las Cosas (IoT) orientado a la detección temprana de focos de incendio, integrando sensores ambientales, un backend IoT, dispositivos móviles y un dashboard web en tiempo real.

El sistema combina reglas basadas en umbrales con análisis inteligente para reducir falsas alarmas y mejorar la confiabilidad en escenarios reales.

---

## Resumen del Proyecto

El sistema monitorea continuamente variables ambientales como temperatura y luminosidad mediante un dispositivo IoT (Arduino / ESP32).  
Cuando los valores superan umbrales configurables, se genera un evento de riesgo que activa una segunda etapa de validación.

En esta etapa, un smartphone captura video del entorno, los cuales son analizados para confirmar o descartar la presencia de fuego.  
Finalmente, el sistema clasifica el estado como Normal, Riesgo o Confirmado, almacena los datos, actualiza el dashboard y emite alertas.

Este enfoque multisensor permite una detección más robusta que los sistemas tradicionales basados únicamente en sensores físicos.

---

## Arquitectura del Sistema

El sistema sigue un enfoque distribuido basado en Edge, Fog y Cloud Computing, permitiendo baja latencia, escalabilidad y respuesta en tiempo real.

### Diagrama de Arquitectura General

<img width="911" height="491" alt="Diagrama" src="https://github.com/user-attachments/assets/fc83e57a-8560-47e2-89ee-746e3f772a44" />

Capas del sistema:

- Edge: Arduino / ESP32, sensores ambientales, smartphone
- Fog: Backend IoT en Python (Flask), evaluación de umbrales y gestión de eventos
- Cloud: Base de datos, dashboard web y almacenamiento histórico

---

## Flujo de Funcionamiento

1. El dispositivo IoT mide variables ambientales.
2. Los datos se envían al backend mediante HTTP (JSON).
3. El servidor evalúa los valores con umbrales configurables.
4. Si se detecta riesgo, se solicita video al smartphone.
5. Se analiza la evidencia multimedia.
6. El sistema clasifica el evento.
7. El dashboard se actualiza en tiempo real y se generan alertas.

---

## Análisis Inteligente y Reducción de Falsas Alarmas

El sistema utiliza fusión de datos provenientes de sensores ambientales y video.

La decisión final se clasifica en Normal, Riesgo o Confirmado, reduciendo significativamente las falsas alarmas.

---

## Dashboard Web

![grafico1](https://github.com/user-attachments/assets/ed0dfdb6-6860-41fa-8556-bab7f3687b1f)
![grafico4](https://github.com/user-attachments/assets/90ca9daa-f62b-4287-a367-2a1f3eab18dd)

El dashboard permite visualizar sensores en tiempo real, el estado global del sistema, evidencia multimedia e historial de eventos.

---

## Alertas por correo electrónico

![email1](https://github.com/user-attachments/assets/33011512-7d58-4ffc-b836-cfac72464576)

El sistema envía alertas automáticas cuando se detecta un posible incendio.

---

## Estructura del Proyecto

API_IoT/<br>
├── arduino_code/<br>
├── frontend/<br>
├── docs/<br>
│   └── img/<br>
├── run.py<br>
├── wsgi.py<br>
├── requirements.txt<br>
├── Dockerfile<br>
├── docker-compose.yml<br>
└── IoT.session.sql<br>

---

## Instalación y Ejecución

```bash
git clone https://github.com/santiagoVL03/API_IoT.git
cd API_IoT
docker compose up --build
```

---

## Autores

- Henry Aron Yanqui Vera
- Freddy Leonel Humpiri Valdivia
- Santiago Javier Vilca Limachi
- Manuel Ángel Nifla Llallacachi
- Sennayda Rimache Choquehuanca
