# Stage 2: Runner - The final, lean image
FROM python:3.11-slim

WORKDIR /app

RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot

COPY --from=builder /root/.local /home/nonroot/.local
COPY . .

# CRÍTICO: Cria a pasta onde o SQLite vai rodar e passa a posse para o nonroot
RUN mkdir -p /app/instance && chown -R nonroot:nonroot /app/instance

ENV PATH=/home/nonroot/.local/bin:$PATH
USER nonroot

# Default command to run the app with a production-grade WSGI server
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app.main:app"]