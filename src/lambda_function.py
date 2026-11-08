import json
import time


def lambda_handler(event, context):
    inicio = time.time()
    procesados = 0
    fallidos = []

    for record in event["Records"]:
        try:
            ubicacion = json.loads(record["body"])
            print(json.dumps({
                "message_id": record["messageId"],
                "conductor_id": ubicacion["conductor_id"],
                "lat": ubicacion["lat"],
                "lon": ubicacion["lon"],
            }))
            procesados += 1
        except Exception as e:
            print(f"Error en mensaje {record['messageId']}: {e}")
            fallidos.append({"itemIdentifier": record["messageId"]})

    duracion_ms = round((time.time() - inicio) * 1000, 2)
    print(json.dumps({
        "resumen": {
            "recibidos": len(event["Records"]),
            "procesados": procesados,
            "fallidos": len(fallidos),
            "duracion_ms": duracion_ms,
        }
    }))

    
    return {"batchItemFailures": fallidos}