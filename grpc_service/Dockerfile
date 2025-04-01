FROM python:3.10

WORKDIR /app

# Copier les fichiers nécessaires (mais PAS le dossier proto via volume pour conserver les stubs générés)
COPY requirements.txt ./
COPY proto /app/proto
COPY service.py client.py ./

RUN pip install --no-cache-dir -r requirements.txt

# Supprimer les anciens stubs et régénérer les nouveaux dans le dossier proto
RUN rm -f proto/egapro_pb2.py proto/egapro_pb2_grpc.py || true && \
    python -m grpc_tools.protoc -Iproto --python_out=proto --grpc_python_out=proto proto/egapro.proto && \
    sed -i "s/^import egapro_pb2 as/from . import egapro_pb2 as/" proto/egapro_pb2_grpc.py && \
    touch proto/__init__.py

# Ajouter /app au PYTHONPATH pour que "import proto.egapro_pb2" fonctionne
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 50051

CMD ["python", "service.py"]
